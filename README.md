

## Install docker
https://docs.docker.com/install/linux/docker-ce/ubuntu/
```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable"
sudo apt install docker-ce docker-ce-cli containerd.io -y
```

## Install docker-compose
https://docs.docker.com/compose/install/
https://github.com/docker/compose/releases/latest
```bash
curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

## Clone repo
```bash
git clone https://github.com/LizaMetla/placex
cd placex
git checkout develop

```
## Create .secret.env file in root
```bash
SECRET_KEY=<YOU TOKEN>
BOT_TOKEN=<BOT TOKEN FROM BOTFATHER>
DJANGO_SETTINGS_MODULE=placex.settings
IS_PRODUCTION=false
```
## Build and run
```bash
docker-compose build
docker-compose up -d
```
