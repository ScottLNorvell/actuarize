
import facebook
import webapp2
import logging
from google.appengine.api import memcache
from user_db import User
import pickle
from urllib import urlencode


from base import BaseHandler

from fb_download import *
from actuary_fb import actuary_valdic

###############################################
### FaceBook Base Handler
###############################################

class FBBaseHandler(BaseHandler):
    
    def get_friend_dict(self,user):
        """ After self.current_user, this gets the friend_dict and stores it in 
                Memcache AND User.
            
            If an existing user hits /fbactuarized with a friend_dict that is <= days days old, 
                their existing friend_dict is returned
        """
        days = 14
        uid = user['id']
        fd = user.get('fd')
        access_token = user['access_token']
        name = user['name']
        if fd:
            # The user db has a friend_dict
            logging.info('****fd = True!***')
            friend_dict = self.get_friend_dict_page(uid)
            if friend_dict:
                # get_friend_dict_page returned a friend_dict
                
                logging.info('****Got friend_dict from uid!***')
                updated = friend_dict.get('updated')
                delta = get_timedif(updated)
                if delta <= days:
                    # friend_dict < 2 weeks old
                    try:
                        ## See if user is authorized user
                        graph = self.init_graph(access_token)
                        profile = graph.get_object("me")
                        logging.info('***This is {}!****'.format(profile['name']))
                        memcache.set('user_' + uid, 
                                     friend_dict)
                        logging.info('****Got fresh-enough friend_dict from user!***')
                        return friend_dict
                    except:
                        ## Session user is not current user
                        self.logout()
                        return None
        
        ### No existing friend_dict, so we'll generate one!        
        sex = user['gender']
        
        ### Tries to get friends using existing access_token
        try:
            friends = get_friends_fql2(access_token, uid)
        except:
            # Generally means session user doesn't match current user
            # logout() dumps the session so that redirect can get current user from cookie!
            self.logout()
            return None
        
        ### Main code that generates friend_dict
        filtered = filter_friends(friends)
        ages, ids, num = extract_ages_and_ids2(filtered)
        friend_dict = actuary_valdic(ages)
        friend_dict['ids'] = ids
        friend_dict['num'] = num
        friend_dict['name'] = name
        friend_dict['sex'] = sex
        friend_dict['updated'] = datetime.date.today()
        
        ### Add friend_dict to memcache (for easy retrieval from permalink)
        memcache.set('user_' + uid, 
                     friend_dict)
        
        ### Adds friend_dict to datastore
        this_user = User.get_by_key_name(uid)
        if this_user:
            # User should exist, but just in case:
            pickled_fd = pickle.dumps(friend_dict)
            this_user.friend_data = pickled_fd
            this_user.put()
            self.session["user"]["fd"] = True
        else:
            return None
        ### Done Adding
        return friend_dict
    
    # get_friend_dict data from page.
    def get_friend_dict_page(self, uid):
        """For PermaLink Purposes:
                Gets user from memcache, then db.
                If neither: user doesn't exist yet. 
                    Returns None.
        """
        friend_dict = memcache.get('user_' + uid)
        if not friend_dict:
            user =  User.get_by_key_name(uid)
            if user:
                logging.info('***Got the user with id {} from User!***'.format(uid))
                pickled_fd = user.friend_data
                friend_dict = pickle.loads(pickled_fd)
                return friend_dict
            else:
                return None
        logging.info('***Got the user with id {} from memcache!***'.format(uid))    
        return friend_dict
    
    


##################################################
### FB Auth Page Handler
##################################################

    
            

class FBLoginHandler(FBBaseHandler):
    def get(self):
        #Renders Login Page. Redirects to redirect_url when done.
        template = 'fb-login.html'
        redirect_url = '/fbactuarized'
        self.render(template, url=redirect_url)
 
##################################################
### Runs Main Code after Login
##################################################
        
class FBActuarizedHandler(FBBaseHandler):
    def get(self):    
        user = self.current_user
        if user:
            uid = user['id']
            friend_dict = self.get_friend_dict(user)
            if friend_dict:
                self.redirect('/fbactuarized/' + uid)
            else:
                self.redirect('/fblogin')
        else:
            self.redirect('/fblogin')

##################################################
### Actuary FB Permalink (for posting purposes)
##################################################
        
class FBActuPermaLinkHandler(FBBaseHandler):
    # Add some handling that checks current user and displays diff message based on That
    # ie if current_user['id'] == uid , render page differently?
#    if friend_dict['name'] == user['name']:
#        ## friend_dict is current user's friend_dict
    def get(self, uid):
        friend_dict = self.get_friend_dict_page(uid)
        
        if friend_dict:
            friend_dict['uid'] = uid
            try:
                sex = friend_dict['sex']
            except:
                sex = 'neuter'
            if sex == 'male':
                pronoun = 'his'
            elif sex == 'female':
                pronoun = 'her'
            else:
                pronoun = 'their'
            friend_dict['pronoun'] = pronoun
            
            post_url = '/fb-post/' + uid + '?' + urlencode(dict(name=friend_dict['name']))
            script = 'actu_fb'                                                
            
            self.render('actuarized-fb.html',
                        script = script,
                        post_url = post_url,
                        **friend_dict)
        else:
            backlink = "/"
            self.render('oops-fb.html',
                        type = 'facebook',
                        backlink = backlink)

##################################################
### FB Posting Handler (handles Posting to Facebook!)
##################################################

class FBPostLoginHandler(FBBaseHandler):
    def get(self, uid):
        self.logout()
        name = self.request.get('name')
        template = 'fb-postlogin.html'
        redirect_url = '/fb-post/' + uid
        self.render(template, 
                    url=redirect_url, 
                    name=name)



##################################################
### FB Posting Handler (handles Posting to Facebook!)
##################################################

class FBPostHandler(FBBaseHandler):
    def get(self, uid):
        name = self.request.get('name')
        if name:
            updated = self.updated_post_session(name)
            if not updated:
                attachment = {"name": "{} has been Actuarized!".format(name),
                              "link": "http://actuarize.appspot.com/fbactuarized/" + uid,
                              "caption": "Actuarize your friends!",
                              "description": "Click here for some disturbing data about {} and friends.".format(name),
                              "picture": "http://s18.postimg.org/63pc81kvp/actulogo_sq.png"}
                
                self.session['post'] = dict(name=name,
                                            attachment=attachment)
            
        user = self.current_user
        if user and self.authed_user(user):
            backlink = '/fbactuarized/' + uid
            self.render('fb-post.html',
                        backlink = backlink,
                        name = name)
        else:
            self.redirect('/fb-postlogin/' + uid + '?' + urlencode(dict(name=name)))
            
    def post(self, uid):
        user = self.current_user
        if user:
            session = self.session.get('post')
            attachment = session['attachment']
            name = session['name']
            message = self.request.get('message')
            try:
                graph = self.init_graph(user['access_token'])
                graph.put_wall_post(message, attachment)
                self.redirect('/fb-posted/' + uid + '?' + urlencode(dict(fb_id=user['id'],
                                                                         name=name)))
            except:
                self.redirect('/fb-postlogin/' + uid  + '?' + urlencode(dict(name=name)))
        else:
            self.redirect('/fb-postlogin/' + uid)
            

##################################################
### FB Posting Handler (handles Posting to Facebook!)
##################################################

class FBPostedHandler(FBBaseHandler):
    def get(self, uid):
        fb_id = self.request.get('fb_id')
        name = self.request.get('name')
        backlink = '/fbactuarized/' + uid
        self.render('fb-posted.html',
                    backlink = backlink,
                    name=name,
                    fb_id=fb_id)
        