# Miner Tool Guide

## Features:

This miner tool listens to the tasks come from Swan platform. It provides the following functions:

* Download tasks automatically using Aria2 for downloading service.
* Import deals once download tasks completed.
* Synchronize deal status with Swan platform so that client will know the status changes in realtime.

## Step 1. Getting Started
### Step 1.1 Prerequisites

```shell
sudo apt install python3-pip
sudo apt install aria2
```

### Step 1.2 Run Aria2 as System Service

Set up Aria2:

```shell
sudo mkdir /etc/aria2
sudo chown $USER:$USER /etc/aria2/
touch /etc/aria2/aria2.session
git clone https://github.com/filswan/swan-miner
cd swan-miner
# copy config files to aria2
cp config/aria2.conf /etc/aria2/
sudo cp aria2c.service /etc/systemd/system/
```

Modify aria2c.service file: 

```shell
# Change User and Group in the [Service] section of the aria2c.service file in /etc/systemd/system/
# with the name of the server/computer where the miner located, such as mycomputer
sudo systemctl enable aria2c.service
sudo systemctl start aria2c.service
```

For aria2.conf,

- **rpc-secret:**  default: my_aria2_secret. It will be used in the config.toml for rpc.

### Step 1.3 Test Aria2 service from log
```shell
journalctl -u aria2c.service -f
```
The Aira2 service will listen on certain port if installed and started correctly.

## Step 2. Start swan_miner
### Step 2.1 Modify config file with the miner information

Modify congfig.toml file in folder swan-miner with the information of the miner, such as filecoin miner id, api key and access token.

For config.toml,

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

### Step 2.2 run swan-miner
```shell
cd swan-miner
python3 swan_miner.py
```

#### Now you are all set. Enjoy using swan miner!
