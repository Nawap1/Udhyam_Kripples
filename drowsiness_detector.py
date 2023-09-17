import cv2
import time
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import _normalized_to_pixel_coordinates as denormalize_coordinates


def calculate_distance(point_1, point_2):
    """
    Calculate the Euclidean distance between two points.

    Args:
        point_1 (tuple): Coordinates of the first point (x1, y1).
        point_2 (tuple): Coordinates of the second point (x2, y2).

    Returns:
        float: Euclidean distance between the two points.
    """
    dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5
    return dist


def calculate_eye_aspect_ratio(landmarks, reference_indexes, frame_width, frame_height):
    """
    Calculate the Eye Aspect Ratio (EAR) for one eye.

    Args:
        landmarks (list): Detected landmarks list.
        reference_indexes (list): Index positions of the chosen landmarks in order P1, P2, P3, P4, P5, P6.
        frame_width (int): Width of the captured frame.
        frame_height (int): Height of the captured frame.

    Returns:
        tuple: A tuple containing the EAR (float) and the coordinates of the chosen landmarks.
    """
    try:
        # Compute the Euclidean distance between the horizontal coordinates of selected landmarks
        coordinates_points = []
        for i in reference_indexes:
            landmark = landmarks[i]
            coordinate = denormalize_coordinates(landmark.x, landmark.y, frame_width, frame_height)
            coordinates_points.append(coordinate)

        # Calculate distances between specific landmarks
        P2_P6 = calculate_distance(coordinates_points[1], coordinates_points[5])
        P3_P5 = calculate_distance(coordinates_points[2], coordinates_points[4])
        P1_P4 = calculate_distance(coordinates_points[0], coordinates_points[3])

        # Compute the Eye Aspect Ratio (EAR)
        ear = (P2_P6 + P3_P5) / (2.0 * P1_P4)

    except:
        ear = 0.0
        coordinates_points = None

    return ear, coordinates_points


def calculate_average_ear(landmarks, left_eye_indexes, right_eye_indexes, image_width, image_height):
    """
    Calculate the average Eye Aspect Ratio (EAR) for both eyes.

    Args:
        landmarks (list): Detected landmarks list.
        left_eye_indexes (list): Index positions of landmarks for the left eye.
        right_eye_indexes (list): Index positions of landmarks for the right eye.
        image_width (int): Width of the captured frame.
        image_height (int): Height of the captured frame.

    Returns:
        tuple: A tuple containing the average EAR (float) and the coordinates of the left and right eye landmarks.
    """
    # Calculate Eye Aspect Ratio for both eyes
    left_ear, left_landmark_coordinates = calculate_eye_aspect_ratio(landmarks, left_eye_indexes, image_width,
                                                                     image_height)
    right_ear, right_landmark_coordinates = calculate_eye_aspect_ratio(landmarks, right_eye_indexes, image_width,
                                                                       image_height)

    # Calculate the average Eye Aspect Ratio
    avg_ear = (left_ear + right_ear) / 2.0

    return avg_ear, (left_landmark_coordinates, right_landmark_coordinates)


def draw_eye_landmarks(frame, left_landmark_coordinates, right_landmark_coordinates, color):
    """
    Draw landmarks for both eyes on the frame.

    Args:
        frame (numpy.ndarray): Input frame.
        left_landmark_coordinates (list): Coordinates of landmarks for the left eye.
        right_landmark_coordinates (list): Coordinates of landmarks for the right eye.
        color (tuple): BGR color for drawing the landmarks.

    Returns:
        numpy.ndarray: Frame with landmarks drawn.
    """
    for lm_coordinates in [left_landmark_coordinates, right_landmark_coordinates]:
        if lm_coordinates:
            for coord in lm_coordinates:
                cv2.circle(frame, coord, 2, color, -1)

    frame = cv2.flip(frame, 1)
    return frame


def draw_text(image, text, position, color, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.8, thickness=2):
    """
    Draw text on the image.

    Args:
        image (numpy.ndarray): Input image.
        text (str): Text to be drawn.
        position (tuple): Coordinates (x, y) where the text should be placed.
        color (tuple): BGR color of the text.
        font (int): Font type.
        font_scale (float): Font scale.
        thickness (int): Thickness of the text.

    Returns:
        numpy.ndarray: Image with text drawn.
    """
    image = cv2.putText(image, text, position, font, font_scale, color, thickness)
    return image

left_eye_landmarks = [362, 385, 387, 263, 373, 380]
right_eye_landmarks = [33, 160, 158, 133, 153, 144]

# Used for coloring landmark points.
# Its value depends on the current EAR value.
RED = (0, 0, 255)  # BGR
GREEN = (0, 255, 0)  # BGR

# Initializing Mediapipe FaceMesh solution pipeline
facemesh_model = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

# For tracking counters and sharing states in and out of callbacks.
start_time = time.perf_counter()
drowsy_time = 0.0
highlight_color = GREEN
sound_alarm = False

state_tracker = {
    "DROWSY_TIME": 0.0,  # Holds the amount of time passed with EAR < EAR_THRESH
    "COLOR": GREEN,
    "play_alarm": False,
}

EAR_text_position = (10, 30)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Error while opening the video')
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error in retrieving frame.")
        break
    frame.flags.writeable = False
    frame_height, frame_width, _ = frame.shape

    DROWSY_TIME_text_position = (400, 30)
    ALARM_text_position = (420, 55)

    results = facemesh_model.process(frame)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        EAR, coordinates = calculate_average_ear(landmarks, left_eye_landmarks, right_eye_landmarks, frame_width, frame_height)
        frame = cv2.flip(frame, 1)

        if EAR < 0.2:
            state_tracker["DROWSY_TIME"] += 0.1

            if state_tracker["DROWSY_TIME"] >= 3:
                state_tracker["play_alarm"] = True
                draw_text(frame, "STAY ALERT!", ALARM_text_position, RED)

        else:
            state_tracker["DROWSY_TIME"] = 0.0
            state_tracker["COLOR"] = GREEN
            state_tracker["play_alarm"] = False

        EAR_text = f"EAR: {round(EAR, 2)}"
        DROWSY_TIME_text = f"DROWSY: {round(state_tracker['DROWSY_TIME'], 3)} Secs"
        draw_text(frame, EAR_text, EAR_text_position, state_tracker["COLOR"])
        draw_text(frame, DROWSY_TIME_text, DROWSY_TIME_text_position, RED)

    else:
        state_tracker["DROWSY_TIME"] = 0.0
        state_tracker["COLOR"] = GREEN
        state_tracker["play_alarm"] = False

        frame = cv2.flip(frame, 1)
    if state_tracker['play_alarm'] == True:
        draw_text(frame, DROWSY_TIME_text, DROWSY_TIME_text_position, RED)

    cv2.imshow('Video Feed', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
