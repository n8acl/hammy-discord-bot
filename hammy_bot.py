#################################################################################

# Hammy, a Ham Radio Discord Bot
# Developed by: Jeff Lehman, N8ACL
# Current Version: 3.0
# https://github.com/n8acl/hammy-discord-bot

# Questions? Comments? Suggestions? Contact me one of the following ways:
# E-mail: n8acl@qsl.net
# Twitter: @n8acl
# Discord: Ravendos#7364
# Mastodon: @n8acl@mastodon.radio
# Website: https://www.qsl.net/n8acl

###################   DO NOT CHANGE BELOW   #########################

#############################
# Import Libraries
import config as cfg
import os
import json
import requests
import time
import xml.etree.ElementTree as et
import interactions # Discord library
from urllib import request, error
from datetime import datetime, date, time, timedelta
from geopy.geocoders import Nominatim
from table2ascii import table2ascii as t2a, PresetStyle, Alignment


#############################
# Create Discord Bot
TOKEN = cfg.discord_bot_token
server_id = int(cfg.discord_server_id)
bot = interactions.Client(token=TOKEN)

#############################
# Define Variables
# DO NOT CHANGE BELOW

linefeed = "\r\n"
degree_sign= u'\N{DEGREE SIGN}'
aprsfi_api_base_url = "https://api.aprs.fi/api/get"
repeaterbook_base_url = 'https://www.repeaterbook.com/api/export.php'
radioid_base_url = "https://database.radioid.net/api"
radioid_dmrid_url = radioid_base_url + "/dmr/user"
radioid_nxdnid_url = radioid_base_url + "/nxdn/user"
geolocator = Nominatim(user_agent="aprstweet")
debug = False

#############################
# Define Functions

def get_api_data(url,data_type):
    if data_type == 'json':
        # get JSON data from api's with just a URL
        return requests.get(url=url).json()
    if data_type =='xml':
        # get XML data from api's with just a URL
        return et.parse(request.urlopen(url))

def get_api_data_payload(url,payload,data_type):
    # get JSON data from api's
    if data_type == 'json':
        try:
            responses = requests.get(url=url,params=payload).json()
        except ValueError as e:
            return 0
        return responses

def get_location(lat,lng):
    # Reverse geocode with openstreetmaps for location
    osm_address = geolocator.reverse(lat.strip()+","+lng.strip())
    return osm_address.address

def get_grid(dec_lat, dec_lon):
    ## Function developed by Walter Underwood, K6WRU https://ham.stackexchange.com/questions/221/how-can-one-convert-from-lat-long-to-grid-square
    # Returns the Grid Square for the packet location

    upper = 'ABCDEFGHIJKLMNOPQRSTUVWX'
    lower = 'abcdefghijklmnopqrstuvwx'

    if not (-180<=dec_lon<180):
        sys.stderr.write('longitude must be -180<=lon<180, given %f\n'%dec_lon)
        sys.exit(32)
    if not (-90<=dec_lat<90):
        sys.stderr.write('latitude must be -90<=lat<90, given %f\n'%dec_lat)
        sys.exit(33) # can't handle north pole, sorry, [A-R]

    adj_lat = dec_lat + 90.0
    adj_lon = dec_lon + 180.0

    grid_lat_sq = upper[int(adj_lat/10)]
    grid_lon_sq = upper[int(adj_lon/20)]

    grid_lat_field = str(int(adj_lat%10))
    grid_lon_field = str(int((adj_lon/2)%10))

    adj_lat_remainder = (adj_lat - int(adj_lat)) * 60
    adj_lon_remainder = ((adj_lon) - int(adj_lon/2)*2) * 60

    grid_lat_subsq = lower[int(adj_lat_remainder/2.5)]
    grid_lon_subsq = lower[int(adj_lon_remainder/5)]

    return grid_lon_sq + grid_lat_sq + grid_lon_field + grid_lat_field + grid_lon_subsq + grid_lat_subsq

def get_aprs_position(callsign):

    status = ''
    fixed_station = False

    position_payload = {
    'name': callsign,
    'what': 'loc',
    'apikey': cfg.aprsfikey,
    'format': 'json'
    }

    data = get_api_data_payload(aprsfi_api_base_url,position_payload,'json')

    if len(data['found']) == 0:
        status = ('No data found for callsign %s' % callsign.upper())
    else:
        station = data["entries"][0]["name"]
        lat = str(data["entries"][0]["lat"])
        lng = str(data["entries"][0]["lng"])
        lasttime = data["entries"][0]["lasttime"]
        if "speed" in data["entries"][0]:
            speedkph = float(data["entries"][0]["speed"])
        else:
            fixed_station = True


        #Create Status Message
        status = station + ": "+ get_location(lat,lng)
            
        if not fixed_station:
            status = status + " | Speed: "+ str(round(speedkph/1.609344,1)) + " mph"  
        
        status = status + " | Grid: " + get_grid(float(lat),float(lng))

        status = status + " | " + datetime.fromtimestamp(int(lasttime)).strftime('%H:%M:%S') + \
            " | https://aprs.fi/" + station

        return status

