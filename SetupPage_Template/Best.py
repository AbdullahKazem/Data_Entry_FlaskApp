from flask import Flask, render_template, redirect, request, url_for, jsonify, session
import psycopg2
import requests
from functools import wraps
import os
# from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

app.secret_key = os.urandom(24)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/Best/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form["Username"]
        password = request.form["Password"]
        print(username, password)
        if username == "Admin" and password == "Admin":
                session['role'] = 'admin'
                return redirect(url_for("input"))
        else:
            return render_template('login_Page.html')
    else:
        return render_template('login_Page.html')

######################### Product Page #################################################        
@app.route('/Best/products', methods=['POST', 'GET', 'DELETE'])
@login_required
def products():
    print("in product")
    if request.method == 'POST':
        print("in product post")
        name = request.form['productname']
        idealPerformance = request.form['idealperformance']
        weight = request.form['weight']
        # conn = Database Connection  
        dbCursor = conn.cursor()
        insertNewProduct = "INSERT INTO products (productname, productidealperformance ,productweight) VALUES (%s, %s, %s);"
        dbCursor.execute(insertNewProduct, (name, idealPerformance, weight))
        conn.commit()
        dbCursor.close()
        conn.close()
        return redirect(url_for('products'))
    else:
        print("in product get")
        # conn = Database Connection  
        dbCursor = conn.cursor()
        getAllProducts = "select * from products;"
        dbCursor.execute(getAllProducts)
        data = dbCursor.fetchall()
        conn.commit()
        dbCursor.close()
        conn.close()
        rows = []
        numberOfRows = 0
        for row in data:
            numberOfRows = numberOfRows + 1
            fetchedID = row[0]
            fetchedProductName = row[1]
            fetchedIdealPerformance = row[2]
            fetchedWeight = row[3]
            rows.append([fetchedID, fetchedProductName, fetchedIdealPerformance, fetchedWeight])
        print(rows)
        print(numberOfRows)
        return render_template('products.html', rows=rows, numberOfRows=numberOfRows)

@app.route('/Best/delete', methods=['POST', 'GET'])
@login_required
def delete():
    if request.method == 'POST':
        ids = request.form.getlist('checkedList')
        print(ids)
        # conn = Database Connection
        dbCursor = conn.cursor()
        for id in ids:
            # id = str(id)
            print(id)
            sqldelete = "delete from products where product_id = %s ;"
            dbCursor.execute(sqldelete, (id,))      
        conn.commit()
        dbCursor.close()
        conn.close()
        return redirect(url_for('products'))

@app.route('/Best/products/edit_data', methods=['POST', 'GET'])
@login_required
def edit_data():
    editData = request.get_json()
    myEditedArray = editData['origin']
    idList = editData['productId']
    print(len(myEditedArray))
    print(idList)
    sublist_size = int(len(myEditedArray) / len(idList))
    editedData_dict = {key: myEditedArray[i * sublist_size: (i + 1) * sublist_size] for i, key in enumerate(idList)}
    print("Data =", editedData_dict)
    # conn = Database Connection
    dbCursor = conn.cursor()
    for i in range(len(idList)):
        returnedList = editedData_dict[idList[i]]
        sqledit = "update products set productname = %s ,productidealperformance=%s, productweight=%s where product_id=%s;"
        dbCursor.execute(sqledit, (returnedList[0],returnedList[1],returnedList[2],idList[i]))
    conn.commit()
    dbCursor.close()
    conn.close()
    return redirect(url_for('products'))

#####################################################################################
######################### RFID Page #################################################        
@app.route('/Best/RFID', methods=['POST', 'GET', 'DELETE'])
@login_required
def RFID():
    print("in RFID")
    if request.method == 'POST':
        print("in RFID post")
        code = request.form['code']
        operatorname = request.form['operatorname']
        # conn = Database Connection 
        dbCursor = conn.cursor()
        insertNewProduct = "INSERT INTO rfid (code, operatorname) VALUES (%s, %s);"
        dbCursor.execute(insertNewProduct, (code, operatorname))
        conn.commit()
        dbCursor.close()
        conn.close()
        return redirect(url_for('RFID'))
    else:
        print("in product get")
        # conn = Database Connection
        dbCursor = conn.cursor()
        getAllProducts = "select * from rfid;"
        dbCursor.execute(getAllProducts)
        data = dbCursor.fetchall()
        conn.commit()
        dbCursor.close()
        conn.close()
        rfidRows = []
        rfidNumberOfRows = 0
        for row in data:
            rfidNumberOfRows = rfidNumberOfRows + 1
            fetchedID = row[0]
            fetchedCode = row[1]
            fetchedOperatorName = row[2]
            rfidRows.append([fetchedID, fetchedCode, fetchedOperatorName])

        print(rfidNumberOfRows)
        return render_template('RFID.html', rfidRows=rfidRows, rfidNumberOfRows=rfidNumberOfRows)

@app.route('/Best/RFID/delete', methods=['POST', 'GET'])
@login_required
def RFID_delete():
    if request.method == 'POST':
        ids = request.form.getlist('rfidcheckedList')
        print(ids)
        # conn = Database Connection
        dbCursor = conn.cursor()
        for id in ids:
            id = str(id)
            print(id)
            sqldelete = "delete from rfid where rfid_id = %s ;"
            dbCursor.execute(sqldelete, (id,))      
        conn.commit()
        dbCursor.close()
        conn.close()
        return redirect(url_for('RFID'))

