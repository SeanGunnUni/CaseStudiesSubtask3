import flask
from flask import Flask, send_from_directory, render_template, request, redirect, url_for
import pandas as pd
from random import randint, choice
from datetime import datetime
app = Flask(__name__,)
# prevent caching
app.config["CACHE_TYPE"] = "null"


# returns a json responce of the list of patients
@app.route('/get_patients')
def get_patients():
    df = pd.read_csv("patients.csv")
    return df.to_json(orient="split")

# generates random fields for patient 0
@app.route('/gen_data')
def gen_data():
    records = pd.read_csv("records.csv")
    # a random choice is selected from here for the comments field
    choices = ["", "", "", "", "", "had bad back", "has weird mole"]
    row = {
        "Date" : datetime.now(),
        "Patient_ID" : 0,
        "Calories_Burned" : randint(1600, 3000) ,
        "Steps_Taken" : randint(1000, 8000),
        "Minutes_Slept" : randint(300, 600),
        "BPM": randint(60, 100),
        "Systolic": randint(120, 180),
        "Diastolic": randint(80, 120),
        "Floors_Climbed": randint(2, 14),
        "Height": 170,
        "Weight": 70,
        "Comments": choice(choices),
    }
    records = records.append(row, ignore_index=True)
    records.to_csv("records.csv", index=False)
    return "Success"

# displays overview of infomation pertaining to the patient passed as argument
@app.route('/patient/<path:path>')
def get_patient(path):
    patients = pd.read_csv("patients.csv")
    records = pd.read_csv("records.csv")
    # get the latest record for given patient in path
    mostRecentRecord = records[records['Patient_ID'] == int(path)].sort_values(by='Date').iloc[-1]
    latestRecord = {
        'Calories_Burned': mostRecentRecord['Calories_Burned'],
        'Steps_Taken': mostRecentRecord['Steps_Taken'],
        'Hours_Slept': float(mostRecentRecord['Minutes_Slept'])/60,
        'BPM': mostRecentRecord['BPM'],
        'Systolic': mostRecentRecord['Systolic'],
        'Diastolic': mostRecentRecord['Diastolic'],
        'Floors_Climbed': mostRecentRecord['Floors_Climbed'],
        'Height': mostRecentRecord['Height'],
        'Weight': mostRecentRecord['Weight'],
    }
    # get the patients info
    patientInfo = patients[patients['UniqueID'] == int(path)].iloc[0]
    patient = {
        'name' : patientInfo['Name'],
        'gender' : patientInfo['Gender'],
        'birthdate' : patientInfo['Birthdate'],
        'address' : patientInfo['Address'],
        'phone' : patientInfo['Phone'],
    }
    return render_template('profile.html', title="Patient", latestRecord=latestRecord, patient=patient, path=path)

# displays a table of the patient data (sensor readings)
@app.route('/patientlog/<path:path>')
def get_patient_log(path):
    patients = pd.read_csv("patients.csv")
    records = pd.read_csv("records.csv")
    # get the latest record for given patient in path
    patientRecords = records[records['Patient_ID'] == int(path)]
    dateList = pd.to_datetime(patientRecords['Date']).tolist()
    dateList = [datetime.strftime(i, "%Y-%m-%d %H:%M") for i in dateList]
    records = {
        'Date': dateList, 
        'Calories_Burned': patientRecords['Calories_Burned'].tolist(),
        'Steps_Taken': patientRecords['Steps_Taken'].tolist(),
        'Hours_Slept': patientRecords['Minutes_Slept'].tolist(),
        'BPM': patientRecords['BPM'].tolist(),
        'Systolic': patientRecords['Systolic'].tolist(),
        'Diastolic': patientRecords['Diastolic'].tolist(),
        'Floors_Climbed': patientRecords['Floors_Climbed'].tolist(),
        'Height': patientRecords['Height'].tolist(),
        'Weight': patientRecords['Weight'].tolist(),
        'Comments': patientRecords['Comments'].tolist(),
    }
    patientInfo = patients[patients['UniqueID'] == int(path)].iloc[0]
    patient = {
        'name' : patientInfo['Name']
    }
    return render_template('patients-log.html', title="Patient Log", records=records, patient=patient, len = len(records['Date']), path=path)

# displays a list of patients
@app.route('/patients')
def get_patient_list():
    return render_template('data.html', title="Patients")

# route for the static files
@app.route('/stat/<path:path>')
def get_static(path):
    return send_from_directory('../', path)

# displays page that allows user to add a record for patient passed as arg
@app.route('/add_record/<path:path>')
def add_record(path):
    return render_template('manualAddingInformation.html', title="Add Record", path=path)

