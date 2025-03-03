
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from common.decorators import allow_manager
from common.functions import generate_form_errors
from users.models import User


def index(request):
    return render(request, 'index.html')