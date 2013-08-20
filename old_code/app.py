import os
from fb_download import *
from actuary_fb import *
from flask import Flask, redirect, render_template
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)
app.config['BOOTSTRAP_USE_CDN'] = True

@app.route('/')
def index():
    auth_vals = get_authvals_csv('auth_keys.csv')
    auth_url = fb_oauth_init(auth_vals)
    return redirect(auth_url)
    
@app.route('/stats/')
def stats():
    #deleteable
    auth_vals = get_authvals_csv('auth_keys.csv')
    access_token = fb_oauth_final(auth_vals)
    write_authvals_csv(auth_vals,'auth_keys.csv')
    friends_data = get_friends_fql(auth_vals)
    fflist = filter_friends(friends_data)
    output_str, num = extract_age_sex_str(fflist)
    analysis_str = print_actuary(output_str)
    return render_template('template.html', analysis_str=analysis_str, num=num)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug=True
    app.run(host='0.0.0.0', port=port)
