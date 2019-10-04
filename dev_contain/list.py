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

def list_(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' list', description='List known containers.')
    args = parser.parse_args(in_args)
    command = 'podman images '\
                '--sort repository '\
                '--filter dangling=false '\
                '--format "{{.Repository}}"'

    output = subprocess.run(command, shell=True, capture_output=True)
    all_images = output.stdout.splitlines()
    local_images = [x for x in all_images if b'jwp' in x]
    for image in local_images:
        print(image.decode())

if __name__ == '__main__':
    list_(sys.argv[1:])
    
