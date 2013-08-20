from tmdb_download import init_movie, get_autocomp_movies
from mv_actuarize import MVBaseHandler
from base import BaseHandler
import pickle
from actuary_fb import get_proball_data, get_probany_data, get_prob_percentages
import logging

##################################################
### Movie Api Handler for autocomplete! 
##################################################

class MVAPIHandler(MVBaseHandler):
    def get(self):
        term = self.request.get('term')
        init_movie()
        results = get_autocomp_movies(term,10)
        self.write(results)
        
class ActuAPIHandler(BaseHandler):
    def get(self):
        pickled_ages = self.request.get('ages')
        prob = self.request.get('prob')
        logging.info('***prob = {}***'.format(prob))
        ages = pickle.loads(pickled_ages)
        if prob == 'any':
            data = get_probany_data(ages)
        else:
            data = get_proball_data(ages)
        self.write(data)

class ActuSliderHandler(BaseHandler):
    def get(self):
        pickled_ages = self.request.get('ages')
        years = self.request.get('years')
        ages = pickle.loads(pickled_ages)
        data = get_prob_percentages(ages,int(years))
        self.write(data)
        
class GraphActuHandler(BaseHandler):
    def get(self):
        self.render('actu-graph.html')
        
class StatusLightboxHandler(BaseHandler):
    def get(self):
        self.render('status-lightbox.html')