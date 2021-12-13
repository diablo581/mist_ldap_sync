# Mist LDAP Sync
 This is Python script to automatically create/delete Mist PPSK for user in AD/LDAP/LDAPS Group.

## MIT LICENSE
 
Copyright (c) 2021 Thomas Munzer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the  Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## How it works?
1. The script will retrieve all the LDAP/AD users that belong to a specific user group. It will only query for username and email attributes
2. The script will retrieve all the Mist Site or Org PPSK created for the configured SSID
3. The script will look for
  * PPSKs not tied to any users from the AD/LDAP. If any, it will delete the PPSK
  * Users without PPSK. If any it will create the PPSK.

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/generate.png" width="45%">
</div>
 
4. If configured, the script will send the new PPSK to each user

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/user.png" width="45%">
</div>

5. If configured, the script will send a report with created/deleted PPSK to the administrator(s)

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/report.png" width="45%">
</div>


## How to use it?
1. Just install the dependencies manually or with the `requirements.txt` file. For example with `pîp -r requirements.txt`.
2. Then configure the `config.py` file.
3. And to finish start the script with `python mist_ldap_sync.py` or `python3 mist_ldap_sync.py` depending on your system

##  Curent Limitation
- If you have multiple sites, the script must be run for each site

## Configuration
### Script settings
Check the `example.env` file to know how to configure the script. You will have to create a `.env` file with the required settings.

By default, the script is looking for the `.env` file in its own directory. You can also pass the `.env` file location when running the script with the `-e` option (i.e. `python3 mist_psk_rotate.py -e <path to the env file>`).

You can use the `-c` option to check your configuration.

<div>
<img src="https://github.com/tmunzer/mist_ldap_sync/raw/main/._readme/img/check.png" width="50%">
</div>

### Email template
**Any change in the `psk_template.html` is at your own risks!**

If you want to customize the email sent to the users, you can modify the `psk_template.html` file. It's basicaly a HTML file, but:
- Be sure to use double curly brackets "{{" and "}}" instead of single curly brackets for HTML
- The script will inject 3 information in the template:
  - `{0}` will be replaced by the logo image location. It must be published on a web server and reachable by the users' devices
  - `{1}` will be replaced by the user name
  - `{2}` will be replaced by the SSID name
  - `{3}` wll be replaced by the PPSK value
  - If QRcode is enabled, `{4}` wll be replaced by the QRCode information (i.e. "You can also scan the QRCode below to configure your device:")
  - If QRcode is enabled, `{5}` wll be replaced by the QRCode
