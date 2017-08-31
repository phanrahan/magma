# Icestick examples
We provide a instructions for setting up a local development environment, as
well as a [Vagrant](https://www.vagrantup.com/) virtual machine.

* [Local](https://github.com/phanrahan/magma/tree/master/notebooks/icestick#local)
* [Vagrant VM](https://github.com/phanrahan/magma/tree/master/notebooks/icestick#vagrant-virtual-machine)

## Local
Tested on MacOS 10.12.6 with Homebrew and Ubuntu 14.04.
### MacOS
```
brew install python3
python3 install.py
```

### Ubuntu
```
sudo apt-get install python3 python3-pip
sudo python3 install.py
```

## Vagrant Virtual Machine

### Dependencies
Install vagrant:
[https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html)

#### MacOS
```
brew cask install virtualbox vagrant
```

#### Ubuntu
```
sudo apt-get install virtualbox vagrant
```

### Running the VM
```
vagrant up       # Bring the VM online (will provision using the install.py)
vagrant ssh      # SSH into the VM
```

```
vagrant destroy  # Terminate the VM
```
