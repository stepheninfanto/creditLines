from flask import Flask,flash, render_template,request,jsonify,redirect,url_for
import json
from werkzeug.utils import secure_filename
from constants import *
from utils import *
from sqlalchemy import func , DateTime
from sqlalchemy.dialects.postgresql import JSON
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import csv

with open('MSME-CreditLine.txt', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
        line_count += 1
    print(f'Processed {line_count} lines.')

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:sql@localhost:5432/postgres"
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class creditRating(db.Model):
    """Model for the stations table"""
    __tablename__ = 'creditRating'
    id = db.Column(db.Integer, primary_key = True)
    CompanyName = db.Column(db.Float)
    RequestData = db.Column(JSON)
    ZScoreData = db.Column(JSON)
    ZScoreOutput = db.Column(JSON)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), onupdate=func.now())
    
def __init__(self,CompanyName,RequestData,ZScoreData,ZScoreOutput,time_created,time_updated):
        self.CompanyName = CompanyName
        self.RequestData=RequestData
        self.ZScoreData=ZScoreData
        self.ZScoreOutput=ZScoreOutput
        self.time_created=time_created
        self.time_updated=time_updated

@app.route('/dashboard/<company_name>',methods=["GET"])
def companyDashboarddata(company_name:str):
    try:
        if db.session.query(creditRating).filter("CompanyName"==company_name):
                print("f Record Exist in the DB")
                data = creditRating.query.filter(creditRating.CompanyName==company_name).order_by(-creditRating.id).limit(2).all()
                print(data)
        resp_data = {"Q1": data[0].RequestData ,"Q2": data[1].RequestData}
    except Exception as e:
        print(f"Error Occurred :{e}")
    return jsonify(resp_data)


@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")



@app.route("/data",methods=["GET"])
def dashboard():
    return render_template("data.html")




@app.route("/upload_financial_statements",methods=["POST"])
def upload_doc():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      flash('File Uploaded Sucessfully .', 'success')
      return render_template("index.html")



@app.route('/credit_rate_engine', methods=['POST'])
def credit_rate_engine():
    try:
        request_data = json.loads(request.data)
        print((len(set(REQUIRED_PARAMETER_LIST) - set(request_data.keys()))== 0))
        if request_data and len((set(REQUIRED_PARAMETER_LIST) - set(request_data.keys())))== 0:
            try:
                if db.session.query(creditRating).filter("CompanyName"==request_data["CompanyName"]):
                    print("f Record is Already Present in the DB")
                    data = creditRating.query.filter(creditRating.CompanyName==request_data["CompanyName"]).first()
                    data = data.ZScoreOutput
                    data.update({"message":"hellos","status":200})
                    resp = jsonify(data) , 200
            except :
                resp_data = ZScore(request_data)
                try:
                    credit_rate = creditRating(RequestData = request_data,ZScoreData = resp_data["ZScore_calculation"],ZScoreOutput= resp_data["finance_data"],CompanyName=request_data["CompanyName"])
                    db.session.add(credit_rate)
                    db.session.commit()
                except Exception as e:
                    print(f"error {e}")
                resp_data["finance_data"].update({"message": "", "status": 200})
                resp = jsonify(data=resp_data["finance_data"]), 200
        else:
            return jsonify(data={"message": "Please Provide All the Data required", "status": 400}), 400
    except ValueError :
        resp = jsonify(data={"message":"Empty request body is not acceptable","status":400}),400
    except Exception as e:
        print(f"Error Occurred :{e}")
        resp = jsonify(data={"financial_ratio":[],"credit_worth":"","message":"Something Went Wrong. Please Contact "
                                                                              "Administrator"}), 500
    return resp



if __name__ == "__main__":
    app.run()