import argparse
from build import build
from run import run
import sys

def main():
    parser = argparse.ArgumentParser(description='Build and run containers for development.')
    parser.add_argument('command', help='Subcommand to run.')
    args = parser.parse_args(sys.argv[1:2])

    if args.command == 'build':
        build(sys.argv[2:])
    if args.command == 'run':
        run(sys.argv[2:])

if __name__ == '__main__':
    main()
