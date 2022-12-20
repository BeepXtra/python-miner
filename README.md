# python-miner
___
## Setup instructions

### Summary
1. Linux OS setup
2. Windows OS setup
___

### 1. Linux OS Setup
#### Step 1: Download and install SMiner
* Open your terminal (If you have a desktop linux system. If you are running server edition, skip this step)
* Copy and paste the following and hit enter:
```
sudo mkdir /home/sminer && cd /home/sminer && sudo git clone https://github.com/BeepXtra/python-miner.git && cd python-miner/ && sudo python3 -m venv venv && source venv/bin/activate
```
#### Step 2: Prepare your miner
* Edit the config.txt file and replace [VALUES] with your own wallet details and save it
* Copy paste the following command in terminal and hit enter
```
sudo pip install -r requirements.txt
```

#### Step 3: Start your miner
* To start the miner, run this command in terminal:
```
python3 /home/sminer/main.py
```

_Note! Before your start your miner, check that you have the correct venv active.

#### Step 4: (Optional) Auto-start miner on boot
* Edit your cronjobs
```
crontab -e
```
* Add the following lines to the crontab and save it
```
@reboot cd /home/sminer/python-miner/
@reboot source venv/bin/activate
@reboot python3 main.py
```
___

### 2. Windows OS Setup

#### STAY TUNED
___
