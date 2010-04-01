from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext import db
from dataModel import *
import datetime
import time


class Broadcaster(webapp.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
    # get(message, sender)
        msgSender = message.sender
        msgBody = message.body
        #userid to remain private  msgSender.find('@')
        msgBody = '*' + msgSender[0:msgSender.find('@')] + ':* ' + msgBody
        currentTime = time.time()






        
        #message.reply("Broadcasting your message........")
    #add message to data store
        newMessage=UserMessage(
                      sender=msgSender,
                      messageBody = msgBody,
                      curtime=currentTime
                      )
        newMessage.put()
    #get all usernames from user in data store.. FUTURE IMPL memcache
        allUsers = db.GqlQuery("SELECT * FROM AllUser")
    #send message to users who are online
        for aUser in allUsers:
            userAddress = aUser.emailID
            chat_message_sent = False
            if userAddress <> msgSender[0:msgSender.find('/')]:
                xmpp.send_message(userAddress, msgBody)
                    






class IsOnline(webapp.RequestHandler):
    def get(self):
        allUsers = db.GqlQuery("SELECT * FROM AllUser")
        onlineCount = 0
        for aUser in allUsers:
            userAddress = aUser.emailID
            if xmpp.get_presence(userAddress):
                onlineCount = onlineCount + 1
        self.response.out.write(str(onlineCount))
            
        



application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', Broadcaster),
                                      ('/onlineCount', IsOnline)

                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
