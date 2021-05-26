from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath

import numpy as np
import pandas as pd
import pickle 
#import mysql.connector
import psycopg2
from sqlalchemy import create_engine

app = Flask(__name__)

# enable debugging moade
app.config["DEBUG"] = True 

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Create Database


# Connect Database
conn = psycopg2.connect(database='denver_properties', user="postgres", password='2855Wakonda', host='localhost', port='5432')
# engine = create_engine("postgresql://postgres:galvanize@localhost:5000/csvdata")

cur = conn.cursor()

# # mysql attempt
# mydb = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='csvdata'
# )

# mycursor = mydb.cursor()

# mycursor.execute('SHOW DATABASES')

# View All Database
# for x in mycursor:
#     print(x)

# ROOT URL
@app.route("/")
def index():
    # Set the upload HTMP template '\tempaltes\index.html'
    return render_template('index.html')

# Get the upload files
@app.route("/upload_project", methods=['POST'])
def upload_users():
    first_name = str(request.form['first_name'])
    last_name = str(request.form['last_name'])
    email = str(request.form['email'])
    firm_name = str(request.form['firm_name'])

    query = """INSERT INTO users VALUES (%s, %s, %s, %s)"""

    
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        #save the file
    return redirect(url_for('index'))

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
            


if (__name__ == "__main__"):

    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)

# to run
# $ export FLASK_APP=main
# $ flask run
#  * Running on http://127.0.0.1:5000/
# go to http://127.0.0.1:5000/ in a browseer
# browser displays "Flask CSV filer Uploader and Parser"

