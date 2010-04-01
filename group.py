#########################################################
#                                                       #
#   Activities related to group creation and fetching.  #
#                                                       #
#########################################################



from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from dataModel import Groups
import datetime
import time
import urllib



class CreateGroup(webapp.RequestHandler):
    def get(self):
        
        #getting the parameter values
        administrator = self.request.get('administrator')
        groupName = self.request.get('groupName')
        password = self.request.get('password')
        curtime = time.time()
        
        #storing the parameters in the group data Model
        try:
            newGroup = Groups( administrator = administrator,
                          groupName = groupName,
                          password = password,
                          memberCount = 1,
                          curtime = curtime
                        )
            newGroup.put()

            #Wow, a group has been added. Now its time for response to the client
            self.response.out.write("Group <B>" + groupName + "</B> has been created.<a href='/inviteFriends' target='_blank'> Click to invite your friends to your group.</a>")
            urllib.urlopen('https://instantshout.appspot.com/invite?email=' + administrator)
            
        except:
            #In case something went wrong with the datastore
            self.response.out.write('Group could not be created. Please try again.')
        
        


class GetPublicGroups(webapp.RequestHandler):
    def get(self):
        #getting the parameter values for limit
        limit = self.request.get('limit')

        # we now make a query for public groups i.e. groups with password as empty string
        try:
            publicGroups = db.GqlQuery("SELECT * FROM Groups WHERE password = 'public' ORDER BY memberCount DESC LIMIT " +limit)
            self.response.out.write("<TABLE class='ui-state-error-text' width='100%'>")
            self.response.out.write("<TR class='ui-state-default'><TD>Group Name</TD><TD>User Count</TD><TD>Group Administrator</TD></TR>")

            for aGroup in publicGroups:
                self.response.out.write('<TR><TD>' + aGroup.groupName + '</TD><TD>' + 'NA' + '</TD><TD>' + aGroup.administrator + '</TD></TR>')
            self.response.out.write('</TABLE>')
        except:
            #In case something went wrong with the datastore
            self.response.out.write('Public Groups could not be retrived now.')



class GetAllGroups(webapp.RequestHandler):
    def get(self):
        #getting the parameter values for limit
        limit = self.request.get('limit')

        # we now make a query for public groups i.e. groups with password as empty string
        try:
            publicGroups = db.GqlQuery("SELECT * FROM Groups ORDER BY memberCount DESC LIMIT " +limit)
            self.response.out.write("<TABLE class='ui-state-error-text' width='100%'>")
            self.response.out.write("<TR bgcolor='orange'><TD>Group Name</TD><TD>User Count</TD><TD>Group Administrator</TD></TR>")

            for aGroup in publicGroups:
                self.response.out.write('<TR><TD>' + aGroup.groupName + '</TD><TD>' + 'NA' + '</TD><TD>' + aGroup.administrator + '</TD></TR>')
            self.response.out.write('</TABLE>')
        except:
            #In case something went wrong with the datastore
            self.response.out.write('Public Groups could not be retrived now.')






application = webapp.WSGIApplication([('/createGroup', CreateGroup),
                                      ('/getPublicGroups', GetPublicGroups),
                                      ('/getAllGroups', GetAllGroups)

                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
