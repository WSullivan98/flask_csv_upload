from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath

import numpy as np
import pandas as pd
import pickle 
#import mysql.connector
import psycopg2
from sqlalchemy import create_engine

from datetime import date


app = Flask(__name__)
app.config["DEBUG"] = True 

# Set up Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Connect Database
conn = psycopg2.connect(database='firm', user="postgres", password='insights', host='localhost', port='5432')
# engine = create_engine("postgresql://postgres:galvanize@localhost:5000/csvdata")

cur = conn.cursor()


# ROOT URL
@app.route("/")
def index():
    # Set the upload HTML template '\tempaltes\index.html'
    return render_template('index.html')


@app.route("/create_user", methods=['POST'])
def create_user():
    return render_template('create_user.html')




# Get the upload files
@app.route("/upload_project", methods=['POST'])
def uploadFiles():
    upload_users()
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        #save the file
    return redirect(url_for('dataviz'))

def upload_users():
    first_name = str(request.form.get('first_name'))
    last_name = str(request.form.get('last_name'))
    email = str(request.form.get('email'))
    firm_name = str(request.form.get('firm_name'))

    cur.execute('''SELECT COUNT(*)
                   FROM users''')
    firm_users = cur.fetchone()

    query = """
        INSERT INTO users (
            user_id,
            first_name,
            last_name,
            email,
            created_date
        ) VALUES (%s, %s, %s, %s, %s)"""

    cur.execute(query, (
        firm_users[0]+1, 
        first_name,
        last_name,
        email,
        date.today())
        )
    conn.commit()

    


def parseCSV(filePath):
    # CSV Column Names
    col_names = ['first_name', 'last_name', 'address', 'street', 'state', 'zip']
    # use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    # loop through the Rows
    for i, row in csvData.iterrows():
        sql = "INSERT INTO addresses (first_name, last_name, address, street, state, zip) VALUES (%s, %s, %s, %s, %s, %s)"
        value = (row['first_name'],row['last_name'],row['address'],row['street'],row['state'],str(row['zip']))
        mycursor.execute(sql, value, if_exists='append')
        mydb.commit()
        print(i,row['first_name'],row['last_name'],row['address'],row['street'],row['state'],row['zip'])
            

@app.route("/dataviz", methods=['POST']) #eventually /firm_name/project_name
def dataviz():
    return render_template('dataviz.html')



if (__name__ == "__main__"):

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)




# to run
# $ export FLASK_APP=main
# $ flask run
#  * Running on http://127.0.0.1:5000/
# go to http://127.0.0.1:5000/ in a browseer
# browser displays "Flask CSV filer Uploader and Parser"

