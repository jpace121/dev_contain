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

def clean(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' clean', description='Prune system of uneeded containers and images.')
    parser.add_argument('--buildah', '-b', action='store_true', help='Cleanup after buildah.')
    parser.add_argument('--container', '-c', help='Stop and remove a running container.')
    args = parser.parse_args(in_args)

    builder = common.get_builder()
    manager = common.get_manager()

    if(args.buildah):
        if builder == 'buildah':
            run_and_log('Removing buildah containers.', 'buildah rm --all')
            run_and_log('Pruning buildah images.', 'buildah rmi --prune')
        else:
            print('Builder is {}. I only know how to clean up for buildah.'.format(builder))
    if(args.container):
        # Is container running?
        check_command = manager + ' inspect ' + args.container  +' -f "{{ .State.Running }}"'
        check_result = subprocess.Popen(shlex.split(check_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        is_running = check_result.stdout.read().decode('ascii').strip() == 'true'
        # If so stop it.
        if(is_running):
            stop_command = '{manager} stop {container}'.format(manager=manager,
                                                               container=args.container)
            run_and_log('Stopping container.', stop_command)
        # rm container.
        remove_command = '{manager} rm {container}'.format(manager=manager,
                                                           container=args.container)
        run_and_log('Stopping container.', remove_command)

def run_and_log(comment, command):
    print(comment)
    print('Running: {}'.format(command))
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    clean(sys.argv[1:])
