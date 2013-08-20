from base import BaseHandler
from actuary_fb import actuary_valdic
from tmdb_download import get_cast_data, init_movie, get_first_mov_url_noyear, get_first_mov_url
from user_db import MovieDB
import pickle
import logging
from google.appengine.api import memcache
from urllib import urlencode

###############################################
### Movie Base Handler
###############################################

class MVBaseHandler(BaseHandler):
    def get_movie(self,movie_id,title,year):
        """ First check to see if movie is in memcache.
            Then see if movie is in db.
            Then get movie from themoviedb.org using script.
        """
        moviedic = memcache.get('movie_' + str(movie_id))
        if moviedic:
            logging.info('****Got {} from MemCache!****'.format(title))
        else:
            movie =  MovieDB.get_by_key_name(movie_id)
            if movie:
                # movie is in MovieDB! PermaLink will work!
                return True
            else:
        
                # this is a new query. Let's find it on TheMovieDb.org!
                init_movie() # sets api key, etc
                try:
                    poster,movie_id,dead,alive,ages = get_cast_data(title,year)
                except:
                    # No Cast, no Cast with bdays and bios, or no movie found
                    return False
                num = len(alive) + len(dead)
                # actuarize the ages
                valdic = actuary_valdic(ages)
                datadic = dict(movie_title = title,
                               poster = poster,
                               movie_id = movie_id,
                               dead = dead,
                               alive = alive,
                               num = num)
                moviedic = dict(valdic.items() + datadic.items())
                memcache.set('movie_' + str(movie_id), moviedic)
                pickled_moviedic = pickle.dumps(moviedic)
                this_movie = MovieDB(key_name = str(movie_id),
                                     movie_id = str(movie_id),
                                     movie_data = pickled_moviedic)
                this_movie.put()
                logging.info('****Added {} to the MovieDB!****'.format(title))
        
        # return python dict with ALL data for rendering page
        return moviedic
    
    def get_moviedic(self, movie_id):
        """For PermaLink Purposes:
                Gets movie from memcache, then db.
                If neither: movie doesn't exist yet. 
                    Returns None.
        """
        moviedic = memcache.get('movie_' + movie_id)
        if not moviedic:
            movie =  MovieDB.get_by_key_name(movie_id)
            if movie:
                logging.info('***Got the movie with id {} from MovieDB!***'.format(movie_id))
                pickled_moviedic = movie.movie_data
                moviedic = pickle.loads(pickled_moviedic)
                return moviedic
            else:
                return None
        logging.info('***Got the movie with id {} from memcache!***'.format(movie_id))    
        return moviedic


###############################################
### Movie Form Handler
###############################################

class MVFormHandler(MVBaseHandler):
    def get(self):
        message = 'Enter the title of a Movie'
        self.render('mv-form.html', message = message)
    
    def post(self):
        moviestr = self.request.get('moviestr')
        year = self.request.get('year')
        movie_id = self.request.get('movie_id')
        if movie_id:
            url = get_first_mov_url(moviestr, year, movie_id)
            logging.info('***GOT URL FOR {} FROM THE SELECTED DATA!***'.format(moviestr))
        else:
            init_movie()
            url = get_first_mov_url_noyear(moviestr)
            logging.info('***TRIED TO GET URL FOR {} FROM RAW DATA!***'.format(moviestr))
        if url:
            self.redirect(url)
        else:
            self.render('oops-movie.html',
                        movie = moviestr,
                        movie_id = movie_id)
        
###############################################
### Movie Actuarized Handler
###############################################

# At BaseHandler write function that gets movie data easiest to hardest
# Add Update funct that updates if movie needs updating?
class MVActuarizedHandler(MVBaseHandler):
    def get(self):
        title = self.request.get('movie')
        year = self.request.get('year')
        movie_id = self.request.get('movie_id')
        if not title:
            # Someone hit this page in error or for some other reason, there was no title...
            self.redirect('/tmdb-form')
            return
        
        movie = self.get_movie(movie_id, title, year)
        
        ################################################################
        ### Tries to find movie in memcache, db, then looks up via script.
        ### Adds to db if found and returns True
        ### Returns False if error
        ################################################################
        
        if movie:
            # get_movie returned True, so the moviedic is in DB keyed with movie_id and finding with ID is possible
            
            self.redirect('/tmdb-actuarized/' + movie_id)
        else:
            # There was an error parsing the Movie Data. 
            # get_movie returned False
            self.render('oops-movie.html',
                        movie=title,
                        movie_id = movie_id)

###############################################
### Movie Actuarized Permalink Handler
###############################################        
        
class MVActuPermaLinkHandler(MVBaseHandler):      
    def get(self, movie_id):
        moviedic = self.get_moviedic(movie_id)
        if moviedic:
#            self.write(moviedic)
            post_url = '/mv-post/' + movie_id + '?' + urlencode(dict(title=moviedic['movie_title'],
                                                                     poster=moviedic['poster']))
            self.render('actuarized-mv.html', 
                        post_url=post_url,
                        **moviedic)
        else:
            backlink = '/tmdb-form'
            self.render('oops-fb.html',
                        type = 'movie',
                        backlink = backlink)
            
##################################################
### MV Posting Handler (handles login for Posting to Facebook!)
##################################################

class MVPostLoginHandler(MVBaseHandler):
    def get(self, movie_id):
        self.logout()
        name = self.request.get('name')
        template = 'fb-postlogin.html'
        redirect_url = '/mv-post/' + movie_id
        self.render(template, 
                    url=redirect_url,
                    name=name)

##################################################
### MV Posting Handler (handles Posting to Facebook!)
##################################################

class MVPostHandler(MVBaseHandler):
    def get(self, movie_id):
        name = self.request.get('title')
        poster = self.request.get('poster')
        if name:
            updated = self.updated_post_session(name)
            if not updated:
                # Edit for Movie's Sake
                attachment = {"name": "{} has been Actuarized!".format(name),
                              "link": "http://actuarize.appspot.com/tmdb-actuarized/" + movie_id,
                              "caption": "Actuarize your favorite movies!",
                              "description": "Click here for some disturbing data about {}...".format(name),
                              "picture": poster}
                
                self.session['post'] = dict(name=name,
                                            attachment=attachment)
            
        user = self.current_user
        if user and self.authed_user(user):
            backlink = "/tmdb-actuarized/" + movie_id
            self.render('fb-post.html',
                        backlink = backlink,
                        name = name)
        else:
            self.redirect('/mv-postlogin/' + movie_id + '?' + urlencode(dict(name=name)))
            
    def post(self, movie_id):
        user = self.current_user
        if user:
            session = self.session.get('post')
            attachment = session['attachment']
            name = session['name']
            message = self.request.get('message')
            uid = user['id']
            try:
                graph = self.init_graph(user['access_token'])
                graph.put_wall_post(message, attachment)
                self.redirect('/mv-posted/' + movie_id + '?' + urlencode(dict(uid=uid,
                                                                              title=name)))
            except:
                self.redirect('/mv-postlogin/' + movie_id + '?' + urlencode(dict(name=name)))
        else:
            self.redirect('/mv-postlogin/' + movie_id)
            

##################################################
### MV Posted Handler (Link has been posted. Link to fbpage)
##################################################

class MVPostedHandler(MVBaseHandler):
    def get(self, movie_id):
        fb_id = self.request.get('uid')
        title = self.request.get('title')
        backlink = "/tmdb-actuarized/" + movie_id
        self.render('fb-posted.html',
                    backlink=backlink,
                    fb_id=fb_id,
                    name=title)

            

        
        
        
        