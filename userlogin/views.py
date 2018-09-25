from django.shortcuts import render
from django.contrib import auth
import pyrebase


config = {
    'apiKey': "AIzaSyBnLexI4Z6Qt8FxVKpkYDK5hOBwTcPlqe4",
    'authDomain': "lights-camera-popcorn-nec.firebaseapp.com",
    'databaseURL': "https://lights-camera-popcorn-nec.firebaseio.com",
    'projectId': "lights-camera-popcorn-nec",
    'storageBucket': "lights-camera-popcorn-nec.appspot.com",
    'messagingSenderId': "167484483918"
}
fireBase = pyrebase.initialize_app(config)

authe = fireBase.auth()
database = fireBase.database()

user_movie_data = {}


def sign_in(request):
    return render(request, "userlogin/signIn.html")


def post_sign_in(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid Username or password. Please try again :) !"
        return render(request, "userlogin/signIn.html", {'msg': message})
    uid = user['localId']
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    user_name = database.child("Users").child(uid).child("User info").child("Name").get().val()
    return render(request, "userlogin/welcome.html", {"user_name": user_name})


def sign_up(request):
    return render(request, "userlogin/signUp.html", request.GET)


def post_sign_up(request):
    name = request.POST.get('username')
    email = request.POST.get('email')
    contact_no = request.POST.get('telephone')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email, passw)
    except:
        message = "Please check your username and password.Username might be in use or password maybe too weak. Password should be atleast of 6 character long. Otherwise try unique username"
        return render(request, "userlogin/signUp.html", request.GET, {"msg": message})
    uid = user['localId']
    data = {"Name": name, "Contact No": contact_no, "Email": email, "Password": passw}
    database.child("Users").child(uid).child("User info").set(data)
    message = "Registration Completed. Login to Book Tickets"
    return render(request, "userlogin/signIn.html", {'msg': message})


def log_out(request):
    auth.logout(request)
    return render(request, "userlogin/signIn.html")


def seat_booking(request):
    city = request.POST.get('cities')
    theatre = request.POST.get('theatre')
    movie = request.POST.get('movies')
    shows = request.POST.get('shows')
    return render(request, "userlogin/bookseats.html", {'movie': movie, 'city': city, 'theatre': theatre, 'shows': shows})


def ticket_confirmation(request):
    counter = 1

    movie_name = request.GET['movieName']
    theatre_name = request.GET['theatreName']
    city_name = request.GET['cityName']
    show_time = request.GET['showTime']
    ticket_owner = request.GET['name']
    no_of_seats = request.GET['no_of_seats']
    seat_id = request.GET['seat_id']
    seat_val = request.GET['seat_val']

    user_movie_data['movie_name'] = movie_name
    user_movie_data['city_name'] = city_name
    user_movie_data['theatre_name'] = theatre_name
    user_movie_data['show_time'] = show_time
    user_movie_data['seat_id'] = seat_id
    user_movie_data['no_of_seats'] = no_of_seats
    user_movie_data['ticket_owner'] = ticket_owner
    user_movie_data['seat_val'] = seat_val

    print(user_movie_data)

    idToken = request.session['uid']
    user_data = authe.get_account_info(idToken)
    user = user_data['users']
    user = user[0]
    localid = user['localId']

    booking = database.child("Users").child(localid).child("Booking-not-confirmed-info").get().val()
    if booking is None:
        counter = 1
    else:
        for book in booking:
            counter += 1

    database.child("Users").child(localid).child("Booking-not-confirmed-info").child("booking_no_" + str(counter)).set(
        user_movie_data)

    return render(request, "userlogin/confirmbooking.html", user_movie_data)
