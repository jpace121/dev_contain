#!/usr/bin/env python3
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
import shlex
import dev_contain.common as common


def attach(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' attach', description='Attach to a running container using podman.')
    parser.add_argument('container', help='Name of the container to attach to.', nargs='?')
    parser.add_argument('--command', '-c', help='Command if not default in image to run instead of attaching.')
    args = parser.parse_args(in_args)

    manager = common.get_manager()

    container = 'dev'
    if args.container:
        container = args.container
    
    command = 'eval ${DEV_CONTAIN_ATTACH_CMD:-bash}'
    if args.command:
        command = args.command

    check_command = manager + ' inspect ' + container  +' -f "{{ .State.Running }}"'
    check_result = subprocess.Popen(shlex.split(check_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    is_running = check_result.stdout.read().decode('ascii').strip() == 'true'

    if is_running:
        podman_command = ('{manager} exec -i -t'
                        ' {container}'
                        ' bash -c \'{command}\'').format(
                            manager=manager,
                            container=container,
                            command=command)
        print('Running: {}'.format(podman_command))
        subprocess.run(podman_command, shell=True)
    else:
        print('Container {} is not started. Please create or start it.'.format(container))

if __name__ == '__main__':
    attach(sys.argv[1:])
