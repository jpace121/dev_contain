# jpace121 Development Containers

A series of scripts I built so I can develop, build, and test code in
containers.

Note that this is a HUGE experiment still, don't actually depend on these
for anything.

License (unless otherwise noted): Apache-2.0

## Install Dependencies

Ubuntu 18.04:
```bash
sudo apt-get update 
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:projectatomic/ppa
sudo apt-get update 

sudo apt-get install buildah
sudo apt-get install podman
```

Note buildah and podman don't seem to work on 16.04.

## Install Package
```bash
python3 setup.py install --user
export PATH="~/.local/bin:$PATH"
```