def append_data(record_name,fielddata):
    dataset = []

    dataset.append(record_name)
    dataset.append(fielddata)

    return dataset

def lookup_calldata(callsign):
    callsigndata = ""
    calldata = []
    source = ''

    radioid_payload = {
        "callsign": callsign
    }

    # Let's get callbook data!
    # First, let's check Callook.info for the callsign data

    callook_url = "https://callook.info/" + callsign + "/json"
    callsign_data = get_api_data(callook_url,'json')

    if callsign_data["status"] == 'VALID':

        calldata.append(append_data("Callsign:",callsign_data['current']['callsign']))

        if callsign_data['previous']['callsign'] != '':
            calldata.append(append_data("Previous:",callsign_data['previous']['callsign']))
        if callsign_data['type'] == 'PERSON':
            calldata.append(append_data("Class:",callsign_data['current']['operClass'].title()))
        if callsign_data['type'] == 'CLUB':
            calldata.append(append_data("Trustee:",callsign_data['trustee']['name'].title() + ", "+ callsign_data['trustee']['callsign']))
        
        calldata.append(append_data("Name:",callsign_data['name'].title()))
        calldata.append(append_data("Address:",callsign_data['address']['line1'].title()))
        calldata.append(append_data("",callsign_data['address']['line2'].title()))
        calldata.append(append_data("Grid Square:",callsign_data['location']['gridsquare']))
        calldata.append(append_data("Grant Date:",callsign_data['otherInfo']['grantDate']))
        calldata.append(append_data("Expires:",callsign_data['otherInfo']['expiryDate']))

        source = 'Callook.info'

    # if the status came back invalid, so no data was found, let's try HamQTH.com for the data. 
    # This will include International callsign searches.
    else:
        prefix = '{https://www.hamqth.com}'
        callsign_result = ''
        name = ''
        address = ''
        city = ''
        state = ''
        zip = ''
        country = ''
        grid = ''
        hamqth_sessionid = ''

        hamqth_getsession_url = "https://www.hamqth.com/xml.php?u=" + config.hamqth_username + "&p=" + config.hamqth_password
        session_data = get_api_data(hamqth_getsession_url,'xml') 

        root = session_data.getroot()

        for item in root.findall(prefix + 'session'):
            for child in item:
                if child.tag == prefix + 'session_id':
                    hamqth_sessionid = child.text

        if hamqth_sessionid != '':
            hamqth_lookup_url = 'https://www.hamqth.com/xml.php?id='+ hamqth_sessionid + '&callsign=' + callsign  + '&prg=Hammy_Discord_Bot'

            hamqth_data = get_api_data(hamqth_lookup_url,'xml')

            root = hamqth_data.getroot()

            for item in root.findall(prefix + 'search'):
                for child in item:
                    if child.tag == prefix + 'callsign':
                        callsign_result = child.text.upper()
                    elif child.tag == prefix + 'adr_name':
                        name = child.text.title()
                    elif child.tag == prefix + 'adr_street1':
                        address = child.text.title()
                    elif child.tag == prefix + 'adr_city':
                        city = child.text.title()
                    elif child.tag == prefix + 'us_state':
                        state = child.text.upper()
                    elif child.tag == prefix + 'adr_zip':
                        zip = child.text
                    elif child.tag == prefix + 'country':
                        country = child.text
                    elif child.tag == prefix + 'grid':
                        grid = child.text

            calldata.append(append_data("Callsign:",callsign_result))
            calldata.append(append_data("Name:",name))
            calldata.append(append_data("Address:",address))
            calldata.append(append_data("",city + ', ' + state + ' ' + zip))
            calldata.append(append_data("",country))
            calldata.append(append_data("Grid Square:",grid))

            source = 'HamQTH.com'

    if len(calldata) <=0:
        callsigndata = "No Callsign Data found." + linefeed
    else:
        for x in range(len(calldata)):
            callsigndata = callsigndata + calldata[x][0] + " " + calldata[x][1] + linefeed

    # Now let's get DMR ID Data

    dmr_id_data = get_api_data_payload(radioid_dmrid_url,radioid_payload,'json')

    if len(dmr_id_data) > 0:

        dmr_count = int(dmr_id_data['count'])

        callsigndata = callsigndata + "DMR ID(s): "
        for i in range(dmr_count):
            if i > 0:
                callsigndata = callsigndata + ", " + str(dmr_id_data['results'][i]['id'])
            else:
                callsigndata = callsigndata + str(dmr_id_data['results'][i]['id'])
        
        callsigndata = callsigndata + linefeed
        
    # Now Let's Get NXDN ID Data

    nxdn_id_data = get_api_data_payload(radioid_nxdnid_url,radioid_payload,'json')

    if len(nxdn_id_data) > 0:

        nxdn_count = int(nxdn_id_data['count'])

        callsigndata = callsigndata + "NXDN ID(s): "
        for i in range(nxdn_count):
            if i > 0:
                callsigndata = callsigndata + ", " + str(nxdn_id_data['results'][i]['id'])
            else:
                callsigndata = callsigndata + str(nxdn_id_data['results'][i]['id'])
        
        callsigndata = callsigndata + linefeed
        
    callsigndata = callsigndata + "Source: " + source + linefeed

    # Return whatever data we have found.
    return callsigndata

