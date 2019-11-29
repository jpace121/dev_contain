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
import jinja2
import shlex
import yaml

def build(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' build', description='Build a base development image from a pre-existing image.')
    parser.add_argument('--template_dir', help='Directory containing the base templates.')
    parser.add_argument('--print', action='store_true', help='Print result of applying template. Do not run build command.')
    parser.add_argument('--docker', action='store_true', help='Build with docker, not buildah. (Only works for Dockerfile templates.)')
    parser.add_argument('config_file', help='Path to yaml file with appropriate variables.')
    args = parser.parse_args(in_args)
        
    # Grab values from config file.
    if not os.path.exists(args.config_file):
        print('Provided config file ({}) does not exist.'.format(args.config_file))
        return -1

    config = {}
    try:
        with open(args.config_file, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
    except yaml.YAMLError as err:
        print('Failed to parse config file.')
        if hasattr(err, 'problem_mark'):
            print('Error Position: {} {}'.format(err.problem_mark.line+1, err.problem_mark.column+1))
        return -1
     
    # Set promised values if not set in file.
    if not config.get('template'):
        config['template'] = 'base.sh.template'
    if not config.get('username'):
        config['username'] = os.getlogin()
    if not config.get('user_id'):
        config['user_id'] = os.getuid()
    if not config.get('base_image'):
        config['base_image'] = 'jwp_build_latest'
    if not config.get('save_docker'):
        config['save_docker'] = False
    if not config.get('image_name'):
        config['image_name'] = 'dev_contain'
        
    # Find template directory.
    template_dir = args.template_dir
    if not template_dir:
        template_dir = './templates'

    # Load templates.
    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
        loader=jinja2.FileSystemLoader(template_dir)
    )
    # Find and render the base template.
    template = env.get_template(config['template'])
    res = template.render(config)
    
    # Run the resulting script.
    if args.print:
        print(res)
    else:
        if '.bash' in config['template'] or '.sh' in config['template']:
            subprocess.run(res, shell=True)
        elif 'Dockerfile' in config['template']:
            if args.docker:
                cmd = 'docker build -t {} -f - .'.format(config['image_name'])
            else:
                cmd = 'buildah bud -t {} --layers -f - .'.format(config['image_name'])
                
            process = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE)
            process.communicate(res.encode())
        else:
            print("Not sure how to run template file. File name should contain '.sh', '.bash', or 'Dockerfile'.")
            return -1
            

if __name__ == '__main__':
    build(sys.argv[1:])