@app.route('/Best/RFID/edit_data', methods=['POST', 'GET'])
@login_required
def RFID_edit_data():
    editData = request.get_json()
    myEditedArray = editData['origin']
    idList = editData['productId']
    print(len(myEditedArray))
    print(idList)
    sublist_size = int(len(myEditedArray) / len(idList))
    editedData_dict = {key: myEditedArray[i * sublist_size: (i + 1) * sublist_size] for i, key in enumerate(idList)}
    print("Data =", editedData_dict)
    # conn = Database Connection
    dbCursor = conn.cursor()
    for i in range(len(idList)):
        returnedList = editedData_dict[idList[i]]
        sqledit = "update rfid set code = %s, operatorname=%s where rfid_id=%s;"
        dbCursor.execute(sqledit, (returnedList[0],returnedList[1],idList[i]))
    conn.commit()
    dbCursor.close()
    conn.close()
    return redirect(url_for('products'))

#####################################################################################
@app.route('/Best/input', methods=['GET', 'POST'])
# @login_required
def input():
    try:
        if request.method == 'GET':
            # conn = Database Connection
            dbCursor = conn.cursor()
            getProductsName = "select productname from products;"
            getLastLine1Order = "select * from orders where machinename = 'Line 1' order by order_id desc limit 1;"
            getLastLine2Order = "select * from orders where machinename = 'Line 2' order by order_id desc limit 1;"
            getLastLine3Order = "select * from orders where machinename = 'Line 3' order by order_id desc limit 1;"
            dbCursor.execute(getProductsName)
            data = dbCursor.fetchall()
            dbCursor.execute(getLastLine1Order)
            lastLine1Order = dbCursor.fetchall()
            print("------------------------ lastLine1Order ----------------------------")
            print(lastLine1Order)
            dbCursor.execute(getLastLine2Order)
            lastLine2Order = dbCursor.fetchall()
            print("------------------------ lastLine2Order ----------------------------")
            print(lastLine2Order)
            dbCursor.execute(getLastLine3Order)
            lastLine3Order = dbCursor.fetchall()
            print("------------------------ lastLine3Order ----------------------------")
            print(lastLine3Order)
            orders_rows = []
            ################ Get Line 1 #######################
            for row in lastLine1Order:
                fetchedMachinename = row[1]
                fetchedOrdernumber = row[2]
                fetchedProductname = row[3]
                fetchedTargetamount = row[4]
                orders_rows.append([fetchedMachinename, fetchedOrdernumber, fetchedProductname, fetchedTargetamount])
            
            ##############################################################################
            ################ Get Line 2 #######################
            for row in lastLine2Order:
                fetchedMachinename = row[1]
                fetchedOrdernumber = row[2]
                fetchedProductname = row[3]
                fetchedTargetamount = row[4]
                orders_rows.append([fetchedMachinename, fetchedOrdernumber, fetchedProductname, fetchedTargetamount])
            
            ##############################################################################
            ################ Get Line 1 #######################
            for row in lastLine3Order:
                fetchedMachinename = row[1]
                fetchedOrdernumber = row[2]
                fetchedProductname = row[3]
                fetchedTargetamount = row[4]
                orders_rows.append([fetchedMachinename, fetchedOrdernumber, fetchedProductname, fetchedTargetamount])
            
            ##############################################################################
            print("-------------------Oreders Rows---------------------------")
            print(orders_rows)
            orderlen = len(orders_rows)
            print(orderlen)
            print("--------------------------------------------------------------------------")
            names = []
            namelen=0
            print(data)
            for row in data:
                namelen = namelen + 1
                name = row[0]
                print(name)
                names.append([name])
            print(names)
            print("--------")
            print(namelen)
            return render_template('inputs.html', names=names, len=namelen, orderLen = orderlen, orderrows = orders_rows)
        
    except (Exception, psycopg2.Error) as error:
        print(error)
        return jsonify('unexpected error a7a, call tatbeek for support')

@app.route('/Best/input/send', methods=['GET', 'POST'])
# @login_required
def send():
    try:
        if request.method == 'POST':
            machineName = str(request.form['machinename'])
            productname = str(request.form['products'])
            orderNumber = str(request.form['ordernumber'])
            targetAmount = str(request.form['targets'])
            print(machineName,productname,orderNumber,targetAmount)
            # conn = Database Connection
            dbCursor = conn.cursor()
            addDatatoTablesqlSelect = "insert into orders(machinename, ordernumber, productname, targetamount) values(%s, %s, %s, %s);"
            dbCursor.execute(addDatatoTablesqlSelect, (machineName,orderNumber, productname, targetAmount))
            conn.commit()
            dbCursor.close()
            conn.close()

            # conn = Database Connection
            dbCursor = conn.cursor()   
            sqlSelect = "select * from orders, products where orders.targetamount = %s and products.productname = %s;"
            dbCursor.execute(sqlSelect, (targetAmount,productname))
            rows = dbCursor.fetchall()
            conn.commit()
            dbCursor.close()
            conn.close()
            ######Get data and send it to node red###################
            # conn = Database Connection
            dbCursor = conn.cursor()   
            sqlSelect = "select * from orders, products where orders.targetamount = %s and products.productname = %s;"
            dbCursor.execute(sqlSelect, (targetAmount,productname))
            rows = dbCursor.fetchall()
            conn.commit()
            dbCursor.close()
            conn.close()
            # res = http request to send data to platform which will provide analytics on the data  
            if res.ok:
                print(res)
            return redirect(url_for('input'))
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
