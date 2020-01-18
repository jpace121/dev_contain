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
    args = parser.parse_args(in_args)

    builder = common.get_builder()
    manager = common.get_manager()

    if builder == 'buildah':
        run_and_log('Removing buildah containers.', 'buildah rm --all')
        run_and_log('Pruning buildah images.', 'buildah rmi --prune')
    if builder == 'docker':
        run_and_log('Pruning dangling images.', 'docker image prune')

def run_and_log(comment, command):
    print(comment)
    print('Running: {}'.format(command))
    subprocess.run(command, shell=True)

if __name__ == '__main__':
    clean(sys.argv[1:])
