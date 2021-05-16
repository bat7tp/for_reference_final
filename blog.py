from flask import Flask, render_template, redirect, request, session, g
import sqlite3 as lite
import sys

import os

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __actual__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Batsheva', password='password'))
print(users)
app = Flask(__name__)

app.secret_key = 'asecretkeythatnobodyknows'

posts = [

    {
        'title': 'Blog Post 1',
        'date_published': 'April 6, 2021',
        'author': 'Batsheva Paul',
        'content': 'stuff'
    },

]

@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

def db_connection():
    conn = None
    try:
        conn = lite.connect('real_sql_database_final.db')
        print("connected")
    except lite.error as e:
        print(e)
    return conn

@app.route("/")
def open_post():
    print("in posting fxn")
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * from posts")
    blog_posts = cursor.fetchall()
    print("successfully posted")
    return render_template('home.html', posts=posts, blog_posts=blog_posts)

@app.route("/dashboard")
def dash():
    print("in dash fxn")
    conn = db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * from posts")
    list_title = cursor.fetchall()
    print("successfully received existing posts")

    return render_template("dashboard.html", list_title=list_title)

@app.route("/add" , methods = ['POST', 'GET'])
def add():

    print("in add fxn")
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        print("in method")
        try:
            print("in try")
            title = request.form["book_title"]
            author = request.form["author_name"]
            content = request.form["content"]
            publication_date = int(request.form["date"])
            print(title)
            print(author)
            print(content)
            cursor.execute("INSERT INTO posts (title, author, content, publication_date) VALUES (?, ?, ?, ?)", [title,
                                                                                                                author, content, publication_date])
            conn.commit()
            print("Title successfully added")
        except lite.Error as e:
            # conn.rollback()
            print(e)

    return redirect('/dashboard')

@app.route("/edit/<postid>" , methods = ['POST', 'GET'])
def edit(postid):
    print("in edit fxn")
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * from posts WHERE post_id = ?", [postid])
        post_stuff = cursor.fetchall()[0]

        return render_template("edits.html", post_stuff=post_stuff)

    if request.method == "POST":
        print("in method")
        try:
            print("in try")
            edited_title = request.form["edit_book_title"]
            edited_author = request.form["edit_author_name"]
            edited_content = request.form["edit_content"]
            edited_date = request.form["edit_date"]

            print(edited_title)
            print(edited_author)
            print(edited_content)
            print(edited_date)

            if edited_date != "":
                cursor.execute("UPDATE posts SET publication_date = ? WHERE post_id = ?", [edited_date, postid])
                conn.commit()
                print(" date Edits successful")

            if edited_content != "":
                cursor.execute("UPDATE posts SET content = ? WHERE post_id = ?", [edited_content, postid])
                conn.commit()
                print("content Edits successful")

            if edited_author != "":
                cursor.execute("UPDATE posts SET author = ? WHERE post_id = ?", [edited_author, postid])
                conn.commit()
                print("author Edits successful")

            if edited_title != "":
                cursor.execute("UPDATE posts SET title = ? WHERE post_id = ?", [edited_title, postid])
                conn.commit()
                print("title Edits successful")

        except lite.Error as err:
            # conn.rollback()
            print(err)

    return redirect("/dashboard")


@app.route("/delete/<delid>", methods=['POST', 'GET'])
def delete(delid):
    print("in delete fxn")
    conn = db_connection()
    cursor = conn.cursor()


    if request.method == "POST":
        print("in method")
        try:
            print("in try")
            cursor.execute("DELETE FROM posts WHERE post_id = ?", [delid])
            print(delid)
            conn.commit()
            print("Deletes successful")
        except lite.Error as err:
            print(err)

    return redirect("/dashboard")


@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
    session.pop('user_id', None)
    username = request.form['username']
    password = request.form['password']

    user = [x for x in users if x.username == username][0]
    if user and user.password == password:
        print("work?")
        session['user_id'] = user.id
        return redirect('/dashboard')
    return redirect('login')


   return render_template('login.html')



# @app.route("/login", methods = ["POST"])
# def login():
#
#     if request.method == 'POST':
#         un = request.form['username']
#         pswd = request.form['password']

    # query1 = "SELECT username, password From Users WHERE username = {n_un} and password = {n_pswd}".format(n_un = un, n_pswd = pswd)
    #
    # #sqlconnection here
    # rows = cursor.execute(query1)
    # rows = rows.fetchall()

    # if len(rows) ==1:
    #     return render_template(login.html)
    # else:
    #     return redirect("/register")
    # return render_template("login.html")

# @app.route("/register", methods = ["GET", "POST"])
# def registration_page():
#     if request.method == "POST":
#         new_UN = request.form['new_username']
#         new_PSWD = request.form['new_password']
#         #SQLconnection
#         # query1 = "INSERT into Users VALUES('{u}', '{p}'".format(u = new_UN, p = new_PSWD)
#         # cursor.execute(query)
#         # connection.commit()
#         #
#         # return redirect('/') #redirect to the login page
#     return render_template("register.html")

#
#


if __name__ == '__main__':
    app.run(debug=True)