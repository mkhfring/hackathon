# English class
A bale bot to simulate an English class room
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
mkvirtualenv --python=$(which python3.6) --no-site-packages enlish_class
```
Clone the project with the following link:
```
https://github.com/mkhfring/hackathon.git
```

Then create a virtual enviroment and try the following commands:
```
pip install -e .
pip install -r requirements.txt
```

## Prerequisites
Requirements for this project is listed in the requirments.txt file and will be install using the following command:

```
pip install -r requirements.txt
```

## Deploy
create a docker-compose file like below:
```
version: '3.4'
services:
  vip_report_bot:
    image: 
    volumes:
      - /home/enbot:/home/enbot
    container_name: 
    environment:
      - PROVIDER_TOKEN=
      - BOT_TOKEN=
      - AMOUNT=
      
     
```

Then run docker-compose up -d
