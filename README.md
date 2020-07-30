nukxScan
===
An application for demonstrating mMTC scenario

## Requirements

- Server
    - Nodejs
    - Express ~4.16.1
    - MongoDB
    - Mongoose ^5.9.26

- Client
    - Python3
    - pywifi==1.1.12
    - requests==2.24.0

## Installation

Server
```bash
sudo apt install -y nodejs npm mongodb
git clone https://github.com/Nukicslab/nukxScan.git
cd nukxScan/server
sudo npm install
```

Client
```bash
sudo apt install -y python-is-python3 pyhton3-pip
git clone https://github.com/Nukicslab/nukxScan.git
cd nukxScan/rpi_client
sudo pip3 install -r requirements.txt
```

## Usage

Client
```bash
cd nukxScan/rpi_client
sudo python3 rpi_client.py 
```

Server
```bash
cd nukxScan/server
npm start
```

## Licsnse
Copyright 2020 Inform System Lab.
