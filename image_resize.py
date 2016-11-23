import os
import argparse
from PIL import Image


def input_all_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--original_path', help='Укажите путь к картинке ', \
                        required = True, nargs = '?')
    parser.add_argument('--width', help='Укажите ширину результирующей'\
                        'картинки', nargs = '?')
    parser.add_argument('--height', help='Укажите высоту результирующей'\
                        'картинки ', nargs = '?')
    parser.add_argument('--scale', help='Укажите во сколько раз'\
                        'увеличить изображение ', nargs = '?')
    parser.add_argument('--output', help='Укажите, куда класть'\
                        'результирующий фаил ', nargs = '?')
    original_path = parser.parse_args().original_path
    width = parser.parse_args().width
    height = parser.parse_args().height
    scale = parser.parse_args().scale
    output_path = parser.parse_args().output
    return original_path, width, height, scale, output_path  


def open_image(original_path):
    try:
        original_image = Image.open(original_path)
        return original_image
    except IOError:
        return None


def resize_with_scale(original_image, input_scale):
    return Image.putdata(original_image, scale = input_scale)
    

def resize_with_width_or_height(original_image, width, height,\
                                original_width, original_height):
    proportions_warning = 0
    if width is not None and height is not None:
        proportions_width = width/original_width
        proportions_height = height/original_height
        if proportions_width != proportions_height:
            raise proportions_warning
        return original_image.resize(width, height), proportions_warning
    elif width is not None:
        new_height = original_height*(width/original_width)
        return original_image.resize(width, new_height), proportions_warning
    elif height is not None:
        new_width = original_width*(height/original_height)
        return original_image.resize(new_width, height), proportions_warning


if __name__ == '__main__':
    while True:
        original_path, width, height, scale, output_path = input_all_arguments()
        if scale and (width or height):
            print('нельзя вводить масштаб и ... одновременно')
            break
        if not width and not height and not scale:
            print('Ничего не заданно')
            break
        if os.path.exists(original_path):
            original_image = open_image(original_path)
            original_width, original_height = original_image.size
            if scale is not None:
                try:
                    round(scale)
                except TypeError:
                    print('Неверный формат')
                    break
                resize_with_scale(original_image, scale)
            else:
                if width:
                    print('wow')
                    try:
                        width = int(width)
                    except TypeError:
                        print('Неверный формат')
                        break
                if height:
                    try:
                        height = int(height)
                    except TypeError:
                        print('Неверный формат')
                        break
                resize_with_width_or_height(original_image, width, height, \
                                            original_width, original_height)
        else:
            print('не правильно задан путь')
            break
        break