#############################
# Define Discord Bot Functions


@bot.command(
    name='callsign',
    description="Lookup Callsign Data",
    scope=server_id,
    options = [
        interactions.Option(
            name="callsign",
            description = "Callsign to search for",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
    )
async def callsign(ctx: interactions.CommandContext, callsign: str):

    await ctx.send("This will take a moment. I will send you a DM when I have the data ready!", ephemeral=True)

    embed = interactions.Embed(title = "Callbook Data for " + callsign.upper(),
        description=lookup_calldata(callsign.lower()),
    )

    await ctx.author.send(embeds = embed)

@bot.command(
    name='dmr',
    description='Look up Callsign by DMR ID',
    scope=server_id,
    options = [
        interactions.Option(
            name="dmrid",
            description = "DMR ID to search for",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
    )
async def dmr(ctx: interactions.CommandContext, dmrid: str):

    radioid_payload = {
    "id": dmrid
    } 

    await ctx.send("This will take a moment. I will send you a DM when I have the data ready!", ephemeral=True)

    dmr_id_data = get_api_data_payload(radioid_dmrid_url,radioid_payload,'json')

    if int(dmr_id_data['count']) > 0 :
        embed = interactions.Embed(title = "Callbook Data for " + dmr_id_data['results'][0]['callsign'].upper(),
            description=lookup_calldata(dmr_id_data['results'][0]['callsign']),
        )

    else:
       
        embed = interactions.Embed(title = "No DMR ID's Found",
            description="No ID's Found"
        )

    await ctx.author.send(embeds = embed)

@bot.command(
    name='nxdn',
    description='Look up Callsign by NXDN ID',
    scope=server_id,
    options = [
        interactions.Option(
            name="nxdnid",
            description = "NXDN ID to search for",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
    )
async def nxdn(ctx: interactions.CommandContext, nxdnid: str):

    radioid_payload = {
    "id": nxdnid
    } 

    await ctx.send("This will take a moment. I will send you a DM when I have the data ready!", ephemeral=True)

    nxdn_id_data = get_api_data_payload(radioid_nxdnid_url,radioid_payload,'json')

    if int(dmr_id_data['count']) > 0 :
        embed = interactions.Embed(title = "Callbook Data for " + nxdn_id_data['results'][0]['callsign'].upper(),
            description=lookup_calldata(nxdn_id_data['results'][0]['callsign']),
        )

    else:
       
        embed = interactions.Embed(title = "No NXDN ID's Found",
            description="No ID's Found"
        )

    await ctx.author.send(embeds = embed)

@bot.command(
    name='aprs',
    description='Find Last APRS Position for a Station',
    scope=server_id,
    options = [
        interactions.Option(
            name="callsign",
            description = "Callsign+SSID of the station to look for",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
    )
async def aprs(ctx: interactions.CommandContext, callsign: str):

    await ctx.send("This will take a moment. I will send you a DM when I have the data ready!", ephemeral=True)

    embed = interactions.Embed(title = "Last APRS Position",
        description=get_aprs_position(callsign),
    )
    await ctx.author.send(embeds = embed)

@bot.command(
    name='hammy',
    description='Help Text',
    scope=server_id,
    )
async def hammy(ctx: interactions.CommandContext):
    
    cmd_list = """
    /callsign <callsign> - Returns callbook data for the callsign queried, including DMR ID and NXDNID, in a DM. ex: /callsign W1AW.

    /dmr <dmrid> - Returns callbook data for the DMR ID queried, including DMR ID and NXDNID, in a DM. ex: /dmr 1234567
        Note: This does not return information about a Talkgroup ID, only a DMR ID linked to a callsign.

    /nxdn <nxdnid> - Returns callbook data for the NXDN ID queried, including DMR ID and NXDNID, in a DM. ex: /nxdn 1234567
        Note: this does not return information about an NXDN Talkgroup, just an ID linked to a callsign.

    /aprs <callsign+ssid> - Returns last postion beaconed for the station queried. Note that SSID is optional, but it will not do a wildcard or fuzzy search. ex: /aprs W1AW or /aprs W1AW-9

    /hammy - This help text

    More information about me can be found at https://github.com/n8acl/hammy-discord-bot
    """

    embed = interactions.Embed(title = "Hammy Commands",
        description=cmd_list
    )
    await ctx.send(embeds = embed)

bot.start()