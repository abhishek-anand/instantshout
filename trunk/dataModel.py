#########################################################
#                                                       #
#   The Data models used in Instant Shout are here.     #
#                                                       #
#########################################################



from google.appengine.ext import db


# Stores the user messages which are sent to the bot. Message can be multiline

class UserMessage(db.Model):
    sender=db.StringProperty()
    messageBody = db.StringProperty(multiline=True)
    curtime = db.FloatProperty()



# This contains the groupName alongwith its password and administrator name

class Groups(db.Model):
    administrator = db.StringProperty(required = True)
    groupName = db.StringProperty(required = True)
    password = db.StringProperty(default = 'public')
    curtime = db.FloatProperty()
    memberCount = db.IntegerProperty(default = 1)



# The collection of users with their present group set to global by default

class Users(db.Model):
    userID=db.StringProperty(required = True)
    presentGroup = db.StringProperty(default = 'global')
    curtime = db.FloatProperty()
