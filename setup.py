from setuptools import setup

setup(name='dev_contain',
      version='0.0.0',
      description='CLI script to build and use containers for development leveraging podman.',
      author='James Pace',
      author_email='jpace121@gmail.com',
      url='dev_contain.local',
      license='Apache 2.0',
      packages=['dev_contain'],
      install_requires=['jinja2'],
      entry_points = {
        'console_scripts': ['dev_contain=dev_contain.dev_contain:main'],
      },
      zip_safe=False)
