from flask import Blueprint, render_template, request, session, redirect
from air_ticket import conn
from air_ticket.utils import requires_login_customer

mod = Blueprint('customer', __name__, url_prefix='/customer')


# Define route for homepage
@mod.route('/')
@requires_login_customer
def homepage():
	return render_template('customer/index.html')


# View my flights
@mod.route('/viewMyFlights', methods=['POST'])
@requires_login_customer
def viewMyFlights():
	# grabs information
	customer_email = session['username']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT *
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND departure_time > NOW()
		ORDER BY departure_time '''
	cursor.execute(query, customer_email)
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()
	return render_template('customer/index.html', result=data)


# Purchase tickets
@mod.route('/purchaseTickets', methods=['POST'])
@requires_login_customer
def purchaseTickets():
	# grabs information
	customer_email = session['username']
	airline_name = request.form['airline_name']
	flight_num = request.form['flight_num']

	# cursor used to send queries
	cursor = conn.cursor()
	
	# check seat availability
	query = '''
		SELECT COUNT(*) as count, seats
		FROM ticket NATURAL JOIN flight NATURAL JOIN airplane
		WHERE airline_name = %s AND flight_num = %s '''
	cursor.execute(query, (airline_name, flight_num))
	data = cursor.fetchone()
	if data['count'] < data['seats']:
		msg = "Purchase successful!"
		# generates ticket_id
		query = 'SELECT COUNT(*) as count FROM ticket'
		cursor.execute(query)
		data = cursor.fetchone()
		ticket_id = data['count'] + 1
		# executes updates
		ins_ticket = 'INSERT INTO ticket VALUES(%s, %s, %s)'
		cursor.execute(ins_ticket, (ticket_id, airline_name, flight_num))
		ins_purchases = 'INSERT INTO purchases VALUES(%s, %s, NULL, CURDATE())'
		cursor.execute(ins_purchases, (ticket_id, customer_email))
		conn.commit()
	else:
		msg = 'All tickets have been sold out!'

	cursor.close()
	return render_template('customer/index.html', message=msg)


# Search for flights
@mod.route('/searchFlights', methods=['POST'])
@requires_login_customer
def searchFlights():
	# grabs information
	departure_airport = request.form['departure_airport']
	departure_date = request.form['departure_date']
	arrival_airport = request.form['arrival_airport']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = ''' 
		SELECT * 
		FROM flight 
		WHERE departure_airport = %s AND DATE(departure_time) = %s AND 
			arrival_airport = %s 
		ORDER BY departure_time '''
	cursor.execute(query, (departure_airport, departure_date, arrival_airport))
	# stores the results in a variable
	data = cursor.fetchall()
	cursor.close()
	return render_template('customer/index.html', result=data)


# Track my spending default view
@mod.route('/trackMySpendingDefault', methods=['POST'])
@requires_login_customer
def trackMySpendingDefault():
	# grabs information
	customer_email = session['username']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = ''' 
		SELECT SUM(price) as total
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND purchase_date >= DATE_SUB(NOW(), INTERVAL 1 YEAR) '''
	cursor.execute(query, (customer_email))
	total = cursor.fetchone()
	query = ''' 
		SELECT YEAR(departure_time) as year, MONTH(departure_time) as month, SUM(price) as total
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND purchase_date >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
		GROUP BY year, month 
		ORDER BY year DESC, month DESC '''
	cursor.execute(query, (customer_email))
	monthwise = cursor.fetchall()
	cursor.close()
	return render_template('customer/index.html', total=total, monthwise=monthwise)


# Track my spending optional view
@mod.route('/trackMySpendingOptional', methods=['POST'])
@requires_login_customer
def trackMySpendingOptional():
	# grabs information
	customer_email = session['username']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT SUM(price) as total
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s '''
	cursor.execute(query, (customer_email, start_date, end_date))
	total = cursor.fetchone()
	query = ''' 
		SELECT YEAR(departure_time) as year, MONTH(departure_time) as month, SUM(price) as total
		FROM purchases NATURAL JOIN ticket NATURAL JOIN flight
		WHERE customer_email = %s AND purchase_date BETWEEN %s AND %s
		GROUP BY year, month 
		ORDER BY year DESC, month DESC '''
	cursor.execute(query, (customer_email, start_date, end_date))
	monthwise = cursor.fetchall()
	cursor.close()
	return render_template('customer/index.html', total=total, monthwise=monthwise)


# Define route for logout
@mod.route('/logout')
@requires_login_customer
def logout():
	session.pop('username')
	session.pop('usertype')
	return redirect('/')
