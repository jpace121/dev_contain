#
# Copyright 2022 James Pace
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
import functools
import sys
import subprocess
from pathlib import Path
import shutil
import json5
import dev_contain.common as common

def vs(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' vs', description='Support for interacting with devcontainer containers.')
    parser.add_argument('command', choices=['start', 'stop', 'exec', 'hotfix'], help='Subcommand to run.')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments to pass to the subcommand.')
    args = parser.parse_args(in_args)

    if not is_dev_container_installed():
        print('Could not find devcontainer. Please install it with:')
        print('\t sudo npm install -g @devcontainers/cli')
        return

    workspace_dir = find_workspace_folder()
    if not workspace_dir:
        print('Could not find workspace folder. Looked in $PWD for .devcontainer.')
        return

    manager = common.get_manager()

    if args.command == "hotfix":
        hotfix(manager, workspace_dir)
    if args.command == "start":
        start(manager, workspace_dir)
    if args.command == "exec":
        exec_(manager, workspace_dir, args.args)
    if args.command == "stop":
        stop(manager, workspace_dir)

def stop(manager, workspace_dir):
    filter_text = '--filter label=devcontainer.local_folder="{}"'.format(workspace_dir)
    command = manager + ' ps -a '\
        + filter_text + \
        ' --format "{{.Names}}"'
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    containers = output.stdout.splitlines()

    if len(containers) < 1:
        print("Found no containers to stop.")

    for container in containers:
        command = '{manager} stop {container} && {manager} rm {container}'.format(
            manager=manager,
            container=container.decode('utf-8'))
        print('Running: "{}"'.format(command))
        subprocess.run(command, shell=True)

def exec_(manager, workspace_dir, args):
    manager_path = shutil.which(manager)
    if not manager_path:
        print("Could not find manager. Bailing.")
        return
    # Merge the args elements into a string.
    args_string = functools.reduce(lambda list_, elem_: str(list_) + ' ' + str(elem_), args)
    command = 'devcontainer exec --workspace-folder {} --docker-path "{}" {}'.format(
        workspace_dir.resolve(), manager_path, args_string)
    print('Running: {}'.format(command))
    subprocess.run(command, shell=True)

def start(manager, workspace_dir):
    manager_path = shutil.which(manager)
    if not manager_path:
        print("Could not find manager. Bailing.")
        return
    command = 'devcontainer up --workspace-folder {} --docker-path "{}"'.format(
        workspace_dir.resolve(), manager_path)
    print('Running: {}'.format(command))
    subprocess.run(command, shell=True)

def hotfix(manager, workspace_dir):
    # Podman needs to run the container with --userns=keepid.
    # If we're using podman, modify the devcontainer.json file.
    if manager != 'podman':
        return
    json_file = workspace_dir / '.devcontainer' / 'devcontainer.json'
    if not json_file.exists():
        print('Can not find json file.')
        return
    json_in = []
    with open(json_file.resolve(), 'r') as f:
        json_in = json5.load(f)
    if u'runArgs' in json_in.keys():
        if not '--userns=keep-id' in json_in[u'runArgs']:
            json_in[u'runArgs'].append('--userns=keep-id')
    else:
        json_in[u'runArgs'] = ['--userns=keep-id']

    with open(json_file.resolve(), 'w') as f:
        json5.dump(json_in, f, indent=4, quote_keys=True)


def find_workspace_folder():
    # For now, I'm assuming that we want $PWD.
    current_dir = Path.cwd()
    desired_dir = current_dir / '.devcontainer'
    if desired_dir.exists():
        return current_dir
    else:
        return None

def is_dev_container_installed():
    path = shutil.which("devcontainer")
    if not path:
        return False
    else:
        return True

if __name__ == '__main__':
    vs(sys.argv[1:])

