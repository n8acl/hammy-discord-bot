# Obtaining your API Keys

The first step in this process will be obtaining the API keys that you need. 

Even though this script does alot, there are alot of other webservices and networks that it needs to interact with and that is where these API, or Advanced Programmer Interface, Keys come in. An API is a service provided to allow users to programatically interact with the fore mentioned webservice.

While gathering your keys, make sure to copy them to a safe place where you can find them. You will need them for the script and some of these services can take a few days to approve your access. So please make sure to work through this and get all the keys you need saved some place before you start.

This part of the installation process, especially for a new user, takes the longest and is the most frustrating. If you already have some keys for each of these, you can use those if you choose to, to make things quicker.

##### APRS.fi API Key
* First and foremost, you will need an [APRS.fi](https://aprs.fi) account. On your account page is the API key you will need.
  
##### HamQTH.com Login
* To be able to use HamQTH.com for searching (especially International Callsigns), you will need to obtain a username and password for HamQTH.com. [Click here to register.](https://www.hamqth.com/register.php)

##### Discord

* Go to: [https://discord.com/developers/applications](https://discord.com/developers/applications)
* Click ```New Application```
* Give it a name (I called it Hammy)
* On the next screen, you can upload an avatar for the bot.
* Click the ```bot``` selection under settings
* Click ```Add Bot```
* Give it a Name (I used the same name )
* Then Copy the Bot Token (you will need this for the config.py part of the script along with the APRS.fi keys)
* Turn off ```Public Bot```
* Make sure to turn on the ```Message Intents``` Setting under ```Privileged Gateway Intents```.
* Save Settings
* Click ```OAuth2``` and then ```URL Generator```
* For Scope Choose ```bot``` and ```appplications.commands```
* For Permissions, choose the following:
    - Under General Permissions:
        - Read Messages/View Channels
    - Under Text Permissions:
        - Send messages
        - Send Messages in threads
        - Embed Links
        - Attach Files
        - Read message History
        - Use Slash Commands
* Copy the generated URL
* Paste it into a browser window Address bar
* Choose the Server you want to authorize it to and then click authorize.
* It should pop into the server.
* Next you will need to get your server id.
  * To get this, you will need to, on Discord, go into ```User Settings```->```Advanced``` and turn on ```Developer Mode``` (if it is not already on.)
  * Then just right click on your server's icon and click ```Copy ID```. Then go back into your ```config.json``` and paste that ID in the ```discord_server_id``` field.

Once you have the keys you need and the bot authorized into your server, you will eventually copy them into the appropriate places in the config.json file, but now we need to get the files and get things installed.