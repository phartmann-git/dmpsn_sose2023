import pickle
import random
import cv2
import mediapipe as mp
import numpy as np

# Loading the model into our program
model_dict = pickle.load(open("./model.p", "rb"))
model = model_dict["model"]

#### Get the properties for using mediapipe ####
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

mp_face = mp.solutions.face_mesh

mp_face = mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.75)

mp_faceMesh = mp.solutions.face_mesh.FaceMesh(
    refine_landmarks=True, min_detection_confidence=0.85
)
mp_face_mesh = mp.solutions.face_mesh
#####################################


# Inserting a dictionary for  pred -> char
labels_dict = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
    4: "E",
    5: "F",
    6: "G",
    7: "H",
    8: "I",
    9: "K",
    10: "L",
    11: "M",
    12: "N",
    13: "O",
    14: "P",
    15: "Q",
    16: "R",
    17: "S",
    18: "T",
    19: "U",
    20: "V",
    21: "W",
    22: "X",
    23: "Y",
}

## Learning round inits ##
rounds = 5
searchChars = [None] * rounds
counter = 0


def newRound():
    for i in range(rounds):
        searchChars[i] = labels_dict[random.randint(0, 23)]


###################

# Init of the openCV webcam capture
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
image = cap

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# While open
while True:
    data_aux = []
    x_ = []
    y_ = []

    # Termination con  or reset
    if counter == 5:
        searchChars = [None] * rounds
        counter = 0

    # Frame prep
    ret, frame = cap.read()

    # Color coding needs to be rgb so the mp model can use it
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # serching for a face
    face_result = mp_face.process(frame)
    faceMesh_result = mp_faceMesh.process(frame)

    #### drawing of the mp face detect features ####
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if face_result.detections:
        for detection in face_result.detections:
            mp_drawing.draw_detection(frame, detection)

    if faceMesh_result.multi_face_landmarks:
        for face_landmarks in faceMesh_result.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
            )
    ######################################

    # Getting the geometry of the webcam to make precise calcs later
    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    t_output_string = "Re-/start Round: 'N'\nClose Window: 'Esc' \n \nAsked: " + str(
        searchChars[counter]
    )
    y0, dy = 50, 20
    for i, line in enumerate(t_output_string.split("\n")):
        y = y0 + i * dy
        # Printing text for showing asked chars
        cv2.putText(
            frame,
            line,
            # "Asked: " + str(searchChars[counter]),
            (30, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (109, 255, 19),
            1,
        )

    # Searching for hands
    results = hands.process(frame_rgb)

    #### drawing of the mp hand detect features ####
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )
        ######################################

        #### Using the handmark coords for prediction making ####
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
        #############################################

        # Coords for the detection frame of our hands
        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10
        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        # Check if helper array holds 42  coordinates (x and y of landmarks)
        # Prevents crashing when second hand comes into webcam FOV
        if len((data_aux)) == 42:
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = labels_dict[int(prediction[0])]

            # Iterate through our searched letters
            for j in range(rounds):
                if counter != 5:
                    if predicted_character == str(searchChars[counter]):
                        counter += 1

            # Drawing the predicted letter to our hand
            cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 255, 20), 4)
            cv2.putText(
                frame,
                predicted_character,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.3,
                (50, 255, 20),
                3,
                cv2.LINE_AA,
            )

    # Window controls
    cv2.imshow("GSL Analyzer", frame)
    cv2.namedWindow("GSL Analyzer", cv2.WINDOW_NORMAL)
    c = cv2.waitKey(1)

    # Starting new round
    if c == ord("n"):
        newRound()

    # Quitting window
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()
