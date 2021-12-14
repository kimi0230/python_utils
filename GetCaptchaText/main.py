from PIL import Image, ImageEnhance
import pytesseract


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


def Noise(image):
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


def getImgInfo(image):
    print("圖片文件格式：" + image.format)
    print("圖片大小：" + str(image.size))
    print("圖片模式：" + image.mode)


def getImgText(image):
    text = pytesseract.image_to_string(image)  # 將圖片轉成字串
    return text.replace(' ', '').replace('\n', '').replace('-', '')


if __name__ == "__main__":
    filePath = "./images/1.png"
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
    coverImg = Noise(coverImg)
    coverImg.show()
    print(getImgText(coverImg))
