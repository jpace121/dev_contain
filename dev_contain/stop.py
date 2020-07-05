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

def stop(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' stop', description='Stop and remove a running container.')
    parser.add_argument('container', help='Name of the container to stop.', nargs='?')
    args = parser.parse_args(in_args)

    container = 'dev'
    if args.container:
        container = args.container

    manager = common.get_manager()

    # Is container running?
    check_command = manager + ' inspect ' + container  +' -f "{{ .State.Running }}"'
    check_result = subprocess.Popen(shlex.split(check_command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    is_running = check_result.stdout.read().decode('ascii').strip() == 'true'
    # If so stop it.
    if(is_running):
        stop_command = '{manager} stop {container}'.format(manager=manager,
                                                           container=container)
        print('Stopping container: {}'.format(stop_command))
        subprocess.run(stop_command, shell=True)
    # rm container.
    remove_command = '{manager} rm {container}'.format(manager=manager,
                                                       container=container)
    print('Removing container: {}'.format(remove_command))
    subprocess.run(remove_command, shell=True)

if __name__ == '__main__':
    stop(sys.argv[1:])
