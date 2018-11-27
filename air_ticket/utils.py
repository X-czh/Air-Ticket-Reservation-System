from functools import wraps
from flask import url_for, flash, request, session, redirect


def requires_login_customer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['usertype'] != 'customer':
            flash('You need to be signed in as customer for this page.')
            return redirect(url_for('general.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def requires_login_booking_agent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['usertype'] != 'booking_agent':
            flash('You need to be signed in as booking agent for this page.')
            return redirect(url_for('general.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function


def requires_login_airline_staff(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['usertype'] != 'airline_staff':
            flash('You need to be signed in as airline staff for this page.')
            return redirect(url_for('general.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
