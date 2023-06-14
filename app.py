from flask import Flask, jsonify, request, render_template
import sqlite3
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


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
#=========================================show patient==============

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
#===========================================================================
# @app.route("/add-patient",methods=['GET','POST'])
# def addpatient():
#     if request.method=='POST':
#         conn = sqlite3.connect('patient.db')
#         cur = conn.cursor()
#         customername=request.form.get('Patient_Name')
#         customeraddr=request.form.get('')
#         customeremail=request.form.get('email')
#         cur.execute(f"insert into customer(customer_name,customer_addr,customer_email) values('{customername}','{customeraddr}','{customeremail}')")
#         conn.commit()
#         print('Data as been Inserted')
#         return jsonify({'message':'sucessfull'})
#     else:
#         return render_template('addcustomer.html')


if __name__ == '__main__':
    app.run()

