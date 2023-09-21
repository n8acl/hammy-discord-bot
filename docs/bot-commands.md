# Bot Commands

All Commands can be issued from any text channel and the message will be returned in a message that only you can see. While callbook data is available online publicly, this helps to keep it at least a little private on the server.

| Command | Description | Example |
|---------|-------------|---------|
|/callsign < callsign >|Returns callbook data for the callsign queried,<br>including DMR ID and NXDNID, in a DM.|/callsign W1AW|
|/dmr < dmrid > | Returns callbook data for the DMR ID queried,<br>including DMR ID and NXDNID, in a DM.<br>This is useful to determine who is talking if you see a DMR ID<br>on your Radio that is not loaded into the radio contact list.|/dmr 1234567|
|/nxdn < nxdnid > | Returns callbook data for the NXDN ID queried,<br>including DMR ID and NXDNID, in a DM.<br>This is useful to determine who is talking if you see a NXDN ID<br>on your Radio that is not loaded into the radio contact list.|/nxdn 1234567|
|/aprs <callsign+ssid>|Returns last postion beaconed for the station queried.<br>Note that SSID is optional, but it will not do a<br>wildcard or fuzzy search.| /aprs W1AW<br>/aprs W1AW-9|
|/hammy|Brings up help text with the above command list.|/hammy|