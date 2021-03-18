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
Install deps:
```bash
sudo apt install \
    python3-pip \
    python3-setuptools \
    build-essential \
    fakeroot \
    devscripts \
    debhelper \
    dh-python
```

1. Merge master to packaging/debian
2. Modify change log.
```
   dch --newversion <version>-1
```
Hand edit changelog from the template.
Add and commit change log.
3. Build:
```
  debian/build.bash
```
4. Built files will be put in `/tmp/dev_contain_build`.

### Fedora
`sudo dnf install rpm-build pyhton3-devel`

`dnf install rpm-build fedora-packager python3-devel`
On CentOS8:
`pip3 install --upgrade --user setuptools wheel`

1. Merge master to packaging/fedora.
2. Update version number in spec file in the rpm directory.
3. Run `rpm/build.bash`.
4. Grab rpm from `/tmp/rpm/RPMS`.
