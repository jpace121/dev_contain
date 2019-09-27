#!/usr/bin/env python3
import os
import argparse
import subprocess
import tempfile
import jinja2

def main():
    parser = argparse.ArgumentParser(description='Build a base development image from a pre-existing image.')
    parser.add_argument('--base_image', '-f', default='ubuntu:18.04' , help='Base image to start from.')
    parser.add_argument('--image_name', '-n', default='jwp-build-latest', help='Name for the final image.')
    parser.add_argument('--template_dir', '-d', default='./templates', help='Directory containing the base template.')
    parser.add_argument('--template', '-t', default='base.sh.template', help='Template to expand.')
    parser.add_argument('--dry_run', '-r', action='store_true', help='Print templated script, but do not run it.')
    args = parser.parse_args()
 
    # Copy arguments to temp variables for consistency.
    base_image = args.base_image
    image_name = args.image_name
    template_dir = args.template_dir
    template = args.template

    # Load templates.
    env = jinja2.Environment(
        autoescape=False,
        loader=jinja2.FileSystemLoader(template_dir)
    )
    # Find and render the base template.
    template = env.get_template(template)
    res = template.render(base_image=base_image, image_name=image_name)
    # Run the resulting script.
    if args.dry_run:
        print(res)
    else:
        subprocess.run(res, shell=True)

if __name__ == '__main__':
    main()
