#TODO find the best method to do a priority 2 notification
#Import our various libraries
import textwrap
import argparse
import urllib.request
import http.client, urllib
import time

#Clearly defined pushover block for maximum clarity and pushing
def pushover(message, url, priority=0):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.parse.urlencode({
        "token": app_token,
        "user": group_id,
        "message": message,
        "url": url,
        "priority": priority,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

#Start our argument parser, with help, etc.
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='''Designed with Nagios in mind, this script takes your input, and uses it to send pushover messages.''',
                                 epilog=textwrap.dedent('''\
                                 A full example could look like:
                                 push_file.py Ajeieij234342ef kjvvi335ajffkDFA "I like cheese" http://cheese.com
                                 '''))
parser.add_argument('app_token', type=str, help='App Token as given to you in pushover')
parser.add_argument('user_key', type=str, help='User key from pushover')
parser.add_argument('message', type=str, help='Message you wish to send. I.e "Hey, this is a message"')
parser.add_argument('--url', type=str, help='Optional URL to send, i.e. http://google.com')
parser.add_argument('--priority', type=int, help='Manually specify the priority for your message')
args = parser.parse_args()

#Getting little global variables
app_token = args.app_token
group_id = args.user_key
message = args.message
priority = args.priority

#Seeing as argument is optional, we can't definitively set this every time
#Also, there's probably a better way to handle this, but I'm new to python...
if args.url != 0:
    url = args.url

#Add support to detect the phrase "CRITICAL" from Nagios
if 'CRITICAL' in message:
    priority = 1
else:
    priority = 0

#Call our almighty pushy one
pushover(message, url, priority)
