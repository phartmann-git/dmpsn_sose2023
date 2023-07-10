import os
import cv2

# Getting directory
DATA_DIR = "./dataset"

# Preping our data collection scope
n_of_letters = 24
samples_per_letter = 100
alphabet = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
]

# Utilizing webcam
cap = cv2.VideoCapture(0)

# Iterating through our chars
for j in range(len(alphabet)):
    # Creating folder structure if needed
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    # Info so we dont lose track while collecting
    print("Collecting data for letter " + alphabet[j])
    printout = 'Letter "' + alphabet[j] + '" is next. Press "c".'
    done = False
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        cv2.putText(
            frame, printout, (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2
        )
        cv2.imshow("frame", frame)
        if cv2.waitKey(25) == ord("c"):
            break

    #### Capturing usable frames ####
    counter = 0
    while counter < samples_per_letter:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(25)
        cv2.imwrite(os.path.join(DATA_DIR, str(j), "{}.jpg".format(counter)), frame)

        counter += 1
    ##########################

cap.release()
cv2.destroyAllWindows()
