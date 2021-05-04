import cv2
import mediapipe as mp
import os
import json
from google.protobuf.json_format import MessageToJson

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


class MediaPipe:
    def __init__(self):
        self.num_pose_lm = 33
        self.num_hand_lm = 21
        self.holistic_lm = {}

        self.pose_lm = {
            i: {"x": 0.0, "y": 0.0, "z": 0.0, "vis": 0.0} for i in range(self.num_pose_lm)
        }
        self.rhand_lm = {
            i: {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
            }
            for i in range(self.num_hand_lm)
        }
        self.lhand_lm = {
            i: {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
            }
            for i in range(self.num_hand_lm)
        }

    def update(self, frame):
        lms = {"pose": self.pose_lm, "rhand": self.rhand_lm, "lhand": self.lhand_lm}
        self.holistic_lm[frame] = lms

    def save_json(self, name):
        os.makedirs("data/output/json", exist_ok=True)
        with open(f"data/output/json/{name}.json", "w") as f:
            json.dump(self.holistic_lm, f)

    def reset(self):
        self.pose_lm = {
            i: {"x": 0.0, "y": 0.0, "z": 0.0, "vis": 0.0} for i in range(self.num_pose_lm)
        }
        self.rhand_lm = {
            i: {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
            }
            for i in range(self.num_hand_lm)
        }
        self.lhand_lm = {
            i: {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
            }
            for i in range(self.num_hand_lm)
        }


def landmark_to_dict(landmark, dictionary):
    for i, lm in enumerate(landmark):
        dictionary[i]["x"] = lm.x
        dictionary[i]["y"] = lm.y
        dictionary[i]["z"] = lm.z
        if lm.visibility:
            dictionary[i]["vis"] = lm.visibility


def inference(model, name):
    cap = cv2.VideoCapture(0)
    os.makedirs("data/output/video/", exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"DIVX")
    out = cv2.VideoWriter(f"data/output/video/{name}.avi", fourcc, 30, (640, 480))

    with mp_holistic.Holistic(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as holistic:

        frame = 1
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = holistic.process(image)

            pose_lm = results.pose_landmarks
            rhand_lm, lhand_lm = results.right_hand_landmarks, results.left_hand_landmarks

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Save JSON file
            if pose_lm:
                landmark_to_dict(pose_lm.landmark, model.pose_lm)
            else:
                model.pose_lm = None

            if rhand_lm:
                landmark_to_dict(rhand_lm.landmark, model.rhand_lm)
            else:
                model.rhand_lm = None

            if lhand_lm:
                landmark_to_dict(lhand_lm.landmark, model.lhand_lm)
            else:
                model.lhand_lm = None

            model.update(frame)
            model.save_json(name)
            model.reset()

            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
            mp_drawing.draw_landmarks(
                image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS
            )
            mp_drawing.draw_landmarks(
                image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS
            )
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            cv2.imshow("MediaPipe Holistic", image)
            out.write(image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            frame += 1
    cap.release()


def main(model, name):
    inference(model, name)


if __name__ == "__main__":
    model = MediaPipe()
    name = "wonjun"
    main(model, name)
