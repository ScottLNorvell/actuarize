import webapp2
#from render import render_str

import os
import jinja2
import facebook
import logging

from user_db import User
from webapp2_extras import sessions
import time


#from signup import UserInfo


###############################################
### info for actuarize 2
###############################################
FACEBOOK_APP_ID = "337031986416801"
FACEBOOK_APP_SECRET = "b0e1f9ae4d5ca035d426395f8e8b15d3"

###############################################
### info for fbtest3500
###############################################
#FACEBOOK_APP_ID = "624790460881207"
#FACEBOOK_APP_SECRET = "f9ada0d17315bf760e4fba34d2366fec"

###############################################
### Create Environment and basic handler funct
###############################################


def render_str(template, **params):
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def init_graph(self,access_token):
        return facebook.GraphAPI(access_token)
    
    # check if post session is current
    def updated_post_session(self,name):
        post = self.session.get('post')
        if post and post['name'] == name:
            return True
        else:
            return False
    
    def authed_user(self,user):
        graph = facebook.GraphAPI(user['access_token'])
        try: 
            graph.get_object(user['id'])
        except:
            return False
        return True
    
    @property
    def current_user(self):
        """ First checks to see if the user exists in sessions. 
            Then tries to get the user from Cookie set by facebook.
            If user is not in Database, adds user to database.
            If user in database and access token has expired, it updates the access token.
            If all else fails, returns None. """
        if self.session.get("user"):
            # User is logged in
            logging.info('****Got User from Session!****')
            return self.session.get("user")
        else:
            # Either used just logged in or just saw the first page
            # We'll see here
            cookie = facebook.get_user_from_cookie(self.request.cookies,
                                                   FACEBOOK_APP_ID,
                                                   FACEBOOK_APP_SECRET)
            if cookie:
                # Okay so user logged in.
                # Now, check to see if existing user
                user = User.get_by_key_name(cookie["uid"])
                # If user has a friend_data field, say so in the session
                fd = False
                if user and user.friend_data:
                    fd = True
                    
                if not user:
                    # Not an existing user so get user info
                    graph = facebook.GraphAPI(cookie["access_token"])
                    profile = graph.get_object("me")
                    user = User(
                        key_name=str(profile["id"]),
                        id=str(profile["id"]),
                        name=profile["name"],
                        access_token=cookie["access_token"],
                        gender=profile['gender']
                    )
                    # Add user info to DB
                    user.put()
                    logging.info('****Added User to DataBase!****')
                elif user.access_token != cookie["access_token"]:
                    user.access_token = cookie["access_token"]
                    user.put()
                    logging.info('Changed access token!')
                # User is now logged in
                self.session["user"] = dict(
                    name=user.name,
                    id=user.id,
                    access_token=user.access_token,
                    gender=user.gender,
                    fd=fd
                )
                return self.session.get("user")
        return None
    
    
    def logout(self):
        if self.current_user is not None:
            self.session['user'] = None
        
    def dispatch(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        self.session_store = sessions.get_store(request=self.request)
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        """
        This snippet of code is taken from the webapp2 framework documentation.
        See more at
        http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html

        """
        return self.session_store.get_session()
    
class TestHandler(BaseHandler):   
    def get(self):
        self.render('bartest.html')
        
    def post(self):
        time.sleep(5)
        tt = self.request.get('test_text')
        self.render('you-did-it.html',
                    test_text = tt)
