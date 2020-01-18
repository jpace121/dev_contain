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
from dev_contain.build import build
from dev_contain.start import start
from dev_contain.list import list_
from dev_contain.attach import attach
from dev_contain.clean import clean
from dev_contain.stop import stop
from dev_contain.version import version

def main():
    parser = argparse.ArgumentParser(description='Build and run containers for development.')
    parser.add_argument('command', choices=['start', 'build', 'list', 'attach', 'clean', 'stop', 'version'], help='Subcommand to run.')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments to pass to the subcommand.')
    args = parser.parse_args()

    if args.command == 'build':
        build(args.args)
    if args.command == 'start':
        start(args.args)
    if args.command == 'stop':
        stop(args.args)
    if args.command == 'list':
        list_(args.args)
    if args.command == 'attach':
        attach(args.args)
    if args.command == 'clean':
        clean(args.args)
    if args.command == 'version':
        version()

if __name__ == '__main__':
    main()
