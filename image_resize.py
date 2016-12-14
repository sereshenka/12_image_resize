import argparse
from PIL import Image
import os


def get_resized_image_size(size, args):
    if args.scale and not args.height and not args.width:
        return tuple(map(lambda x: int(x*args.scale), size))
    if args.width and not args.height and not args.scale:
        return tuple(map(lambda x: int(x*args.width/size[0]), size))
    if args.height and not args.width and not args.scale:
        return tuple(map(lambda x: int(x*args.height/size[1]), size))
    if args.height and args.width and not args.scale:
        if args.width/args.height != size[0]/size[1]:
            print('scale is not the same')
        return (int(args.width), int(args.height))
    raise Exception('incorrect parameters')


def get_resized_image_name(name, size):
    dot_index = name.rfind('.')
    res_name = '{}__{}x{}{}'.format(
        name[:dot_index],
        str(size[0]),
        str(size[1]),
        name[dot_index:]
    )
    return res_name


def resize_image(args):
    im = Image.open(args.original_path)
    width, height = im.size
    new_size = get_resized_image_size((width, height), args)
    new_name = get_resized_image_name(os.path.basename
                                      (args.original_path),
                                      new_size)
    if args.output:
        path_to_resized = os.path.join(args.output, new_name)
    else:
        path_to_resized = os.path.join(os.path.dirname(args.original_path),
                                       new_name)

    im = im.resize(new_size)
    im.save(path_to_resized)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--original_path', help='Укажите путь к картинке ', 
                        required = True, nargs = '?')
    parser.add_argument('--width', help='Укажите ширину результирующей'
                        'картинки', type = int, nargs = '?')
    parser.add_argument('--height', help='Укажите высоту результирующей'
                        'картинки ', type = int, nargs = '?')
    parser.add_argument('--scale', help='Укажите во сколько раз'
                        'увеличить изображение ', type = float, nargs = '?')
    parser.add_argument('--output', help='Укажите, куда сохранить ', nargs = '?')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    resize_image(args)
