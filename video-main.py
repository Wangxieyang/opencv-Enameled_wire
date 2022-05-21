import cv2
import roi
import estimate

h0 = 170
w0 = 115  # 量取目标区域高、宽
h1 = 480  # 摄像头画面高度
w1 = 640  # 摄像头画面宽度



capture = cv2.VideoCapture(0)  # 调用摄像头
while True:
    ret, frame = capture.read()  # 提取摄像头当前帧，没有则返回0
    (image, tl, br) = roi.roi(frame)

    result = estimate.estimate(image)

    cv2.rectangle(frame, (tl[0], tl[1]), (br[0], br[1]), (0, 255, 0), 1)
    if result == 0:
        cv2.putText(frame, "NONE", (tl[0], br[1]+20), 0, 1, (255, 255, 255), 1, 1)
    if result == 1:
        cv2.putText(frame, "COCKED", (tl[0], br[1] + 20), 0, 1, (255, 255, 255), 1, 1)
    if result == 2:
        cv2.putText(frame, "BIAS", (tl[0], br[1] + 20), 0, 1, (255, 255, 255), 1, 1)
    if result == 3:
        cv2.putText(frame, "INCLINE", (tl[0], br[1] + 20), 0, 1, (255, 255, 255), 1, 1)
    if result == 4:
        cv2.putText(frame, "WELL", (tl[0], br[1] + 20), 0, 1, (255, 255, 255), 1, 1)
    cv2.imshow("camera", frame)
    key = cv2.waitKey(1)
    if key != -1:
        break

capture.release()
