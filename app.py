#Import necessary libraries
from flask import Flask, jsonify, request, render_template
import sqlite3
import pickle

#initialization of flask library
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#=========================================Prediction Function==============
@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method=='POST':
        pregnancies = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        blood_pressure = int(request.form['blood-pressure'])
        skin_thickness = int(request.form['skin-thickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        diabetes_pedigree = float(request.form['diabetes-pedigree'])
        age = int(request.form['age'])
        data = [pregnancies,glucose,blood_pressure,skin_thickness,insulin,bmi,diabetes_pedigree,age]
        print(data)
        with open('model.pickle','rb') as file:
            model = pickle.load(file)
        result = model.predict([data])
        print(result)
        if result[0] == 0:
            outcome = 'Negative'
        else:
            outcome = 'Postive'
        print('Data has been inserted')
        return jsonify({'message':outcome})
    else:
        return render_template('predict.html')
#=========================================show patient Function==============

@app.route("/show-patient", methods=['GET','POST'])
def patient_show():
    conn = sqlite3.connect('patient.db')
    cur = conn.cursor()
    cur.execute('select * from PATIENT_DETAILS')
    #print(cur.fetchall())
    data=[]
    for i in cur.fetchall():
        patient={}
        patient['patient_name'] = i[0]
        patient['patient_age'] = i[1]
        patient['gender'] = i[2]
        patient['diabetic'] = i[3]
        data.append(patient)
    print(data)
    return render_template('showpatient.html',data = data)
#==========================================Insert Function=================================
@app.route("/insert-patient",methods=['GET','POST'])
def addpatient():
    if request.method=='POST':
        conn = sqlite3.connect('patient.db')
        cur = conn.cursor()
        Patient_Name=request.form.get('Patient_Name')
        Patient_Age=request.form.get('Patient_Age')
        gender=request.form.get('gender')
        Result_diabetic=request.form.get('Result_diabetic')
        cur.execute(f"insert into PATIENT_DETAILS(PATIENT_NAME,PATIENT_AGE,GENDER,DIABETIC) values('{Patient_Name}',{Patient_Age},'{gender}','{Result_diabetic}')")
        conn.commit()
        print('Data as been Inserted')
        return jsonify({'message':'sucessfull'})
    else:
        return render_template('insert_patient.html')


if __name__ == '__main__':
    app.run()

