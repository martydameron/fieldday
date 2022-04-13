import cs304dbi as dbi

# all functions used for clubs
# used to get list of all club's sid a user is envolved in
def involved_clubs(conn, uid):
    curs = dbi.dict_cursor(conn)
    sql = ('''select club from user where uid = %s;''')
    curs.execute(sql, [uid])
    return curs.fetchall()

# used to get name of club from sid
def club_names(conn, club):
    curs = dbi.dict_cursor(conn)
    sql = ('''select sport from sport where sid = %s;''')
    curs.execute(sql, [club])
    return curs.fetchone()

# gets list of all club names
def all_club(conn):
    curs = dbi.dict_cursor(conn)
    sql = ('''select * from sport;''')
    curs.execute(sql)
    return curs.fetchall()

# all functions for users
# gets all information about user with certain uid
def current_user(conn, uid):
    curs = dbi.dict_cursor(conn)
    sql = ('''select * from user where uid = %s;''')
    curs.execute(sql, [uid])
    return curs.fetchone()

# gets a list of all the users besides the current one
def all_users_NOT_current(conn, uid):
    curs = dbi.dict_cursor(conn)
    sql = ('''select uid, firstname, lastname, admin from user where uid != %s;''')
    curs.execute(sql, [uid])
    return curs.fetchall()

# functions for inserting data from settings page
# updates a user's firstname based on uid
def update_first_name(conn, uid, first):
    curs = dbi.dict_cursor(conn)
    sql = ('''update user set firstname = %s where uid = %s;''')
    curs.execute(sql, [first, uid])
    conn.commit()

# updates a user's lastname based on uid
def update_last_name(conn, uid, last):
    curs = dbi.dict_cursor(conn)
    sql = ('''update user set lastname = %s where uid = %s;''')
    curs.execute(sql, [last, uid])
    conn.commit()

# updates a user's password based on uid
def update_password(conn, uid, password):
    curs = dbi.dict_cursor(conn)
    sql = ('''update user set password = %s where uid = %s;''')
    curs.execute(sql, [password, uid])
    conn.commit()

# updates a users admin status
def update_admin(conn, admin_uid):
    curs = dbi.dict_cursor(conn)
    sql = ('''update user set admin = 1 where uid = %s;''')
    curs.execute(sql, [admin_uid])
    conn.commit()

# updates the list of sid's in a users clubs attribute
def update_teams(conn, uid, team):
    curs = dbi.dict_cursor(conn)
    sql = ('''update user set club = %s where uid = %s;''')
    curs.execute(sql, [team, uid])
    conn.commit()

# gets the sid of a team based on the name
# used in conjunction with update_teams to delete memberships
def get_sid(conn, team):
    curs = dbi.dict_cursor(conn)
    sql = ('''select sid from sport where sport = %s;''')
    curs.execute(sql, [team])
    return curs.fetchone()
