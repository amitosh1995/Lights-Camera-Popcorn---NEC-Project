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
    print(user)
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "userlogin/welcome.html", {'e': email})


def sign_up(request):
    return render(request, "userlogin/signUp.html", request.GET)


def post_sign_up(request):
    name = request.POST.get('username')
    email = request.POST.get('email')
    contact_no = request.POST.get('telephone')
    passw = request.POST.get('pass')

    user = authe.create_user_with_email_and_password(email, passw)

    uid = user['localId']
    data = {"Name": name, "Contact No": contact_no, "Email": email, "Password": passw}
    database.child("Users").child(uid).child("User info").set(data)
    message = "Registration Completed. Login to Book Tickets"
    return render(request, "userlogin/signIn.html", {'msg': message})


def log_out(request):
    auth.logout(request)
    return render(request, "userlogin/signIn.html")


def seat_booking(request):
    return render(request, "userlogin/bookseats.html")
