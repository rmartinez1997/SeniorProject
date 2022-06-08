
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from scapy.all import sniff
#Getting used to git
#Editing via Github browser

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# Start

# Print out the first 5 packets
# if __name__=="main":
#      print("hello")
#      print(sniff())
# print("Testing")
# cap = sniff()
# cap.summary()

# Let's make a function that sends a message to your phone
def sndMessage(b_message):
    # TODO
    account_sid = "ACf03feeb2b0e2e3e6027c1356b645d022"
    auth_token = "013160597fed8fc537d0eabda330650d"
    client = Client(account_sid, auth_token)
    message = client.messages \
    .create(
         body=b_message,
         from_='+14784296043',
         to='+13235097091'
     )
sndMessage('hello')
