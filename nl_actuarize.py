from base import BaseHandler
from actuary_fb import actuary_valdic, neg_fems, pos_males

        
###############################################
### class to handle no login fun test
###############################################

class ActuaryNoLogin(BaseHandler):
    def get(self):
        self.render('fb-form.html')
    
    def post(self):
        males = self.request.get('males')
        females = self.request.get('females')
        try:
            ages = neg_fems(females) + pos_males(males)
        except:
            self.render('oops-nl.html')
            return
        data = actuary_valdic(ages)
        self.render('actuarized-nl.html', **data)
        
        
        