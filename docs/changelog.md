# Change Log

* 09/21/2023 - Moved bot to Docker Container

* 05/30/2022 - Removed returning data in a DM to returning it as an ephemeral message using slash commands.

* 05/25/2022 - Version 4.0 Release
  * Migrated to ```pycord``` discord library for slash command support. This replaces the ```interactions.py``` library and the ```discord.py``` library.

* 03/14/2022 - Version 3.0 Release
  * Migrated to ```interactions.py``` for slash command support
  * Removed Repeater lookup for now. ```interactions.py``` does not support file sending at this point and the returns are too large to send via a message.

* 02/19/2022 - Version 2.0 Release
  * Added ability to look up North American Repeaters via RepeaterBook.com

* 01/18/2022 - Minor Release
  * Added HamQTH.com for international callsign lookups. If a callsign is not found at callook.info, it will then try to retreive information on that callsign from HamQTH.com.

* 01/15/2022 - Initial Release 1.0