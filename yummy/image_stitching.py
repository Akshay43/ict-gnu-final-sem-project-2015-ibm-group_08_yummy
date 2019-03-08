import cv2 as cv
import glob
import os
import argparse
import datetime


ERROR = {0: 'OK',
             1: 'ERR_NEED_MORE_IMGS',
             2: 'ERR_HOMOGRAPHY_EST_FAIL',
             3: 'ERR_CAMERA_PARAMS_ADJUST_FAIL', }


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--images", type=str, required=True,
                        help="path to input directory of images to stitch")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="path to the output image")
    parser.add_argument("-d", "--debug", type=bool, required=False,
                        help="path to the output image")
    parser.add_argument("-n", "--nimages", type=int, required=False,
                        help="no of images to stich")
    parser.add_argument("-s", "--sort", type=bool, required=False,
                        default=False, help="sort images")

    args = vars(parser.parse_args())

    return args

def stitch(args):
    image_types = ('*.jpg', '*.png', '*.jpeg', '*.tiff')
    images_path = []

    for image_type in image_types:
        if args.get('debug', None):
            print('[INFO] ADDING ALL IMAGES WITH TYPE', image_type.split('.')[-1].upper(), 'FROM',
                  args.get('images', '').upper())
        images_path.extend(glob.glob(os.path.join(args.get('images', ''), image_type)))

    if args.get('sort', None):
        images_path = sorted(images_path, key=lambda x: int(os.path.split(x)[-1].split('_')[0][1:]))

    no_of_images = args.get('images', len(images_path))

    images = []

    for image_path in images_path:
        image = cv.imread(image_path)
        if args.get('debug', None):
            print('[INFO] READING IMAGE', os.path.split(image_path)[-1].upper())
        images.append(image)

    stitcher = cv.createStitcher(try_use_gpu=False)

    if args.get('debug', None):
        start = datetime.datetime.now()
        print('[INFO] STARTED AT', start)
        print('[INFO] PROCESSING ', no_of_images, 'IMAGES')

    (status, stitched) = stitcher.stitch(images[1:no_of_images])

    if args.get('debug', None):
        end = datetime.datetime.now()
        print('[INFO] TO STITCH', len(images), 'IMAGES TOOK', end - start)
        print('[INFO] COMPLETED AT', end)
        print('[INFO] STITCH STATUS', status)

    if status == 0:
        cv.imwrite(args.get('output', os.getcwd()), stitched)

        cv.imshow('Stitched', stitched)
        cv.waitKey(0)
    else:
        print('[INFO] ERROR', status, ERROR[status])


if __name__ == '__main__':
    args = parse_argument()
    stitch(args)
