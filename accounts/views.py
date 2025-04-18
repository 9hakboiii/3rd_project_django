from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import RegisterUserForm

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


def register_user(request):

    form = RegisterUserForm()

    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            form = RegisterUserForm(request.POST)

            # form 검증
            if form.is_valid():
                form.save()

                # 회원가입 하자 마자, 로그인 시켜줌 (검증 끝난 데이터)
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")

                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect("/")
    else:
        form = RegisterUserForm()

    return render(request, "accounts/register.html", {"form": form})
