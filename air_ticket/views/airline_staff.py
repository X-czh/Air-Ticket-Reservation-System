from flask import Blueprint, render_template, request, session, redirect, url_for
from pymysql import MySQLError
from air_ticket import conn
from air_ticket.utils import requires_login_airline_staff

mod = Blueprint('airline_staff', __name__, url_prefix='/airline_staff')


# Define route for homepage
@mod.route('/')
@requires_login_airline_staff
def homepage():
	return render_template('airline_staff/index.html')


# Define route for update
@mod.route('/update')
@requires_login_airline_staff
def update():
	return render_template('airline_staff/update.html')


# Define route for view
@mod.route('/view')
@requires_login_airline_staff
def view():
	return render_template('airline_staff/view.html')


# Define route for compare
@mod.route('/compare')
@requires_login_airline_staff
def compare():
	return render_template('airline_staff/compare.html')


@mod.route('/createNewFlights', methods=['POST'])
@requires_login_airline_staff
def createNewFlights():
	# grabs information
	airline_name = session['airline_name']
	flight_num = request.form['flight_num']
	departure_airport = request.form['departure_airport']
	departure_time = request.form['departure_time']
	arrival_airport = request.form['arrival_airport']
	arrival_time = request.form['arrival_time']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplane_id']

	try:
		with conn.cursor() as cursor:
			ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
			cursor.execute(ins, (airline_name, flight_num, departure_airport, departure_time, 
				arrival_airport, arrival_time, price, status, airplane_id))
		conn.commit()
	except MySQLError as e:
		print('Got error {!r}, errno is {}'.format(e, e.args[0]))
	
	return render_template('customer/index.html')


# Change status of flights
@mod.route('/changeFlightStatus', methods=['POST'])
@requires_login_airline_staff
def changeFlightStatus():
	# grabs information
	airline_name = session['airline_name']
	flight_num = request.form['flight_num']
	status = request.form['status']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		UPDATE flight
		SET status = %s
		WHERE airline_name = %s AND flight_num = %s '''
	cursor.execute(query, (status, airline_name, flight_num))
	# stores the results in a variable
	cursor.close()
	return render_template('customer/index.html')


# Add new airplane
@mod.route('/addNewAirplane', methods=['POST'])
@requires_login_airline_staff
def addNewAirplane():
	# grabs information
	airline_name = session['airline_name']
	airplane_id = request.form['airplane_id']
	seats = request.form['seats']

	try:
		with conn.cursor() as cursor:
			ins = 'INSERT INTO airplane VALUES(%s, %s, %s)'
			cursor.execute(ins, (airline_name, airplane_id, seats))
		conn.commit()
	except MySQLError as e:
		print('Got error {!r}, errno is {}'.format(e, e.args[0]))
	
	return render_template('customer/index.html')


# Add new airport
@mod.route('/addNewAirport', methods=['POST'])
@requires_login_airline_staff
def addNewAirport():
	# grabs information
	airport_name = request.form['airport_name']
	airport_city = request.form['airport_id']

	try:
		with conn.cursor() as cursor:
			ins = 'INSERT INTO airport VALUES(%s, %s)'
			cursor.execute(ins, (airport_name, airport_city))
		conn.commit()
	except MySQLError as e:
		print('Got error {!r}, errno is {}'.format(e, e.args[0]))
	
	return render_template('customer/index.html')


# View top5 booking agent
@mod.route('/viewTop5BookingAgent', methods=['POST'])
@requires_login_airline_staff
def viewTop5BookingAgent():
	# grabs information
	airline_name = session['airline_name']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT booking_agent_id, COUNT(ticket_id) as count
		FROM ticket NATURAL JOIN purchases
		WHERE airline_name = %s AND booking_agent_id IS NOT NULL AND
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND CURDATE()
		GROUP BY booking_agent_id
		ORDER by count DESC
		LIMIT 5 '''
	cursor.execute(query, (airline_name))
	top5bycount_past_month = cursor.fetchall()
	query = '''
		SELECT booking_agent_id, COUNT(ticket_id) as count
		FROM ticket NATURAL JOIN purchases
		WHERE airline_name = %s AND booking_agent_id IS NOT NULL AND
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND CURDATE()
		GROUP BY booking_agent_id
		ORDER by count DESC
		LIMIT 5 '''
	cursor.execute(query, (airline_name))
	top5bycount_past_year = cursor.fetchall()
	query = '''
		SELECT booking_agent_id, SUM(price) * 0.1 as commission
		FROM ticket NATURAL JOIN purchases NATURAL JOIN flight
		WHERE airline_name = %s AND booking_agent_id IS NOT NULL AND
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND CURDATE()
		GROUP BY booking_agent_id
		ORDER by commission DESC
		LIMIT 5 '''
	cursor.execute(query, (airline_name))
	top5bycommission_past_year = cursor.fetchall()
	cursor.close()
	return render_template('airline_staff/index.html', 
		top5bycount_past_month=top5bycount_past_month,
		top5bycount_past_year=top5bycount_past_year,
		top5bycommission_past_year = top5bycommission_past_year)


