import argparse
import os
import shutil
import sys
from datetime import datetime
from glob import glob
from pip._vendor import tomli


parser = argparse.ArgumentParser(
    prog="toml2xml.py",
    description="Convert toml format file to hadoop configuration files"
)
parser.add_argument('filename', type=str)
parser.add_argument('-o', dest='output_dir', type=str, required=False)


HEADER = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

"""

def move_files(src_dir, pattern, dst_dir, msg):
    filenames = glob(os.path.join(src_dir, pattern))

    for filename in filenames:
        print(msg % os.path.basename(filename))
        shutil.move(filename, dst_dir)


def iterate_flatten_dict(dct):
    stack = []
    for key, value in dct.items():
        stack.insert(-1, (key, value))

    while len(stack) > 0:
        key, value = stack.pop()
        if type(value) is dict:
            for child_key, child_value in value.items():
                stack.append((f'{key}.{child_key}', child_value))
        else:
            yield key, value


if __name__ == '__main__':
    args = parser.parse_args()

    base_dir = os.path.dirname(__file__)
    if args.output_dir is None:
        output_dir = base_dir
    else:
        output_dir = os.path.join(base_dir, args.output_dir)

    dirname = datetime.strftime(datetime.now(), '%Y%d%m-%H%M%S')
    backup_dir = os.path.join(base_dir, 'conf_backups', dirname)
    os.makedirs(backup_dir, exist_ok=True)

    try:
        with open(args.filename, 'r') as f:
            data_dict = tomli.load(f)
    except OSError as e:
        print(f'ERROR: failed to read {args.filename} -', e)
        sys.exit(1)
    except tomli.TOMLDecodeError as e:
        print('Error: parsing error -', e)
        sys.exit(1)

    if args.output_dir is None:
        dirpath = ''
    else:
        dirpath = args.output_dir

    created_files = []
    for filename, configs in data_dict.items():
        filepath = os.path.join(dirpath, filename + '.xml')

        if os.path.exists(filepath):
            print(f"Backing up {filename}.xml...")
            shutil.move(filepath, backup_dir)

        try:
            print(f'Modifying {os.path.basename(filename)}.xml...')
            created_files.append(filepath)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(HEADER)
                f.write('<configuration>\n')
                for key, value in iterate_flatten_dict(configs):
                    f.write(f'\t<property>\n\t\t<name>{key}</name>\n\t\t<value>{value}</value>\n\t</property>\n')
                f.write('</configuration>\n\n')
        except OSError as e:
            print(f'ERROR: failed to write {filepath} -', e)
            for filename in created_files:
                os.remove(filename)
            move_files(backup_dir, '*.xml', output_dir, "Restoring %s...")
            sys.exit(1)
    
    sys.exit(0)

