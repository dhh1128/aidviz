from argparse import ArgumentParser
import re

ASPECT_RATIO_PAT = re.compile(r'(\d+):(\d+)')

def viz(entropy, width, height):
    print(f'Entropy: {entropy}')
    print(f'Width: {width}')
    print(f'Height: {height}')

def main():
    parser = ArgumentParser(
        prog='entviz',
        description='Visualize entropy as an SVG file.')
    parser.add_argument('entropy')
    parser.add_argument('--ar')
    args = parser.parse_args()
    if args.ar:
        match = ASPECT_RATIO_PAT.match(args.ar)
        if not match:
            parser.error('Invalid aspect ratio')
        width, height = map(int, match.groups())
    else:
        width, height = 1, 1
    try:
        viz(args.entropy, width, height)
    except:
        import sys, traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()