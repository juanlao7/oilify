import argparse
import sys
import random
import time
import numpy as np
from matplotlib import pyplot as plt
from skimage import draw
from math import ceil, pi

MEASURE_MIN_TIME = False
BRUSHES = 50

def showImage(image):
    plt.imshow(image)
    plt.show()

def process(inputImage, brushSize, expressionLevel):
    start = time.time()
    
    brushSizeInt = int(brushSize)
    expressionSize = brushSize * expressionLevel
    margin = int(expressionSize * 2)
    halfBrushSizeInt = brushSizeInt // 2
    
    shape = ((inputImage.shape[0] - 2 * margin) // brushSizeInt, (inputImage.shape[1] - 2 * margin) // brushSizeInt)
    brushes = [draw.ellipse(halfBrushSizeInt, halfBrushSizeInt, brushSize, random.randint(brushSizeInt, expressionSize), rotation=random.random() * pi) for _ in range(BRUSHES)]

    result = np.zeros(inputImage.shape, dtype=np.uint8)

    for x in range(margin, inputImage.shape[0] - margin, brushSizeInt):
        for y in range(margin, inputImage.shape[1] - margin, brushSizeInt):
            ellipseXs, ellipseYs = random.choice(brushes)
            result[x + ellipseXs, y + ellipseYs] = inputImage[x, y]
    
    return result, time.time() - start

parser = argparse.ArgumentParser(description='Convert any image into an impressionist oil painting.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('input_image', help='File path of the input image. Compatible with most common image formats.')
parser.add_argument('output_image', help='File path of the output image. Format is inferred from the extension of the file name. Compatible with most common image formats.')
parser.add_argument('-s', dest='brush_size', default=5.0, type=float, help='Brush size.')
parser.add_argument('-e', dest='expression_level', default=2.0, type=float, help='Expression level.')
parser.add_argument('-r', dest='random_seed', default=0, type=int, help='Random seed.')
args = parser.parse_args()

random.seed(args.random_seed)
inputImage = plt.imread(args.input_image)

if inputImage.ndim < 3:
    sys.exit('Only RGB or RGBA images supported.')
elif inputImage.ndim == 4:
    inputImage = inputImage[:, :, :3]

if MEASURE_MIN_TIME:
    times = np.zeros(5)

    for i in range(5):
        _, duration = process(inputImage, args.brush_size, args.expression_level)
        times[i] = duration

    print(times)
    print(times.min())
else:
    result, duration = process(inputImage, args.brush_size, args.expression_level)
    print('Processed in', round(duration, 2), 'seconds.')
    plt.imsave(args.output_image, result)
