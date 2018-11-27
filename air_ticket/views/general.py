from flask import Blueprint, render_template, redirect, url_for, request, session 
from passlib.hash import pbkdf2_sha256
from air_ticket import conn

mod = Blueprint('general', __name__)

# Define route for homepage
@mod.route('/')
def hoempage():
	return render_template('general/index.html')


# Define route for login
@mod.route('/login')
def login():
	return render_template('general/login.html')


# Define route for register
@mod.route('/register')
def register():
	return render_template('general/register.html')


# Check upcoming flights
@mod.route('/upcoming', methods=['POST'])
def checkUpcoming():
	# grabs information from the forms
	departure_airport = request.form['departure_airport']
	departure_date = request.form['departure_date']
	arrival_airport = request.form['arrival_airport']
	arrival_date = request.form['arrival_date']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT * FROM flight WHERE departure_airport = %s AND DATE(departure_time) = %s AND \
		arrival_airport = %s AND DATE(arrival_time) = %s'
	print(query)
	cursor.execute(query, (departure_airport, departure_date, arrival_airport, arrival_date))
	# stores the results in a variable
	data = cursor.fetchall()
	error = None
	if data:
		return render_template('general/index.html', result = data)
	else:
		return render_template('general/index.html', error = error) 


@mod.route('/status', methods=['POST'])
def checkStatus():
	#TODO
	# grabs information from the forms
	flight_num = request.form['flight_num']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	query = 'SELECT status FROM flight WHERE flight_num = %s AND \
		DATE(departure_time) = %s AND DATE(arrival_time) = %s'
	cursor.execute(query, (flight_num, departure_date, arrival_date))
	# stores the results in a variable
	data = cursor.one()
	error = None
	if data:
		# if the previous query returns data, then user exists
		error = 'This user already exists'
		return render_template('general/register.html', error = error)


# Authenticates the login
@mod.route('/loginAuth', methods=['POST'])
def loginAuth():
	# grabs information from the forms
	usertype = request.form['usertype']
	username = request.form['username']
	password = request.form['password']

	# cursor used to send queries
	cursor = conn.cursor()
	# executes query
	attr_username = 'username' if usertype == 'airline_staff' else 'email'
	query = 'SELECT * FROM {} WHERE {} = %s'.format(usertype, attr_username)
	cursor.execute(query, (username))
	# stores the results in a variable
	data = cursor.fetchone()
	cursor.close()
	error = None

	# authenticates the login information
	if data:
		if pbkdf2_sha256.verify(password, data['password']):
			# creates a session for the the user
			session['username'] = username
			session['usertype'] = usertype
			return redirect(url_for('customer.index'))
		else:
			error = 'Incorrect password!'
	else:
		error = 'User does not exist!'
	return redirect(url_for('general.login', error=error))


# Authenticates the register
@mod.route('/registerAuth', methods=['POST'])
def registerAuth():
	# grabs usertype
	usertype = request.form['usertype']
	
	# if usertype is customer
	if usertype == 'customer':
		# grabs information from the forms
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
		building_number = request.form['building_number']
		street = request.form['street']
		city = request.form['city']
		state = request.form['state']
		phone_number = request.form['phone_number']
		passport_number = request.form['passport_number']
		passport_expiration = request.form['passport_expiration']
		passport_country = request.form['passport_country']
		date_of_birth = request.form['date_of_birth']

		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = 'SELECT * FROM customer WHERE email = %s'
		cursor.execute(query, (email))
		# stores the results in a variable
		data = cursor.fetchone()

		# authenticates the register information
		if data:
			cursor.close()
			# if the previous query returns data, then user exists
			error = 'User alread exists!'
			return redirect(url_for('general.register', error=error))
		else:
			# generates the hash value of the password
			password_hash = pbkdf2_sha256.hash(password)
			# inserts into the database
			ins = ('INSERT INTO customer ' 
				'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
			cursor.execute(ins, (email, name, password_hash,  
				building_number, street, city, state, phone_number, 
				passport_number, passport_expiration, passport_country, 
				date_of_birth))
			conn.commit()
			cursor.close()
			return redirect(url_for('customer.homepage'))

	# if usertype is booking_agent
	elif usertype == 'booking_agent':
		# grabs information from the forms
		email = request.form['email']
		password = request.form['password']
		booking_agent_id = request.form['booking_agent_id']

		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = 'SELECT * FROM booking_agent WHERE email = %s'
		cursor.execute(query, (email))
		# stores the results in a variable
		data = cursor.fetchone()

		# authenticates the register information
		if data:
			cursor.close()
			# if the previous query returns data, then user exists
			error = 'User already exists!'
			return redirect(url_for('general.register', error=error))
		else:
			# generates the hash value of the password
			password_hash = pbkdf2_sha256.hash(password)
			# inserts into the database
			ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s)'
			cursor.execute(ins, (email, password_hash, booking_agent_id))
			conn.commit()
			cursor.close()
			return redirect(url_for('booking_agent.homepage'))

	# if usertype is airline staff
	else:
		# grabs information from the forms
		username = request.form['username']
		password = request.form['password']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		date_of_birth = request.form['date_of_birth']
		airline_name = request.form['airline_name']

		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = 'SELECT * FROM airline_staff WHERE username = %s'
		cursor.execute(query, (username))
		# stores the results in a variable
		data = cursor.fetchone()

		# authenticates the register information
		if data:
			cursor.close()
			# if the previous query returns data, then user exists
			error = 'User already exists!'
			return redirect(url_for('general.register', error=error))
		else:
			# generates the hash value of the password
			password_hash = pbkdf2_sha256.hash(password)
			# inserts into the database
			ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
			cursor.execute(ins, (username, password_hash, 
				first_name, last_name, date_of_birth, airline_name))
			conn.commit()
			cursor.close()
			return redirect(url_for('airline_staff.homepage'))
