# jpace121 Development Containers

A series of scripts I built so I can use containers as my primary development
environment.

License: Apache-2.0

Templates for building compliant containers are located in
[this sister repository](https://github.com/jpace121/dev_contain_templates).

## Install Dependencies

By default, `dev_contain` tries to call
[buildah](https://github.com/containers/buildah) and
[podman](https://github.com/containers/libpod) to build and run containers.

For  `dev_contain` to use docker instead, set the environment variables
`DEV_CONTAIN_BUILDER` and `DEV_CONTAIN_MANAGER` to `docker`.

## Install Package
```bash
pip3 install --user .
export PATH="~/.local/bin:$PATH"
```

## Packaging
Always fix issues and modify the version number in the setup.py file before
merging to master.

### Debian
1. Merge master to packaging/debian
2. Modify change log.
3. Build:
```
   gbp buildpackage -us -uc
```
