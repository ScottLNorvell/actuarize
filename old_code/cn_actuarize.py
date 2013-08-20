from base import BaseHandler
from actuary_fb import actuary_valdic
from cn_download import init_congress, get_by_state, get_congress_data, get_by_party


class CNFormHandler(BaseHandler):
    def get(self):
        message = 'Soon you will be able to Actuarize members of Congress...'
        self.render('coming-soon.html', message=message)
    
    
    
    
#    def get(self):
#        self.render('cn-form.html')
#    
#    def post(self):
#        state = self.request.get('state').upper()
#        party = self.request.get('party').upper()
#        init_congress()
#        if state:
#            cong_list = get_by_state(state)
#        else:
#            cong_list = get_by_party(party)
#        ages,cong_info = get_congress_data(cong_list)
#        cong_dict = actuary_valdic(ages)
#        cong_dict['cong_info'] = cong_info
#        cong_dict['num'] = len(cong_info)
#        self.render('actuarized-cn.html', **cong_dict)


class CNActuarizedHandler(BaseHandler):
    pass
    