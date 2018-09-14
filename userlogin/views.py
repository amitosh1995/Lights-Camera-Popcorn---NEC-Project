from django.shortcuts import render
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

auth = fireBase.auth()


def sign_in(request):
    return render(request, "userlogin/signIn.html")


def post_sign_in(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = auth.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid Username or password. Please try again :) !"
        return render(request, "userlogin/signIn.html", {'msg': message})

    return render(request, "userlogin/welcome.html", {'e': email})


def sign_up(request):
    return render(request, "userlogin/signUp.html", request.GET)
