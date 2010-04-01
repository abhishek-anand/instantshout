from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext import db
from dataModel import Users
from dataModel import Groups
import datetime
import time

curtime =time.time()

class ResponseHandle(xmpp_handlers.CommandHandler):
    def join_command(self, message=None):
        msgArg = message.arg
        msgSender = message.sender
        msgSender = msgSender[0:msgSender.find('/')]
        groupName = msgArg[0:msgArg.find(' ')]
        password  = msgArg[msgArg.find(' ')+1:]
        #we now have message sender, group name and password to check and do things
        groups = db.GqlQuery("SELECT * FROM Groups WHERE groupName = :1 AND password = :2",groupName,password)
        valid = groups.count()
        if valid > 0:
            queryRes = db.GqlQuery('SELECT * FROM Users WHERE userID = :1', msgSender)
            for result in queryRes:
                result.delete()
            newUser=Users(
                      userID=msgSender,
                      curtime=curtime,
                      presentGroup = groupName
                      )
            newUser.put()
            message.reply('You have joined ' + groupName +'. say hi to everyone')
            #TO IMPLEMENT increase group.memberCount by one
        else:
            message.reply('Incorrect groupName or password.For list of public groups visit https://instantshout.appspot.com')
                
    def leave_command(self,message=None):
        msgSender = message.sender
        msgSender = msgSender[0:msgSender.find('/')]
         #downgrade users group to global
        queryRes = db.GqlQuery('SELECT * FROM Users WHERE userID = :1', msgSender)
        for result in queryRes:
            result.delete()
        newUser=Users(
                      userID=msgSender,
                      curtime=curtime,
                      presentGroup = 'global'
                      )
        newUser.put()
        #TO IMPLEMENT decrease group.memberCount by one
        message.reply('You have left the group')                



    def text_message(self, message=None):                
        msgSender = message.sender
        username = msgSender[0:msgSender.find('/')]
        msgBody = message.body
        msgBody = '*' + username[0:username.find('@')] + ':* ' + msgBody

        #EVERYTHING IS CORRECT TILL HERE
        
        queryRes = db.GqlQuery('SELECT * FROM Users WHERE userID = :1', username)
        for result in queryRes:
            groupName = result.presentGroup
            execQuery = db.GqlQuery('SELECT * FROM Users WHERE presentGroup = :1', groupName)
            for user in execQuery:
                if user.userID <> username:
                    xmpp.send_message(user.userID, msgBody)
        












application = webapp.WSGIApplication([
    ('/_ah/xmpp/message/chat/', ResponseHandle)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
