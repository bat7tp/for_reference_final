import sqlite3 as lite
import sys

con = lite.connect('C:/Users/batsh/Documents/IS 211/IS211_Final_Project/real_sql_database_final.db')

with con:
    cur = con.cursor()

    cur.execute(""" CREATE TABLE posts (
                                              post_id integer PRIMARY KEY,
                                                title text NOT NULL,
                                                author text NOT NULL,
                                                content text NOT NULL, 
                                                publication_date integer NOT NULL


                                            ); """
                )
