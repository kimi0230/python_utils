import imageio
from os import listdir
from os.path import isfile, join
import cv2


# mode: {‘i’, ‘I’, ‘v’, ‘V’, ‘?’}
# Used to give the writer a hint on what the user expects(default ‘?’): “i” for an image, “I” for multiple images, “v” for a volume, “V” for multiple volumes, “?” for don’t care.
def start(filename, source):
    with imageio.get_writer(filename, mode='I', fps="0.3") as writer:
        for s in source:
            image = imageio.imread(s)
            # print(image.shape)
            # scale_percent = 100       # percent of original size
            # width = int(image.shape[1] * scale_percent / 100)
            # height = int(image.shape[0] * scale_percent / 100)
            # dim = (width, height)
            # print(dim)
            dim = (370, 500)
            image = cv2.resize(
                image, dim, interpolation=cv2.INTER_AREA)
            writer.append_data(image)


if __name__ == "__main__":
    botPath = "images/bot/"
    source = [botPath+f for f in listdir(botPath) if isfile(join(botPath, f))]
    filename = "build/bot.gif"
    start(filename, source)

    botPath = "images/notify/"
    source = [botPath+f for f in listdir(botPath) if isfile(join(botPath, f))]
    filename = "build/notify.gif"
    start(filename, source)
