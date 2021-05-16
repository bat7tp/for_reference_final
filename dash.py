import sqlite3 as lite
import sys

con = lite.connect('C:/Users/batsh/Documents/IS 211/IS211_Final_Project/sql_database_final.db.')

with con:
        cur = con.cursor()

        cur.execute(""" CREATE TABLE titles (
                                              title_id integer PRIMARY KEY,
                                                title text NOT NULL

                                            ); """
                    )
        cur.execute(""" CREATE TABLE dates (
                                                date_id integer PRIMARY KEY,
                                                   publication_date integer NOT NULL

                                               ); """
                    )

        cur.execute(""" CREATE TABLE authors (
                                                        author_id integer PRIMARY KEY,
                                                           name text NOT NULL

                                                       ); """
                    )