# api to add record to database
# takes a json dict, which corresponds to db values as follows
# {
#         'date' : 'Date',
#         'weight' : 'Weight',
#         'systolic' : 'Systolic',
#         'diastolic' : 'Diastolic',
#         'calories' : 'Calories_Burned',
#         'stepsTaken' : 'Steps_Taken',
#         'hoursSlept' : 'Minutes_Slept',
#         'comments' : 'Comments',
#         'averagePulse' : 'BPM',
#     }
# 
@app.route('/send_record/<path:path>', methods=['POST']) #GET requests will be blocked
def send_patient_data(path):
    records = pd.read_csv("records.csv")
    req_data = request.get_json()
    keyDict = {
        'date' : 'Date',
        'weight' : 'Weight',
        'systolic' : 'Systolic',
        'diastolic' : 'Diastolic',
        'calories' : 'Calories_Burned',
        'stepsTaken' : 'Steps_Taken',
        'hoursSlept' : 'Minutes_Slept',
        'comments' : 'Comments',
        'averagePulse' : 'BPM',
    }
    row = {'Patient_ID': path}
    for i in range(len(req_data['formAnswers'])):
        actualKey = keyDict[req_data['formAnswers'][i]['name']]
        row[actualKey] = req_data['formAnswers'][i]['value']
        print(req_data['formAnswers'][i])
    print(row)
    records = records.append(row, ignore_index=True)
    records.to_csv("records.csv", index=False)
    return "Success"
    
# redirect / to patient page
@app.route('/')
def home():
    return redirect("patients")

# gets stats for patient
@app.route('/patientstats/<path:path>')
def get_stats(path):
    print("test")
    patients = pd.read_csv("patients.csv")
    records = pd.read_csv("records.csv").sort_values(by='Date')
    # get the latest record for given patient in path
    patientRecords = records[records['Patient_ID'] == int(path)]
    dateList = pd.to_datetime(patientRecords['Date']).tolist()
    dateList = [datetime.strftime(i, "%Y-%m-%d %H:%M") for i in dateList]
    records = {
        'Date': dateList, 
        'Calories_Burned': patientRecords['Calories_Burned'].tolist(),
        'Steps_Taken': patientRecords['Steps_Taken'].tolist(),
        'Hours_Slept': patientRecords['Minutes_Slept'].tolist(),
        'BPM': patientRecords['BPM'].tolist(),
        'Systolic': patientRecords['Systolic'].tolist(),
        'Diastolic': patientRecords['Diastolic'].tolist(),
        'Floors_Climbed': patientRecords['Floors_Climbed'].tolist(),
        'Height': patientRecords['Height'].tolist(),
        'Weight': patientRecords['Weight'].tolist(),
        'Comments': patientRecords['Comments'].tolist(),
    }
    patientInfo = patients[patients['UniqueID'] == int(path)].iloc[0]
    patient = {
        'name' : patientInfo['Name']
    }
    caloriesOutput = []
    for i in range(len(records['Date'])):
        caloriesOutput.append({'x': records['Date'][i], 'y': records['Calories_Burned'][i]})
    floorsClimbedOutput = []
    for i in range(len(records['Date'])):
        floorsClimbedOutput.append({'x': records['Date'][i], 'y': records['Floors_Climbed'][i]})
    hoursSleptOutput = []
    for i in range(len(records['Date'])):
        hoursSleptOutput.append({'x': records['Date'][i], 'y': records['Hours_Slept'][i]})
    stepsTakenOutput = []
    for i in range(len(records['Date'])):
        stepsTakenOutput.append({'x': records['Date'][i], 'y': records['Steps_Taken'][i]})
    weightOutput = []
    for i in range(len(records['Date'])):
        weightOutput.append({'x': records['Date'][i], 'y': records['Weight'][i]})
    systolicOutput = []
    for i in range(len(records['Date'])):
        systolicOutput.append({'x': records['Date'][i], 'y': records['Systolic'][i]})
    diastolicOutput = []
    for i in range(len(records['Date'])):
        diastolicOutput.append({'x': records['Date'][i], 'y': records['Diastolic'][i]})
        
        
    return render_template('stats.html', title="Stats", records=records, patient=patient, len = len(records['Date']), path=path, caloriesOutput=caloriesOutput,
    floorsClimbedOutput=floorsClimbedOutput, hoursSleptOutput=hoursSleptOutput, stepsTakenOutput=stepsTakenOutput, weightOutput=weightOutput,
    systolicOutput=systolicOutput, diastolicOutput=diastolicOutput)

@app.route('/sensor_readings/<path:path>')
def get_liveSensorData(path):
    patients = pd.read_csv("patients.csv")
    records = pd.read_csv("records.csv")
    patientRecords = records[records['Patient_ID'] == int(path)].iloc[-1]
    liveSensorReadings = {
        'Calories_Burned': patientRecords['Calories_Burned'].tolist(),
        'Steps_Taken': patientRecords['Steps_Taken'].tolist(),
        'Hours_Slept': patientRecords['Minutes_Slept'].tolist(),
        'BPM': patientRecords['BPM'].tolist(),
        'Systolic': patientRecords['Systolic'].tolist(),
        'Diastolic': patientRecords['Diastolic'].tolist(),
        'Floors_Climbed': patientRecords['Floors_Climbed'].tolist(),
    }
    patientInfo = patients[patients['UniqueID'] == int(path)].iloc[0]
    patient = {
      'name': patientInfo['Name'],
      'gender': patientInfo['Gender'],
      'birthdate': patientInfo['Birthdate'],
      'address': patientInfo['Address'],
      'phone': patientInfo['Phone'],
    }
    return render_template('patients-sensor-readings.html', title="Live Sensor Readings", patientRecords=patientRecords, patient=patient, path=path)
    
app.run()
