from base import BaseHandler

###############################################
### prints out pics of FB users 
###############################################


fbids = ['michelle.wolf.90', 
         'wimsy',
         'melanie.lahti',
         'scottlnorvell']

class FbTest(BaseHandler):
    def get(self):
        #tweak fb_page to include my id?
        self.render('base2.html', fbids=fbids)
        

