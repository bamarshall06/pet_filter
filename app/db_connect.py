import pymysql
import pymysql.cursors
from flask import g

def get_db():
    if 'db' not in g or not is_connection_open(g.db):
        print("Re-establishing closed database connection.")
        g.db = pymysql.connect(
            # Database configuration
            # Configure MySQL
            host = 'q68u8b2buodpme2n.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user = 'xwayhvlpud157l8t',
            password = 'b2nc4d7v4eabgvng',
            database = 'x5wodl0pyke6ik8e',
            cursorclass=pymysql.cursors.DictCursor  # Set the default cursor class to DictCursor
        )
    return g.db

def is_connection_open(conn):
    try:
        conn.ping(reconnect=True)  # PyMySQL's way to check connection health
        return True
    except:
        return False

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None and not db._closed:
        print("Closing database connection.")
        db.close()



