# jpace121 Development Containers

A series of scripts I built so I can develop, build, and test code in
containers.

Note that this is a HUGE experiment still, don't actually depend on these
for anything.

License (unless otherwise noted): Apache-2.0

## Install Dependencies

### Podman and buildah

Ubuntu 18.04:
```bash
sudo apt-get update 
sudo apt-get install software-properties-common uidmap slirp4netns runc
sudo add-apt-repository ppa:projectatomic/ppa
sudo apt-get update 

sudo apt-get install buildah
sudo apt-get install podman

echo -e "[registries.search]\nregistries = ['docker.io', 'quay.io']" | sudo tee /etc/containers/registries.conf
```

On Ubuntu 16.04 I've ran into problems using podman and buildah, but only for
certain images (after I changed the storage settings to use overlayfs, with
vfs I had lots of permission issues...)

### Docker
If desired, docker can be used instead.

Ubuntu 18.04:
```bash
sudo apt install docker.io
sudo groupadd docker
```

Instead of adding myself to the docker group, I've been adding myself
temporarily with, though they're are gotchas with this.
```bash
sudo -i -g docker
```
For  `dev_contain` to use `Docker`, set the environment variables
`DEV_CONTAIN_BUILDER` and `DEV_CONTAIN_MANAGER` to `docker`.

## Install Package
```bash
python3 setup.py install --user
export PATH="~/.local/bin:$PATH"
```
