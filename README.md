# Miner Tool Guide

## Features:

This miner tool listens to the tasks that come from Swan platform. It provides the following functions:

* Download tasks automatically using Aria2 for downloading service.
* Import deals once download tasks completed.
* Synchronize deal status with Swan platform so that client will know the status changes in realtime.

## Prerequisite
- Lotus-miner
- python 3.7+
- pip3

## Config
### **In aria2.conf**
- **rpc-secret:**  default: my_aria2_secret. It will be used in the config.toml for rpc.

### **In aria2c.service**
```shell
[Unit]
Description=Aria2c download manager
After=network.target

[Service]
Type=simple
User=user
Group=user
ExecStart=/usr/bin/aria2c --enable-rpc --rpc-listen-all --conf-path=/etc/aria2/aria2.conf

[Install]
WantedBy=multi-user.target
```
[Service]
- **User**: Change it with the user of server where the miner located
- **Group**: Change it with the group of server where the miner located

### **In config.toml**

Modify config file in folder `swan-provider/config` with the information of the miner, such as filecoin miner id, api key and access token.
```shell
[main]
api_url = "https://api.filswan.com"
miner_fid = "f0xxxx"
expected_sealing_time = 1920    # 1920 epoch or 16 hours
import_interval = 600           # 600 seconds or 10 minutes
scan_interval = 600           # 600 seconds or 10 minutes
api_key = ""
access_token = ""
[aria2]
aria2_download_dir = "/path/to/download/"
aria2_conf = "/etc/aria2/aria2.conf"
aria2_host = "localhost"
aria2_port = "6800"
aria2_secret = "my_aria2_secret"
```
[main]

- **api_url:** Swan API address. For Swan production, it is "https://api.filswan.com"
- **miner_fid:** Your filecoin Miner ID
- **expected_sealing_time:** The time expected for sealing deals. Deals starting too soon will be rejected.
- **import_interval:** Importing interval between each deal.
- **scan_interval:** Time interval to scan all the ongoing deals and update status on Swan platform.
- **api_key & access_token:** Acquire from [Filswan](https://www.filswan.com) -> "My Profile"->"Developer Settings". You
  can also check the [Guide](https://nebulaai.medium.com/how-to-use-api-key-in-swan-a2ebdb005aa4)

[aria2]

- **aria2_download_dir:** Directory where offline deal files will be downloaded for importing
- **aria2_conf:** Aria2 configuration file location
- **aria2_host:** Aria2 server address
- **aria2_port:** Aria2 server port
- **aria2_secret:** Must be the same value as rpc-secre in aria2.conf


## Installation

Install miner tool and aria2
```shell
sudo apt install python3-pip
sudo apt install aria2
```

## How to use

### Step 1. Run Aria2 as System Service

#### Step 1.1 Set up Aria2:

```shell
sudo mkdir /etc/aria2
# Change user authority to current user
sudo chown $USER:$USER /etc/aria2/
# Create a session file
touch /etc/aria2/aria2.session
# Checkout the source and install 
git clone https://github.com/filswan/swan-provider

cd swan-provider

# Copy config file and service file
cp config/aria2.conf /etc/aria2/
sudo cp aria2c.service /etc/systemd/system/
# Modify the aria2c.service file in /etc/systemd/system/

# Set to start Aria2 automatically
sudo systemctl enable aria2c.service
# Start Aria2
sudo systemctl start aria2c.service
```
If modify user is nessecary while the service has been started, service should be reloaded before start.
```shell
sudo systemctl daemon-reload
sudo systemctl start aria2c.service
```


#### Step 1.2 Test Aria2 service from log (Optional)

Check if Aria2 service is successfullly started

```shell
journalctl -u aria2c.service -f
```
The output will be like:

```shell
Jul 30 03:00:00 systemd[1]: Started Aria2c download manager.
Jul 30 03:00:00 aria2c[2433312]: 07/30 03:00:00 [NOTICE] IPv4 RPC: listening on TCP port 6800
```

The Aira2 service will listen on certain port if installed and started correctly.

### Step 2. Start Swan Provider
```shell
cd swan-provider

# Install requirements
pip3 install -r requirements.txt

# Modify config.toml file with the miner information

# Run Swan Provider directly, or
python3 swan_miner.py

# Run Swan Provider in the background, and create a log file (Optional)
nohup python3 -u swan_miner.py > swan_miner.log &
```

The deal status will be synchronized on the filwan.com, both client and miner will know the status changes in realtime.
