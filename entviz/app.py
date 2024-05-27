from argparse import ArgumentParser
import re

ASPECT_RATIO_PAT = re.compile(r'(\d+):(\d+)')

def viz(entropy, ar_width, ar_height, fontsize):
    print(f'Entropy: {entropy}')
    print(f'Width: {width}')
    print(f'Height: {height}')

def main():
    parser = ArgumentParser(
        prog='entviz',
        description='Visualize entropy as an SVG file.')
    parser.add_argument('entropy')
    parser.add_argument('--ar', '--aspectratio', metavar='RATIO', default='1:1')
    parser.add_argument('--fs', '--fontsize', metavar='POINT', default=12, type=int)
    args = parser.parse_args()
    ar_width, ar_height = 1, 1
    fontsize = 12
    if args.ar:
        match = ASPECT_RATIO_PAT.match(args.ar)
        if match:
            ar_width, ar_height = map(int, match.groups())
            if ar_width < 1 or ar_height < 1 or ar_width > 100 or ar_height > 100:
                parser.error('Invalid aspect ratio.')
    if args.fs:
        fontsize = args.fs
        if fontsize < 6 or fontsize > 30:
            parser.error('Invalid font size.')
    try:
        viz(args.entropy, ar_width, ar_height, fontsize)
    except:
        import sys, traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()