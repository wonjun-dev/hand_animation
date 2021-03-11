import cv2
import mediapipe as mp
import os
import json

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

file_list = [
    "source/input/imgs/rock.jpg",
    "source/input/imgs/scissor.jpg",
    "source/input/imgs/paper.jpg",
]


def _coords_to_json(hand_landmarks, name, num_landmarks=21):
    coords_dict = {i: {"x": 0.0, "y": 0.0, "z": 0.0} for i in range(num_landmarks)}
    assert num_landmarks == len(hand_landmarks.landmark), "The number of landmark is not matched"

    for idx in range(num_landmarks):
        coords_dict[idx]["x"] = hand_landmarks.landmark[idx].x
        coords_dict[idx]["y"] = hand_landmarks.landmark[idx].y
        coords_dict[idx]["z"] = hand_landmarks.landmark[idx].z

    os.makedirs("source/output/json", exist_ok=True)
    with open(f"source/output/json/{name}.json", "w") as f:
        json.dump(coords_dict, f)

    # print(dir(hand_landmarks))
    # print(hand_landmarks.landmark)
    # print(len(hand_landmarks.landmark))
    # print(hand_landmarks.landmark[0])


def img_inference(file_list, static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5):

    with mp_hands.Hands(
        static_image_mode=static_image_mode,
        max_num_hands=max_num_hands,
        min_detection_confidence=min_detection_confidence,
    ) as hands:

        for idx, file in enumerate(file_list):
            # Read an image, flip it around y-axis for correct handedness output (see above)
            image = cv2.flip(cv2.imread(file), 1)
            # Convert the BGR image to RGB before processing.
            results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # Print handedness and draw hand landmarks on the image.
            print("Handedness:", results.multi_handedness)
            if not results.multi_hand_landmarks:
                continue
            image_height, image_width, _ = image.shape
            annotated_image = image.copy()
            for hand_landmarks in results.multi_hand_landmarks:
                _coords_to_json(hand_landmarks, name=str(idx))
                print("hand_landmarks:", hand_landmarks)
                print(
                    f"Index finger tip coordinates: (",
                    f"{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, "
                    f"{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})",
                )
                mp_drawing.draw_landmarks(
                    annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

            os.makedirs("source/output/imgs/", exist_ok=True)
            cv2.imwrite("source/output/imgs/" + str(idx) + ".png", cv2.flip(annotated_image, 1))


def video_inference():
    # # For webcam input:
    # cap = cv2.VideoCapture(0)
    # with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    #     while cap.isOpened():
    #         success, image = cap.read()
    #         if not success:
    #             print("Ignoring empty camera frame.")
    #             # If loading a video, use 'break' instead of 'continue'.
    #             continue

    #         # Flip the image horizontally for a later selfie-view display, and convert
    #         # the BGR image to RGB.
    #         image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    #         # To improve performance, optionally mark the image as not writeable to
    #         # pass by reference.
    #         image.flags.writeable = False
    #         results = hands.process(image)

    #         # Draw the hand annotations on the image.
    #         image.flags.writeable = True
    #         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #         if results.multi_hand_landmarks:
    #             for hand_landmarks in results.multi_hand_landmarks:
    #                 mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    #         cv2.imshow("MediaPipe Hands", image)
    #         if cv2.waitKey(5) & 0xFF == 27:
    #             break
    # cap.release()
    pass


if __name__ == "__main__":
    img_inference(file_list)