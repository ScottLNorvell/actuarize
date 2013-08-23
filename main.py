
import webapp2
from webapp2_extras import sessions

from index import Index
from nl_actuarize import ActuaryNoLogin
from fb_actuarize import FBActuarizedHandler, FBLoginHandler, FBActuPermaLinkHandler, FBPostHandler, FBPostedHandler, FBPostLoginHandler
from mv_actuarize import MVActuarizedHandler, MVFormHandler, MVActuPermaLinkHandler, MVPostHandler, MVPostedHandler, MVPostLoginHandler
from api_handlers import MVAPIHandler, ActuAPIHandler, GraphActuHandler, ActuSliderHandler, StatusLightboxHandler
from base import TestHandler
from facebook_secrets import FB_SECRETS 

config = {}
config['webapp2_extras.sessions'] = dict( secret_key = FB_SECRETS['cookie_key'] )

ID_RE = '([0-9]+)'
       
app = webapp2.WSGIApplication([('/', Index),
                               ('/act', ActuaryNoLogin),
                               ('/fblogin', FBLoginHandler),
                               ('/fbactuarized', FBActuarizedHandler),
                               ('/fbactuarized/' + ID_RE, FBActuPermaLinkHandler),
                               ('/tmdb-form', MVFormHandler),
                               ('/tmdb-actuarized', MVActuarizedHandler),
                               ('/tmdb-actuarized/' + ID_RE, MVActuPermaLinkHandler),
                               ('/tmdb-api', MVAPIHandler),
                               ('/actuary-api', ActuAPIHandler),
                               ('/actu-slider', ActuSliderHandler),
                               ('/actu-graph', GraphActuHandler),
                               ('/status-lightbox', StatusLightboxHandler),
                               ('/fb-post/' + ID_RE, FBPostHandler),
                               ('/fb-posted/' + ID_RE, FBPostedHandler),
                               ('/fb-postlogin/' + ID_RE, FBPostLoginHandler),
                               ('/mv-post/' + ID_RE, MVPostHandler),
                               ('/mv-posted/' + ID_RE, MVPostedHandler),
                               ('/mv-postlogin/' + ID_RE, MVPostLoginHandler),
                               ('/test', TestHandler)],
                                debug=True,
                                config=config)
