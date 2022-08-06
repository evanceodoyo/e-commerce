from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer
from .decorators import unauth_middleware


@unauth_middleware
def signup_view(request):
    page_title = 'Sign Up'
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer(
            name = name,
            phone = phone,
            email = email,
            password = password
        )
        # Hold each value sent in post request in a dictionray
        # Use the values to avoid form getting blank if invalid data is posted.
        values = {
            'name': name,
            'phone': phone,
            'email': email,
        }

        error_msg = None
        error_msg = validate_customer(customer)

        if not error_msg:
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('home')
        context = {'error_msg': error_msg, 'values': values}
    context['page_title'] = page_title

    return render(request, 'signup.html', context)

def validate_customer(customer):
    error_msg = None
    if not customer.name:
        error_msg = 'Full Name Required!'
    elif len(customer.name) < 5:
        error_msg = 'Your Name must be at least 5 charcters long.'
    elif not customer.phone:
        error_msg = 'Phone number required.'
    elif len(customer.phone) < 10:
        error_msg = 'Phone number must be at least 10 characters long.'
    elif not customer.email:
        error_msg = 'Email Required!'
    elif not customer.password:
        error_msg = 'Password Required!'
    elif customer.email_exists():
        error_msg = 'User with the email you provided already registered!'

    return error_msg


@unauth_middleware
def login_view(request):
    page_title = 'Login'
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)

        error_msg = None
        if customer:
            auth_customer = check_password(password, customer.password)
            if auth_customer:
                # store the customer details in session (logged in)
                request.session['customer_id'] = customer.id
                request.session['name'] = customer.name
                request.session['email'] = customer.email
                return redirect('home')
            else:
                error_msg = "Invalid email or password."
        else:
            error_msg = "Invalid email or password."
        context['error_msg'] = error_msg
    context['page_title'] = page_title
    print('Email adress is: ', request.session.get('email'))
    return render(request, 'login.html', context)

def logout_view(request):
    request.session['customer_id'] = {}
    return redirect('login')
