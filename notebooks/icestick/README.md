# Icestick examples
Tested on MacOS 10.12.6 with Homebrew and Ubuntu 14.04.
## Dependencies
### MacOS
```
brew install python3
```

### Ubuntu
```
sudo apt-get install python3 python3-pip
```

## Installing Icestorm tools, arachne-pnr, and yosys
```
python3 install.py --num_cores 4
```

# Vagrant Virtual Machine

## Dependencies
Install vagrant: [https://www.vagrantup.com/downloads.html](https://www.vagrantup.com/downloads.html).

### MacOS
```
brew cask install virtualbox vagrant
```

### Ubuntu
```
sudo apt-get install virtualbox vagrant
```

## Running the VM
```
vagrant up       # Bring the VM online (will provision using the install.py)
vagrant ssh      # SSH into the VM
```

```
vagrant destroy  # Terminate the VM
```
