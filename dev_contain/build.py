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
import os
import sys
import argparse
import subprocess
import tempfile
import jinja2

def build(in_args):
    parser = argparse.ArgumentParser(prog='build', description='Build a base development image from a pre-existing image.')
    parser.add_argument('--base_image', help='Base image to start from.')
    parser.add_argument('--image_name', help='Name for the final image.')
    parser.add_argument('--template_dir', help='Directory containing the base template.')
    parser.add_argument('--template', help='Template to expand.')
    parser.add_argument('--user', help='Username for user to add to container.')
    parser.add_argument('--user_id', help='User id to add for user in container.')
    parser.add_argument('--debug', action='store_true', help='Print templated script, but do not run it.')
    parser.add_argument('--docker', action='store_true', help='Export image to location that can be be found by Docker.')
    args = parser.parse_args(in_args)
 
    base_image = args.base_image
    if not base_image:
        base_image = 'ubuntu:18.04'
    image_name = args.image_name
    if not image_name:
        image_name = 'jwp-build-latest'
    template_dir = args.template_dir
    if not template_dir:
        template_dir = './templates'
    template = args.template
    if not template:
        template = 'base.sh.template'
    save_docker = args.docker
    if not save_docker:
        save_docker = False
    username = args.user
    if not username:
        username = os.getlogin()
    user_id = args.user_id
    if not user_id:
        user_id = os.getuid()
    

    # Load templates.
    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
        loader=jinja2.FileSystemLoader(template_dir)
    )
    # Find and render the base template.
    template = env.get_template(template)
    res = template.render(base_image=base_image,
                          image_name=image_name,
                          save_docker=save_docker,
                          username=username,
                          user_id=user_id)
    
    # Run the resulting script.
    if args.debug:
        print(res)
    else:
        subprocess.run(res, shell=True)

if __name__ == '__main__':
    build(sys.argv[1:])
