from PIL import Image, ImageEnhance, ImageDraw
import pytesseract
import cv2
from matplotlib import pyplot as plt


def getImgInfo(image):
    print("圖片文件格式：" + image.format)
    print("圖片大小：" + str(image.size))
    print("圖片模式：" + image.mode)


def getImgText(image, lang="chi_tra+eng"):
    text = pytesseract.image_to_string(image, lang=lang)  # 將圖片轉成字串
    return text.replace(' ', '').replace('\n', '').replace('-', '')


if __name__ == "__main__":
    try:
        # img = cv2.imread("./images/1024.jpg")
        img = cv2.imread("./images/PHRHJ.jpg")
        img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dst = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
        dst_c = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        dst_g = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        plt.subplot(131), plt.imshow(img)
        plt.subplot(132), plt.imshow(dst)
        plt.subplot(133), plt.imshow(dst_c)
        plt.show()
        print(getImgText(dst_c, lang="eng"))

    except Exception as e:
        print(e)
