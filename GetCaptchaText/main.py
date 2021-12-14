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


# 灰階影像
def Grayscale(image):
    # 處理灰白
    image = image.convert("L")
    return image


# 二值化
def Binarization(image, threshold):
    pixels = image.load()
    for x in range(image.width):
        for y in range(image.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return image

# 雜訊處理


def clearNoise2(image):
    data = image.getdata()
    coverImg = image
    w, h = coverImg.size
    count = 0
    for x in range(1, h-1):
        for y in range(1, h - 1):
            # 找出各個像素方向
            mid_pixel = data[w * y + x]
            if mid_pixel == 0:
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]
                if top_pixel == 0:
                    count += 1
                if left_pixel == 0:
                    count += 1
                if down_pixel == 0:
                    count += 1
                if right_pixel == 0:
                    count += 1
                if count > 4:
                    coverImg = image
                    coverImg.putpixel((x, y), 0)
    return coverImg

# ------- DO NOT EDIT BELOW -------
# Code from https://stackoverflow.max-everyday.com/2019/06/python-opencv-denoising/


def getPixel(image, x, y, G, N):
    L = image.getpixel((x, y))
    if L > G:
        L = True
    else:
        L = False

    nearDots = 0
    if L == (image.getpixel((x - 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x, y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1, y + 1)) > G):
        nearDots += 1

    if nearDots < N:
        return image.getpixel((x, y-1))
    else:
        return None

# 降噪 Function


def clearNoise(image, G, N, Z):
    draw = ImageDraw.Draw(image)

    for i in range(0, Z):
        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                color = getPixel(image, x, y, G, N)
                if color != None:
                    draw.point((x, y), color)
    return image


if __name__ == "__main__":
    try:
        filePath = "./images/1024.jpg"
        captcha = Image.open(filePath)

        # 查看圖片文件內容
        getImgInfo(captcha)

        # 轉換圖片
        coverImg = Grayscale(captcha)
        coverImg = Binarization(coverImg, 150)

        # 增強圖片顯示效果
        enhancer = ImageEnhance.Contrast(coverImg)
        coverImg = enhancer.enhance(4)
        # coverImg.show()

        # 處理有雜訊的數字圖片
        coverImg = clearNoise2(coverImg)
        # coverImg = clearNoise(coverImg, 50, 4, 6)
        # coverImg.show()
        print(getImgText(coverImg, lang="eng"))

    except Exception as e:
        print(e)
