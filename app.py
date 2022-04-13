from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi
import data
import random

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/feed/')
def feed_page():
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    
    #currently displays all posts that have made by every team
    # in alpha, we will have to filter out the posts and only 
    # display posts by teams that the user follows
    curs.execute('''select sport.sport, caption, date from sport, 
    (select * from post) as posts where sid = team''')
    stuff = curs.fetchall()
    return render_template('feed.html', posts=stuff)

#used as backup in case drop menu did not work
#generates a webage with links to each individual sport

# @app.route('/teams/')
# def team_page():
#     conn = dbi.connect()
#     curs = dbi.dict_cursor(conn)
#     curs.execute('''select sid,sport from sport''')
#     stuff = curs.fetchall()
#     return render_template('teams_page.html',sports=stuff)

# if at all possible, using something that's not a set for clubs
# both for updating if more clubs are added however all club adding and delete is set based currently
# need to set action attribute for forms maybe? if not using redirect? ask scott
@app.route('/settings/', methods=["GET", "POST"])
def setting_page():
    # uid assigned for testing
    # once login is implemented, route will be changed to /settings/<uid> and setting_page(uid)
    # so is unique for each user
    uid = 2

    # gets user's name to be displayed
    current_user = data.current_user(conn, uid)

    # gets sids of teams that the user is a member of and turns it into a list where each sid is an item
    teams_list_raw = data.involved_clubs(conn, uid)
    teams_list_useful = teams_list_raw[0]["club"].split(',')

    if (request.method == "POST"):
        result = request.form

        if (result["submit"] == "Submit New First Name"):
            data.update_first_name(conn, uid, result["first"])
            flash('First name has been updated.')
            return redirect(url_for('setting_page'))
        
        elif (result["submit"] == "Submit New Last Name"):
            data.update_last_name(conn, uid, result["last"])
            flash('Last name has been updated.')
            return redirect(url_for('setting_page'))

        # confirm old password & forgot password button in alpha?
        elif (result["submit"] == "Submit New Password"):
            data.update_password(conn, uid, result["new-pass"])
            flash('Password has been updated.')
            return redirect(url_for('setting_page'))

        elif (result["submit"] == "Delete Team"):
            # gets sid of the team the user wants to delete by the name of the team and turns it into a string
            sid = str(data.get_sid(conn, result["team-list"])["sid"])

            # removes the sid from the list and converts the list into a string
            teams_list_useful.remove(sid)
            stri = ",".join(teams_list_useful)

            data.update_teams(conn, uid, stri)
            
            flash('A team has been deleted.')
            return redirect(url_for('setting_page'))
        
        elif (result["submit"] == "Add Team"):
            if (result["team-list"] in teams_list_useful):
                flash('You are already a member of this team.')
                return redirect(url_for('setting_page'))

            else: #(result["team-list"] is not teams_list_useful)
                # adds new team to list of teams the user is a member of
                teams_list_useful.append(str(result["team-list"]))

                # converts list to str so that it can be used in mysql
                stri = ",".join(teams_list_useful)

                data.update_teams(conn, uid, stri)

                flash('You have joined a new team!')
                return redirect(url_for('setting_page'))
        
        # add confirmation pop up through javascript?
        # when finished will redirect to login/signup page
        elif (result["submit"] == "Delete Account"):
            data.delete_account(conn, uid)
            flash('Your account has been deleted.')
            return redirect(url_for(home_page))      
        
        elif (result["submit"] == "Add Admin"):
            data.update_admin(conn, result["new-admin"])
            flash('A new admin has been added')
            return redirect(url_for('setting_page'))
            
    else: # (request.method == "GET"):
        # loops through list of user's clubs' sids and creates a dictionary of the names
        in_team_names = []
        for teams_id in teams_list_useful:
            in_team_names.append(data.club_names(conn, teams_id)["sport"])
        
        # gives list of all club
        all_clubs = data.all_club(conn)

        # gives list all of all users except for the current one
        users = data.all_users_NOT_current(conn, uid)

        return render_template('settings.html', clubs=in_team_names, all_clubs=all_clubs, current_user=current_user, users=users)

@app.route('/teams/<sport_id_number>')
def sport(sport_id_number):
    # uid assigned for testing
    # once login is implemented, route will be changed to /settings/<uid> and setting_page(uid)
    # so is unique for each user
    uid = 1

    current_user = data.current_user(conn, uid)
    name = data.club_names(conn, sport_id_number)["sport"]
    
    return render_template('individual_teamPage.html', name=name, current_user=current_user)


@app.before_first_request
def init_db():
    dbi.cache_cnf()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'fieldday_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

if __name__ == '__main__':
    import sys, os
    dbi.conf('fieldday_db')
    conn = dbi.connect()
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
