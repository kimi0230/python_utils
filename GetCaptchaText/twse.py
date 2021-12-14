import pytesseract
import numpy as np
import cv2
from matplotlib import pyplot as plt


def getImgInfo(image):
    print("圖片文件格式：" + image.format)
    print("圖片大小：" + str(image.size))
    print("圖片模式：" + image.mode)


def getImgText(image, lang="chi_tra+eng"):
    text = pytesseract.image_to_string(image, lang=lang)  # 將圖片轉成字串
    print("---", text)
    return text.replace(' ', '').replace('\n', '').replace('-', '')


if __name__ == "__main__":
    img = cv2.imread("./images/azAz09.png")
    kernel = np.ones((4, 4), np.uint8)
    # 橡皮擦
    erosion = cv2.erode(img, kernel, iterations=1)
    # 模糊
    blurred = cv2.GaussianBlur(erosion, (5, 5), 0)
    # 偵測邊界
    edged = cv2.Canny(blurred, 30, 150)
    dilation = cv2.dilate(edged, kernel, iterations=1)
    contours, hierarchy = cv2.findContours(
        dilation.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted([(c, cv2.boundingRect(c)[0])
                  for c in contours], key=lambda x: x[1])
    ary = []
    for (c, _) in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w > 15 and h > 15:
            ary.append((x, y, w, h))

    fig = plt.figure()
    for id, (x, y, w, h) in enumerate(ary):
        roi = dilation[y:y+h, x:x+w]
        thresh = roi.copy()
        a = fig.add_subplot(1, len(ary), id+1)
        res = cv2.resize(thresh, (50, 50))
        # cv2.imwrite("%d.png" % (id), res)
        print(getImgText(res, lang="eng"))
        plt.imshow(thresh)

    # plt.subplot(121), plt.imshow(img)
    # plt.subplot(122), plt.imshow(dilation)
    # plt.show()
    # print(getImgText(dilation, lang="eng"))
