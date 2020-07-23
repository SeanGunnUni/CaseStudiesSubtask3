import os
import tempfile

import pytest

from flaskr import flaskr


@pytest.fixture
def client():
    db_fd, flaskr.app.config['BACKEND'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['BACKEND'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/get_patients')
    assert b'Entries here so far' in rv.data

def genData():
    return client.post('/gen_data',follow_redirects=True)

def test_gen_Data():
    """Make sure gen Data works."""
    genData()
    rv = client.get('/get_patients/')
    temp = rv.data
    assert b'Entries here so far' in temp

def test_get_Patient_1():
    """Make sure it gets the correct patient"""
    send_record_numbered(1)
    rv = client.get('/get_patients/1')
    assert b'Patient 1 is in the database' in rv.data

def send_record():
    row = {
        "Date" : datetime.now(),
        "Patient_ID" : 7,
        "Calories_Burned" : randint(1600, 3000) ,
        "Steps_Taken" : randint(1000, 8000),
        "Minutes_Slept" : randint(300, 600),
        "BPM": randint(60, 100),
        "Systolic": randint(120, 180),
        "Diastolic": randint(80, 120),
        "Floors_Climbed": randint(2, 14),
        "Height": randint(140, 185),
        "Weight": randint(55, 90),
        "Comments": "",
    }
    return client.post('/send_record',row,follow_redirects=True)

def send_record_numbered(number):
    row = {
        "Date" : datetime.now(),
        "Patient_ID" : number,
        "Calories_Burned" : randint(1600, 3000) ,
        "Steps_Taken" : randint(1000, 8000),
        "Minutes_Slept" : randint(300, 600),
        "BPM": randint(60, 100),
        "Systolic": randint(120, 180),
        "Diastolic": randint(80, 120),
        "Floors_Climbed": randint(2, 14),
        "Height": randint(140, 185),
        "Weight": randint(55, 90),
        "Comments": "",
    }
    return client.post('/send_record',row,follow_redirects=True)


def test_getRecord():
    """Make sure it gets the correct patients record"""
    send_record()
    rv = client.get('/patientlog/7')
    assert b'Patients 7 data is in the database' in rv.data