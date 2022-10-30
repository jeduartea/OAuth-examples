# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, request, session

from app import app, oauth, google
from auth_decorator import login_required

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_404.html'), 404


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/main')
@login_required
def main():
    email = dict(session)['profile']['email']
    name = dict(session)['profile']['name']
    url_picture = dict(session)['profile']['name']
    return render_template('main.html',email=email,name=name,url_picture=url_picture)

@app.route('/login', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/login_google', methods=['GET'])
def login_google():
        #google = oauth.create_client('google')  # create the google oauth client
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scope
    #resp.raise_for_status()
    user_info = resp.json()
    #user =google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    print(session['profile'])
    #session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/main')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login'))
