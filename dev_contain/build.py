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
import yaml

def build(in_args):
    parser = argparse.ArgumentParser(prog=sys.argv[0]+' build', description='Build a base development image from a pre-existing image.')
    parser.add_argument('--template_dir', help='Directory containing the base templates.')
    parser.add_argument('--debug', action='store_true', help='Print templated script, but do not run it.')
    parser.add_argument('config_file', help='Path to yaml file with appropriate variables.')
    args = parser.parse_args(in_args)
        
    # Grab values from config file.
    if not os.path.exists(args.config):
        print('Provided config file ({}) does not exist.'.format(args.config))
        return -1

    config = {}
    try:
        with open(args.config, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
    except yaml.yamlError as err:
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
    if args.debug:
        print(res)
    else:
        subprocess.run(res, shell=True)

if __name__ == '__main__':
    build(sys.argv[1:])
