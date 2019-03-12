# hackathon
VIP admin is a bot that would handle the account officer administrative requirements. This requirements would include getting account officer's repors, adding new account officer, searching for vip customers, to name but some.

## Getting Started
### Enviroment setup
First install requirments and create a virtual environment for the project using codes below:
```
sudo apt-get install python3-pip python3-dev
sudo pip3.6 install virtualenvwrapper
echo "export VIRTUALENVWRAPPER_PYTHON=`which python3.6`" >> ~/.bashrc
echo "alias v.activate=\"source $(which virtualenvwrapper.sh)\"" >> ~/.bashrc
source ~/.bashrc
v.activate
mkvirtualenv --python=$(which python3.6) --no-site-packages vip_dmin
```
Clone the project with the following link:

ssh://git@bitbucket.voroodi.ir:7999/bank/vip_admin.git

Then create a virtual enviroment and try the following commands:
```
pip install -e .
pip install -r requirements.txt
```
## Prerequisites
This project needs a connection to the account officer database. Other requirements for the project are listed in requirements.txt

## Deploy
create a docker-compose file like below:
```
version: '3.4'
services:
  vip_report_bot:
    image: "docker.bale.ai/bank/vip_admin:0.1-1"
    volumes:
      - /home/vipbot:/home/vipbot
    container_name: "vip_admin_practice"
    environment:
      - BOT_TOKEN=
      - supported_users=
      - DB_HOSTNAME=
      - DB_USERNAE=
      - DB_PASSWORD=
      - DB_PORT=
      - DB_NAME=
```

Then run docker-compose up -d
