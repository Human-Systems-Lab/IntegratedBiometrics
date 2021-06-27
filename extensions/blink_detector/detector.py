import cv2
import dlib
import numpy as np
import imutils
from imutils import face_utils
from scipy.spatial import distance as dist

mdl_pth = "./extensions/blink_detector/shape_predictor_68_face_landmarks.dat"


class Model:
    def __init__(self):
        self.hog_extractor = dlib.get_frontal_face_detector()
        self.classifier = dlib.shape_predictor(mdl_pth)

    def forward(self, img: np.ndarray):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kpts_set = list()
        rects = self.hog_extractor(gray, 1)
        for i, rect in enumerate(rects):
            shape = self.classifier(gray, rect)
            shape = face_utils.shape_to_np(shape)
            kpts_set.append(shape[36:48])
        return kpts_set


def measure(kpts):
    wl = dist.euclidean(kpts[0], kpts[3])
    h2l = sum([
        dist.euclidean(kpts[1], kpts[5]),
        dist.euclidean(kpts[2], kpts[4]),
    ])
    wr = dist.euclidean(kpts[6], kpts[9])
    h2r = sum((
        dist.euclidean(kpts[7], kpts[11]),
        dist.euclidean(kpts[8], kpts[10]),
    ))
    return h2l / (2 * wl), h2r / (2 * wr)


def main():
    global mdl_pth
    mdl_pth = "./shape_predictor_68_face_landmarks.dat"

    mdl = Model()
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = imutils.resize(frame, width=500)
        kpts_set = mdl.forward(frame)
        for kpts in kpts_set:
            for x, y in kpts:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(0)


if __name__ == '__main__':
    main()
