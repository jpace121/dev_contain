#
# Copyright 2019 James Pace
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
import subprocess
import dev_contain.common as common

def list_(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' list', description='List known containers and images.')
    parser.add_argument('--all', '-a', action='store_true', help='Also list containers/images not labeled by dev_contain.')
    args = parser.parse_args(in_args)

    manager = common.get_manager()

    filter_text = '--filter label=com.github.jpace121.dev_contain.compat=true '
    if args.all:
        filter_text = ''

    # Note that python format strings collide with the syntax for the format
    # commands.
    command = manager + ' images '\
                + filter_text + \
                '--filter dangling=false '\
                '--format "{{.Repository}}"'
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    print('Images: ')
    for line in output.stdout.splitlines():
        print('\t' + line.decode())

    command = manager + ' ps -a '\
                + filter_text + \
                '--format "{{.Names}}    {{.Status}}    {{.Image}}"'
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    print('Containers: ')
    for line in output.stdout.splitlines():
        print('\t' + line.decode())


if __name__ == '__main__':
    list_(sys.argv[1:])

