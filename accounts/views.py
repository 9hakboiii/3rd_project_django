from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

"""
class HTTPRequest:
    POST = {
        "username": "admin",
        "password": "1234",
    }
"""


def login_user(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "로그인 성공")
            return redirect("/")
        else:
            messages.error(request, "로그인 실패")
            return redirect("accounts:login_user")

    return render(request, "accounts/login.html", {})


def logout_user(request):
    logout(request)
    return redirect("/")
