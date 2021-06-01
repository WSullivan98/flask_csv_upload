from flask import Flask, render_template, request, redirect, url_for
import sys
import os
from os.path import join, dirname, realpath


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import pickle 
#import mysql.connector
import psycopg2
from sqlalchemy import create_engine

from datetime import date

import base64
from insights import process_data, customer_cohort_data, customer_cohort_chart 

app = Flask(__name__)
app.config["DEBUG"] = True 

# Set up Upload folder
UPLOAD_FOLDER = 'static/files/'
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


@app.route('/upload_project', methods=['POST'])
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
    return render_template('upload_project.html', firm_name=firm_name)
  


# Get the upload files
@app.route("/insights", methods=["GET" , 'POST'])
def uploadFiles():
    # get the uploaded file
    firm_name = str(request.form.get('firm_name'))
    project_name = str(request.form.get('project_name'))
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        filename=os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        new_name = firm_name +'_'+project_name + '.csv'
        # os.rename(filename, new_name)
        filePath = app.config['UPLOAD_FOLDER']+new_name
        uploaded_file.save(filePath)
        #save the file

        df = process_data(filePath)
        print(df.head(), file=sys.stderr)
    return df

def plotview():
    # https://gitlab.com/snippets/1924163
    # Generate Plot
    fig= figure()
    annual_sales = df.groupby('inv_year')['Revenue'].sum()
    sales_cohort_data = customer_cohort_data(df)
    years = sales_cohort_data.columns.to_list()
    y={}
    for yr in sales_cohort_data.index.to_list():
        y[yr] =sales_cohort_data.loc[yr].to_list()
    
    fig, ax = plt.subplots(figsize=(12,10))
    x = years
    ax.plot(annual_sales, color='blue',linewidth=2)
    ax.stackplot(years, y.values(), labels=y.keys())
    ax.legend(loc='upper left', fontsize=16)
    ax.set_title('Sales by Customer Cohort Year', fontsize=16)
    ax.set_xlabel('Years', fontsize=16)
    ax.set_ylabel('Sales ($000,000)',fontsize=16)
    plt.yticks(np.arange(0, 15000000, 2000000), labels=['0','2m', '4m', '6m', '8m', '10m', '12m', '14m'], fontsize=16)
    plt.xticks(fontsize=16)

    # Convert plot to PNG image
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)

    return render_template('dataviz.html', firm_name=firm_name, project_name=project_name, image=pngImageB64String)



  



# def parseCSV(filePath):
#     # CSV Column Names
#     col_names = ['first_name', 'last_name', 'address', 'street', 'state', 'zip']
#     # use Pandas to parse the CSV file
#     csvData = pd.read_csv(filePath, names=col_names, header=None)
#     # loop through the Rows
#     for i, row in csvData.iterrows():
#         sql = "INSERT INTO addresses (first_name, last_name, address, street, state, zip) VALUES (%s, %s, %s, %s, %s, %s)"
#         value = (row['first_name'],row['last_name'],row['address'],row['street'],row['state'],str(row['zip']))
#         mycursor.execute(sql, value, if_exists='append')
#         mydb.commit()
#         print(i,row['first_name'],row['last_name'],row['address'],row['street'],row['state'],row['zip'])
            

@app.route("/dataviz", methods=['POST']) #eventually /firm_name/project_name/insights
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

