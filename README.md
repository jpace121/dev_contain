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

To use `podman build` to build containers, set `DEV_CONTAINER_BUILDER` to
`podman`.

## Install Package
```bash
pip3 install --user .
export PATH="~/.local/bin:$PATH"
```

## Packaging
Always fix issues and modify the version number in the setup.py file before
merging to master.

### Debian
1. Merge master to packaging.
2. Modify change log by copying and pasting the last entry.
   Add and commit the change log.
3. Install ansible:
   `sudo apt install ansible`
3. Build and release: `ansible-playbook ./build.yaml -i inventory.yaml`
   or just build: `ansible-playbook ./build.yaml -i inventory.yaml --skip-tags "deploy"`
### Fedora
Requires `rpmbuild`/`fedora-packager`.

`dnf install rpm-build fedora-packager python3-devel`
On CentOS8:
`pip3 install --upgrade --user setuptools wheel`

1. Merge master to packaging/fedora.
2. Update version number in spec file in the rpm directory.
3. Run `rpm/build.bash`.
4. Grab rpm from `/tmp/rpm/RPMS`.
