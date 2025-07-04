from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="7654421917@Sibtain",
    database="petrolpumpmanagement",
    port=3000
)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/customers')
def view_customers():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    customers = get_all_customers()
    total_customers = len(customers)
    total_pages = (total_customers + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    return render_template('customers.html', customers=customers, current_page=page, total_pages=total_pages, start=start, end=end)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    name = request.form['name']
    phone = request.form['phone']
    address = request.form['address']

    cursor = db.cursor()
    cursor.execute("INSERT INTO Customer (Name, PhoneNumber, Address) VALUES (%s, %s, %s)", (name, phone, address))
    db.commit()

    return redirect(url_for('view_customers'))

@app.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Customer WHERE CustomerID = %s", (customer_id,))
    db.commit()
    return jsonify({'success': True})

def get_all_customers():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customer")
    return cursor.fetchall()

# Employees
@app.route('/employees')
def view_employees():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()

    total_employees = len(employees)
    total_pages = (total_employees + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page

    return render_template('employees.html',
                           employees=employees,
                           current_page=page,
                           total_pages=total_pages,
                           start=start,
                           end=end)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    phone = request.form['phone']
    role = request.form['role']
    salary = request.form['salary']

    cursor = db.cursor()
    cursor.execute("INSERT INTO Employee (Name, PhoneNumber, Role, Salary) VALUES (%s, %s, %s, %s)", (name, phone, role, salary))
    db.commit()

    return redirect(url_for('view_employees'))

@app.route('/delete_employee/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Employee WHERE EmployeeID = %s", (employee_id,))
    db.commit()
    return jsonify({'success': True})

# Transactions
@app.route('/transactions')
def view_transactions():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    cursor = db.cursor(dictionary=True)
    cursor.execute(""" 
        SELECT TransactionID, Customer.Name AS CustomerName, Amount, QuantityDispensed, DateAndTime
        FROM Transaction
        INNER JOIN Customer ON Transaction.CustomerID = Customer.CustomerID
    """)
    transactions = cursor.fetchall()

    total_transactions = len(transactions)
    total_pages = (total_transactions + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page


    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()

    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()

    cursor.execute("SELECT * FROM Pump")
    pumps = cursor.fetchall()

    cursor.execute("SELECT * FROM Fuel")
    fuels = cursor.fetchall()

    return render_template('transactions.html',
                           transactions=transactions,
                           customers=customers,
                           employees=employees,
                           pumps=pumps,
                           fuels=fuels,
                           current_page=page,
                           total_pages=total_pages,
                           start=start,
                           end=end)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    customer_id = request.form['customer_id']

    # Check if the customer ID exists
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Customer WHERE CustomerID = %s", (customer_id,))
    if cursor.fetchone() is None:
        return jsonify({'error': 'Invalid CustomerID'}), 400

    employee_id = request.form['employee_id']
    pump_id = request.form['pump_id']
    fuel_id = request.form['fuel_id']
    amount = request.form['amount']
    quantity = request.form['quantity_dispensed']
    date_time = request.form['date_and_time']

    cursor.execute(""" 
        INSERT INTO Transaction (CustomerID, EmployeeID, PumpID, FuelID, Amount, QuantityDispensed, DateAndTime) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (customer_id, employee_id, pump_id, fuel_id, amount, quantity, date_time))
    db.commit()

    return redirect(url_for('view_transactions'))

@app.route('/delete_transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Transaction WHERE TransactionID = %s", (transaction_id,))
    db.commit()
    return jsonify({'success': True})


@app.route('/pumps')
def view_pumps():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Pump")
    pumps = cursor.fetchall()
    return render_template('pump.html', pumps=pumps)

@app.route('/add_pump', methods=['POST'])
def add_pump():
    location = request.form['location']        # Get location from form
    capacity = request.form['capacity']        # Get capacity from form
    fuel_types = request.form['fuel_types']    # Get fuel types from form

    cursor = db.cursor()
    cursor.execute("INSERT INTO Pump (Location, Capacity, FuelTypesSupported) VALUES (%s, %s, %s)", (location, capacity, fuel_types))
    db.commit()

    return redirect(url_for('view_pumps'))


@app.route('/delete_pump/<int:pump_id>', methods=['DELETE'])
def delete_pump(pump_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Pump WHERE PumpID = %s", (pump_id,))
    db.commit()
    return jsonify({'success': True})


@app.route('/delivery_vehicles')
def view_delivery_vehicles():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM DeliveryVehicle")
    delivery_vehicles = cursor.fetchall()
    return render_template('delivery_vehicle.html', delivery_vehicles=delivery_vehicles)

@app.route('/add_delivery_vehicle', methods=['POST'])
def add_delivery_vehicle():
    vehicle_number = request.form['vehicle_number']
    capacity = request.form['capacity']
    fuel_type = request.form['fuel_type']  # Get the fuel type from the form

    cursor = db.cursor()
    cursor.execute("INSERT INTO DeliveryVehicle (VehicleNumber, Capacity, FuelType) VALUES (%s, %s, %s)",
                   (vehicle_number, capacity, fuel_type))  # Include fuel_type in the query
    db.commit()

    return redirect(url_for('view_delivery_vehicles'))


@app.route('/delete_delivery_vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_delivery_vehicle(vehicle_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM DeliveryVehicle WHERE DeliveryVehicleID = %s", (vehicle_id,))
    db.commit()
    return jsonify({'success': True})


@app.route('/fuels')
def view_fuels():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Fuel")
    fuels = cursor.fetchall()
    return render_template('fuel.html', fuels=fuels)

@app.route('/add_fuel', methods=['POST'])
def add_fuel():
    fuel_type = request.form['fuel_type']
    price_per_liter = request.form['price_per_liter']

    cursor = db.cursor()
    cursor.execute("INSERT INTO Fuel (FuelType, PricePerLiter) VALUES (%s, %s)", (fuel_type, price_per_liter))
    db.commit()

    return redirect(url_for('view_fuels'))

@app.route('/delete_fuel/<int:fuel_id>', methods=['DELETE'])
def delete_fuel(fuel_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Fuel WHERE FuelID = %s", (fuel_id,))
    db.commit()
    return jsonify({'success': True})

@app.route('/modify_fuel/<int:fuel_id>', methods=['POST'])
def modify_fuel(fuel_id):
    new_stock = request.form['new_stock']
    new_price = request.form['new_price']
    cursor = db.cursor()
    cursor.execute("UPDATE Fuel SET Stock = %s, PricePerLiter = %s WHERE FuelID = %s", (new_stock, new_price, fuel_id))
    db.commit()
    return jsonify({'success': True})




@app.route('/receipts')
def view_receipts():
    cursor = db.cursor(dictionary=True)

    # Fetch all receipts
    cursor.execute("SELECT * FROM Receipt")
    receipts = cursor.fetchall()

    # Fetch TransactionID and CustomerName using a join between Transaction and Customer
    cursor.execute("""
        SELECT t.TransactionID, c.Name AS CustomerName
        FROM `Transaction` t
        JOIN Customer c ON t.CustomerID = c.CustomerID
    """)
    transactions = cursor.fetchall()

    return render_template('receipt.html', receipts=receipts, transactions=transactions)



@app.route('/add_receipt', methods=['POST'])
def add_receipt():
    transaction_id = request.form['transaction_id']
    amount_paid = request.form['amount_paid']
    date_of_issue = request.form['date_of_issue']

    cursor = db.cursor()
    cursor.execute("INSERT INTO Receipt (TransactionID, AmountPaid, DateOfIssue) VALUES (%s, %s, %s)", (transaction_id, amount_paid, date_of_issue))
    db.commit()

    return redirect(url_for('view_receipts'))

@app.route('/delete_receipt/<int:receipt_id>', methods=['DELETE'])
def delete_receipt(receipt_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Receipt WHERE ReceiptID = %s", (receipt_id,))
    db.commit()
    return jsonify({'success': True})



if __name__ == '__main__':
    app.run(debug=True)
