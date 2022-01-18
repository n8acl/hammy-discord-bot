# Hammy, a Ham Radio Discord Bot
Python based Ham Radio Callsign/APRS Discord lookup bot.

---
# Description

This is a Python based, self-hosted, Ham Radio Discord bot that can be added to Ham Radio Discord Servers to allow for Callbook data lookup as well as APRS position packet data. Note that currently this only pulls Callbook data for the United States.

Note that this software is intended for use by Amateur Radio Operators only.

## API's Used

This bot pulls data from the following locations:

| Service | Description | Website |
|---------|---------|---------|
|Callook.info|Used for Call Book data lookup|[https://callook.info/](https://callook.info/)|
|HamQTH.com|Used for Call book data lookup for callsigns not found at callook.info|[https://www.hamqth.com](https://www.hamqth.com)
|APRS.FI|Used for APRS Data lookip|[https://aprs.fi](https://aprs.fi)|
|Radioid.net|Used for DMR/NXDN ID Lookups|[https://radioid.net](https://radioid.net)|

---

# Installation/Setup

### Installation Steps
1) Obtain API Keys
2) Install needed packages, clone Repo and install library dependencies
3) Configure the script

Remember that all the commands shared here are for Linux. So if you want you can run this on a Linux Server or even a Raspberry Pi. (Mine is running on a Raspberry Pi 3B+ with many other bots and scripts running with no issues.)

If you want to run this on a Windows or Mac machine, you will need to install Python3 and be familiar installing from a requirements.txt.

### Obtaining API Keys

The first step in this process will be obtaining the API keys that you need. 

##### APRS.fi API Key
* First and foremost, you will need an [APRS.fi](https://aprs.fi) account. On your account page is the API key you will need.
##### HamQTH.com Login
* To be able to use HamQTH.com for searching (especaillay International Callsigns), you will need to obtain a username and password for HamQTH.com. [Click here to register.](https://www.hamqth.com/register.php)

##### Discord

* Go to: [https://discord.com/developers/applications](https://discord.com/developers/applications)
* Click New Application
* Give it a name (I called it Hammy)
* On the next screen, you can upload an avatar for the bot.
* Click the bot selection under settings
* Click Add Bot
* Give it a Name (I used the same name )
* Then Copy the Bot Token (you will need this for the config.py part of the script along with the APRS.fi keys)
* Do not set as public bot (you only want this on servers you are in or adding it to. You don't want the possibility of other people pounding your API Keys for APRS.fi)
* Save Settings
* Click OAuth2 and then URL Generator
* For Scope Choose bot
* For Permissions, choose the following:
    - Under General Permissions:
        - Read Messages/View Channels
    - Under Text Permissions:
        - Send messages
        - Send Messages in threads
        - Embed Links
        - Read message History
        - Use Slash Commands
* Copy the generated URL
* Paste it into a browser window Address bar
* Choose the Server you want to authorize it to and then click authorize.
* It should pop into the server.

Once you have the keys you need and the bot authorized into your server, you will eventually copy them into the appropriate places in the config.py file, but now we need to get the files and get things installed.

---

### Installing the Script

The next step is installing the needed packages, cloning the repo to get the script and then installing the needed libraries for the script to work properly.

This is probably the easiest step to accomplish.

Please run the following commands:

```bash
sudo apt-get update && sudo apt-get -y upgrade && sudo apt-get -y dist-upgrade

sudo apt-get install python3 python3-pip git screen

git clone https://github.com/n8acl/hammy-discord-bot.git

cd hammy-discord-bot

pip3 install -r requirements.txt
```

Now you have everything installed and are ready to configure the script.

## Configure the Script
Once you have your API Keys, have cloned the repo and installed everything, you can now start configuring the bot. Open the config.py file in your editor of choice and copy in the keys you obtained from APRS.fi and Discord into the appropriate spots.

## Running the Script

Once you have the config file edited, start the bot by typing the following:

```bash
screen -R hammy-discord-bot
```

Then in the new window:
```bash
cd hammy-discord-bot

python3 hammy_bot.py
```

It should say "<bot Name> has connected to Discord". Once that is done, hit CTRL-A-D to disconnect from the screen session. If something ever happens, you can reconnect to the session by typing:

```bash
screen -R hammy-discord-bot
```

And see why it errored or quit. This is useful if you need to contact me for support.

---

# Bot Commands

All Commands can be issued from either a Direct Message or in a text channel, however, Callbook data is always returned in a DM. While callbook data is available online publicly, this helps to keep it at least a little private on the server.

| Command | Description | Example |
|---------|-------------|---------|
|/callsign < callsign >|Returns callbook data for the callsign queried,<br>including DMR ID and NXDNID, in a DM.|/callsign W1AW|
|/dmr < dmrid > | Returns callbook data for the DMR ID queried,<br>including DMR ID and NXDNID, in a DM.<br>This is useful to determine who is talking if you see a DMR ID<br>on your Radio that is not loaded into the radio contact list.|/dmr 1234567|
|/nxdn < nxdnid > | Returns callbook data for the NXDN ID queried,<br>including DMR ID and NXDNID, in a DM.<br>This is useful to determine who is talking if you see a NXDN ID<br>on your Radio that is not loaded into the radio contact list.|/nxdn 1234567|
|/aprs <callsign+ssid>|Returns last postion beaconed for the station queried.<br>Note that SSID is optional, but it will not do a<br>wildcard or fuzzy search.| /aprs W1AW<br>/aprs W1AW-9|
|/hammy|Brings up help text with the above command list.|/hammy



---

## Contact
If you have questions, please feel free to reach out to me. You can reach me in one of the following ways:

- Twitter: @n8acl
- Discord: Ravendos#7364
- Mastodon: @n8acl@mastodon.radio
- E-mail: n8acl@qsl.net

Or open an issue on Github. I will respond to it, and of course you, when I can. Remember, this is a hobby and there are other daily distractors that come first, like work, school and family.

If you reach out to me and have an error, please include what error you are getting and what you were doing. I may also ask you to send me certain files to look at. Otherwise just reach out to me :).

---

## Change Log

* 01/18/2022 - Added HamQTH.com for international callsign lookups. If a callsign is not found at callook.info, it will then try to retreive information on that callsign from HamQTH.com.

* 01/15/2022 - Initial Release 1.0