# View Frequent Customers
@mod.route('/viewFrequentCustomers', methods=['POST'])
@requires_login_airline_staff
def viewFrequentCustomers():
	# grabs information
	airline_name = session['airline_name']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT customer_email, COUNT(ticket_id) AS count
		FROM ticket NATURAL JOIN purchases
		WHERE airline_name = %s AND
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND CURDATE()
		GROUP BY customer_email
		ORDER by count DESC '''
	cursor.execute(query, (airline_name))
	result = cursor.fetchall()
	return render_template('airline_staff/index.html', result=result)


# View reports
@mod.route('/viewReports', methods=['POST'])
@requires_login_airline_staff
def viewReports():
	# grabs information
	airline_name = session['airline_name']
	start_date = request.form['start_date']
	end_date = request.form['end_date']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT YEAR(purchase_time) as year, MONTH(purchase_time) as month, COUNT(ticket_id) as total
		FROM purchases NATURAL JOIN ticket
		WHERE airline_name = %s AND 
			purchase_date BETWEEN %s AND %s
		GROUP BY year, month 
		ORDER BY year DESC, month DESC '''
	cursor.execute(query, (airline_name, start_date, end_date))
	result = cursor.fetchall()
	return render_template('airline_staff/index.html', result=result)


# Compare revenue
@mod.route('/compareRevenue', methods=['POST'])
@requires_login_airline_staff
def compareRevenue():
	# grabs information
	airline_name = session['airline_name']

	# cursor used to send queries
	cursor = conn.cursor()
	# revenue in the last month
	query = '''
		SELECT SUM(price)
		FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
		WHERE airline_name = %s AND booking_agent_id IS NULL AND 
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND CURDATE() '''
	cursor.execute(query, (airline_name))
	revenue_direct_sale_last_month = cursor.fetchone()
	query = '''
		SELECT SUM(price)
		FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
		WHERE airline_name = %s AND booking_agent_id IS NOT NULL AND 
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 MONTH) AND CURDATE() '''
	cursor.execute(query, (airline_name))
	revenue_indirect_sale_last_month = cursor.fetchone()
	revenue_last_month = (revenue_direct_sale_last_month, revenue_indirect_sale_last_month)
	# revenue in the last year
	query = '''
		SELECT SUM(price)
		FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
		WHERE airline_name = %s AND booking_agent_id IS NULL AND 
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND CURDATE() '''
	cursor.execute(query, (airline_name))
	revenue_direct_sale_last_year = cursor.fetchone()
	query = '''
		SELECT SUM(price)
		FROM flight NATURAL JOIN ticket NATURAL JOIN purchases
		WHERE airline_name = %s AND booking_agent_id IS NOT NULL AND 
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND CURDATE() '''
	cursor.execute(query, (airline_name))
	revenue_indirect_sale_last_year = cursor.fetchone()
	revenue_last_year = (revenue_direct_sale_last_year, revenue_indirect_sale_last_year)
	render_template('airline_staff/index.html', 
		revenue_last_month=revenue_last_month,
		revenue_last_year=revenue_last_year)


# View top3 destinations
@mod.route('/viewTop3Destinations', methods=['POST'])
@requires_login_airline_staff
def viewTop3Destinations():
	#grabs information
	airline_name = session['airline_name']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = '''
		SELECT arrival_airport, airport_city, COUNT(ticket_id) as count
		FROM flight NATURAL JOIN ticket NATURAL JOIN purchases, airport
		WHERE airline_name = %s AND arrival_airport = airport_name AND  
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 3 MONTH) AND CURDATE()
		GROUP BY arrival_airport
		ORDER BY count DESC
		LIMIT 3 '''
	cursor.execute(query, (airline_name))
	top3_past3month = cursor.fetchall()
	query = '''
		SELECT arrival_airport, airport_city, COUNT(ticket_id) as count
		FROM flight NATURAL JOIN ticket NATURAL JOIN purchases, airport
		WHERE airline_name = %s AND arrival_airport = airport_name AND  
			purchase_date BETWEEN DATE_SUB(NOW(), INTERVAL 1 YEAR) AND CURDATE()
		GROUP BY arrival_airport
		ORDER BY count DESC
		LIMIT 3 '''
	cursor.execute(query, (airline_name))
	top3_past1year = cursor.fetchall()
	cursor.close()
	return render_template('airline_staff/index.html', 
		top3_past3month=top3_past3month,
		top3_past1year=top3_past1year)


# Define route for logout
@mod.route('/logout')
@requires_login_airline_staff
def logout():
	session.pop('username')
	session.pop('usertype')
	session.pop('airline_name')
	return redirect('/')
