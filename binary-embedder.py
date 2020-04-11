import argparse
import os.path


def parse_named_path(x: str):
    name, path = x.split('=')
    return name, path


parser = argparse.ArgumentParser()
parser.add_argument('header', metavar='BUNDLE_HEADER', help='header of the bundle')
parser.add_argument('source', metavar='BUNDLE_SOURCE', help='source of the bundle')
parser.add_argument('files', nargs='+', metavar='BINARY_NAME=FILE_PATH', type=parse_named_path,
                    help='binary files to embed')
args = parser.parse_args()

with open(f'{args.header}', 'w') as f:
    f.write('#include <array>\n\n')
    for name, path in args.files:
        f.write(f'extern const std::array<char, {os.path.getsize(path)}> {name};\n')

with open(f'{args.source}', 'w') as f:
    f.write('#include <array>\n\n')
    for name, path in args.files:
        size = os.path.getsize(path)
        f.write(f'extern const std::array<char, {size}> {name} = ' + '{')
        with open(path, 'rb') as f_bin:
            binary = ', '.join(hex(b) for b in f_bin.read())
        f.write(binary + '};\n')
