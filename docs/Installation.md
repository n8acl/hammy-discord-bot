# Installation/Setup

### Installation Steps
1) Obtain API Keys/Logins
2) Clone Repo
3) Configure the Bot
4) Run the Bot

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi. (Mine is running on a Raspberry Pi 4 2 GB model with many other bots and scripts running with no issues.)

If you want to run this on a Windows or Mac machine, you will need to install Python3 and be familiar installing from a requirements.txt.

--- 

### Obtain API Keys

First you will need to obtain some API Keys and Logins for this to work. Please see the Obtaining API Keys guide and then come back here.

---

### Clone Repo

Next you will need to clone the repo. Use the following:

```bash
git clone https://github.com/n8acl/hammy-discord-bot.git
cd hammy-discord-bot
```

---

### Configuring the Script

Now we will need to configure the settings for the Bot. You will need to open the ```config.json``` file in the ```hammy-discord-bot``` directory in your editor of choice. Make sure you are in the correct Directory.

In the file you will see the following:

```json
{
    "discord_bot_token": "DISCORD BOT TOKEN HERE",
    "discord_server_id": "DISCORD SERVER ID HERE",
    "hamqth_username": "HAMQTH USERNAME HERE",
    "hamqth_password": "HAMQTH PASSWORD HERE",
    "aprsfikey":"APRS.FI API KEY HERE"
}
```

Please put the corresponding Keys into the correct fields. All fields are needed for the script to work.

---

### Running the bot

There are two methods that can be used to run the bot.
* Docker (Preferred)
* Screen Session

#### Run using Screen Session Method

To use this method, you will need to install the needed packages, cloning the repo to get the script and then installing the needed libraries for the script to work properly all by hand.

Before running the following commands, please make sure you are in the ```hammy-discord-bot``` directory that was cloned above and that you have already updated the ```config.json``` file:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

pip3 install -r requirements.txt

screen -R hammy-discord-bot

python3 hammy-discord-bot.py
```

The Bot will start running and should show up in your server. You can then press ```Ctrl+A+D``` to disconnect from the screen session to allow the bot to run on it's own. If the box that you are running this on ever needs a reboot, you will need to restart the screen session again.

#### Running the bot using the Docker Method (Preferred)

The bot can also be run in Docker. This is the preferred method. The bot can be run in 2 different ways with Docker. You can build the container yourself, or you can use a pre-built container from Docker hub.

To use the Docker container, you will need to have Docker and Docker-Compose installed and configured properly. There are plenty of Guides online to accomplish this and support of that is outside the scope of this project/document.

**Prebuilt Container on DockerHub**

To use the prebuilt container, set the keys in the ```config.json``` file and then use the ```docker-compose.yaml``` file provided in the repo.

Make sure to check the yaml file first and set the path to where your ```config.json``` file is. 

Then just use:

```bash
docker-compose pull
docker-compose up -d
```

to pull and start the container. The bot should start and connect and show up in your server.

**Building the Container**

To build the container, set the keys in the ```config.json``` file and then use the ```docker-compose.yaml``` file provided in the repo.

Make sure to check the yaml file first and change the image line from:

```yaml
image: n8acl/hammy_bot:latest
```

to

```yaml
build: .
```

Also make sure to set the full path to where your ```config.json``` file is. 

Then use:

```bash
docker-compose build
docker-compose up -d
```

to build and Start the container. The bot should start and show up in your server.