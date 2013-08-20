from base import BaseHandler

###############################################
### Super simple Index Handler
###############################################

class Index(BaseHandler):
    def get(self):
        template = 'index.html'
        script = 'index'
        self.render(template,script=script)