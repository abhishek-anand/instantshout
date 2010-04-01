from google.appengine.ext import webapp
from google.appengine.api import xmpp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from dataModel import Users
from google.appengine.api import mail
import datetime
import time



class SendInvitation(webapp.RequestHandler):
    def get(self):
        username=self.request.get("email")
        msg = "Welcome to instantSHOUT. Just send me anything and we will broadcast it to the world. Visit https://instantshout.appspot.com to know more."
        currentTime= time.time()
        xmpp.send_invite(username)
        xmpp.send_message(username, msg)
        newUser=Users(
                      userID=username,
                      curtime=currentTime
                      )
        newUser.put()
        self.response.out.write("<B>" + username + " has been invited. Please accept the request in your chat client.</B>")


class SendGroupInvitation(webapp.RequestHandler):
    def get(self):
        username=self.request.get("email")
        group = self.request.get("group")
        password = self.request.get("password")
        msg = 'Welcome user. Visit https://instantshout.appspot.com to join chat groups or to create your own group.'
        currentTime= time.time()
        xmpp.send_invite(username)
        xmpp.send_message(username, msg)
        newUser=Users(
                      userID=username,
                      curtime=currentTime
                      )
        newUser.put()
        mail.send_mail(sender="Invitation from " + group + " <invite@instantshout.appspotmail.com>",
              to=self.request.get("email"),
              subject="Gtalk group chat invitation for " + group,
              body="""

One of your friends has invited you to join their chat group on Gtalk. To start chatting in this group you need to follow these simple steps.

1. Add instantshout@appspot.com as a friend in your IM client ( Gtalk or others). You may already have received an invitation just accept it in your IM client.
2. Send the following in Gtalk to instantshout@appspot.com to join this group        /join """ + group + """ """ + password + """

/join groupname password is the command to join a group. To prevent you from getting disturbed you can join only one group at a time. To unjoin a group (say for joining other group) type /leave and send it to instanshout in Gtalk.
If you dont want to receive chats and updates from your group while your are offline just send     /leave     to instantshout@appspot.com from Gtalk.
Have fun shouting in groups.

Visit https://instantshout.appspot.com to create your own group and find out more groups and more.



InstantShout.






You received this message because one of yor friends invited you to join their group on http://instantshout.appspot.com
""")
        self.response.out.write("<B>" + username + " has been invited to join your group.Invite more friends for fun</B>")
    

application=webapp.WSGIApplication([
                                    ('/invite',SendInvitation),
                                    ('/groupInvite',SendGroupInvitation)
                                    ],
                                   debug=True)
def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
