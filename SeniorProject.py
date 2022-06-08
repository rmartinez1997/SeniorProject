
# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from scapy.all import sniff
#Getting used to git

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# Start
account_sid = "ACf03feeb2b0e2e3e6027c1356b645d022"
auth_token = "013160597fed8fc537d0eabda330650d"
client = Client(account_sid, auth_token)
message = client.messages \
    .create(
         body='Hi Cunt',
         from_='+14784296043',
         to='+13235097091'
     )
# Print out the first 5 pacets
# if __name__=="main":
#      print("hello")
#      print(sniff())
# print("Testing")
# cap = sniff()
# cap.summary()