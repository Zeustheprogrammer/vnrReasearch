from flask import Flask, flash, render_template, request, redirect, url_for, session, g
import requests
import json
import os


import sqlite3

app= Flask(__name__)






@app.before_request
def before_request():
    g.firstname = None

    if 'firstname' in session:
        g.firstname = session['firstname']
  
@app.route('/',methods =['GET', 'POST'])
def home():
    if request.method == 'POST':
            type = request.form['type']
            when = request.form['when']
            conn = sqlite3.connect("mydb.db")
            c = conn.cursor()
            query = ""
            if(type):
                if when:
                    query= f"SELECT * FROM Publications where Indexing = ? and date=?;"
                    c.execute(query,(type,when))
                else:
                    query= f"SELECT * FROM Publications where Indexing = ?;"
                    c.execute(query,(type))

            else:
                if when:
                    query =f"SELECT * FROM Publications where date= ? ;"
                    c.execute(query(when))

                else:
                    query = f"SELECT * FROM Publications;"
                    c.execute(query)

            tmplist = c.fetchall()
            conn.commit()
            conn.close()
            return render_template('index.html', data= tmplist)
    return render_template('index.html')
    

@app.route('/login',methods =['GET', 'POST'])
def login():
    return render_template('login.html')

   



    
@app.route('/registerhg', methods =['GET', 'POST'])
def registerhg():
    if request.method == 'POST':
        conn = sqlite3.connect("C:\\Users\\abboj\\OneDrive\\Desktop\\job-recommender-main\\likhijr.db")
        c = conn.cursor()
        name= request.form['name']
        city= request.form['city']
        address= request.form['address']
        noofrooms= request.form['noofrooms']
        rent= request.form['rent']
        contact= request.form['contact']
        c.execute(f"INSERT INTO housing (name,city,address,noofrooms,rent,contact) values ('{name}','{city}','{address}','{noofrooms}','{rent}','{contact}');")
        conn.commit()
        conn.close()
        flash("Details added successfully", category='success') 
        return render_template('index.html')
    else:
        return render_template('housingregister.html')


@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('firstname', None)
   g.firstname= None
  
   return redirect(url_for('home')) 


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0',debug = True,port = 8080)