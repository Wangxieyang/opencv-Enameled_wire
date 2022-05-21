import cv2
import roi
import estimate

frame = cv2.imread("bias.jpg")  #测试图片
(image,tl,br) = roi.roi(frame)  # 提取roi

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
cv2.imshow("image", frame)





cv2.waitKey()
