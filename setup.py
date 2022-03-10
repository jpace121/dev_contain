from setuptools import setup
import subprocess
import sys
import os

package_name='dev_contain'
semver = '7.1.0'

setup_file_path = os.path.dirname(os.path.abspath(__file__))

if sys.version_info < (3,):
    print('dev_contain only supports Python 3.')
    sys.exit(1)

def set_version_file():
    # Get git version if we can.
    git_version = ''
    try:
        check_result = subprocess.Popen(['git', 'describe', '--no-match', '--always', '--dirty'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        git_version = check_result.stdout.read().decode('ascii').strip()
    except:
        pass

    # Save git version and version variable to a file.
    with open(os.path.join(setup_file_path, package_name, 'version.yaml'), 'w+') as f:
        f.write('semver: {}\n'.format(semver))
        if git_version:
            f.write('hash: {}\n'.format(git_version))

set_version_file()

setup(name='dev_contain',
      version=semver,
      description='CLI script to build and use containers for development leveraging podman or docker.',
      author='James Pace',
      author_email='jpace121@gmail.com',
      url='dev_contain.local',
      license='Apache 2.0',
      packages=[package_name],
      setup_requires=['wheel'],
      install_requires=['jinja2', 'pyyaml'],
      package_data={
        '': ['version.yaml'],
      },
      entry_points = {
        'console_scripts': ['dev_contain=dev_contain.dev_contain:main'],
      },
      zip_safe=False)
