from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, CreateForm
from django.contrib import messages
from .models import Event, Booking
from datetime import datetime

def home(request):
    # results = Event.objects.filter(title__icontains=query)
    events = Event.objects.all()
    context = {
    "events": events,}
    # "results": results
    return render(request, 'home.html', context)

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


def item_list(request):
    if request.user.is_anonymous:
        return redirect("login")
    events = Event.objects.filter(datetime__gte=datetime.today())
    context = {
        "events": events,    }
    return render(request, 'event_list.html', context)

def my_list(request):
    events = Event.objects.all()
    context = {
        "events": events,}
    return render(request, 'my_list.html', context)

def create_event(request):
    if request.user.is_anonymous:
        return redirect("login")
    form = CreateForm()
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.added_by = request.user
            event.save()
            return redirect('event-list')
    context = {
        "form":form,
    }
    return render(request, 'create_event.html', context)

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    booking=Booking.objects.all()
    if request.method == "POST":
        tickets = request.POST.get('tickets')
        # Do the rest of the logic here

        tickets=str(tickets)+"10"

        return redirect('event-list')
    context = {
        "event": event,
        "booking": booking,

    }
    return render(request, 'event_detail.html', context)

def event_update(request, event_id):

    event_obj = Event.objects.get(id=event_id)
    form = CreateForm(instance=event_obj)
    # if not request.user.is_staff and request.user != event_obj.added_by:
    #     return redirect("unauthorized")
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES, instance=event_obj)
        if form.is_valid():
            form.save()
            return redirect('event-list')
    context = {
        "event_obj": event_obj,
        "form":form,
    }
    return render(request, 'event_update.html', context)

def dashboard(request):
    return render(request,'dashboard.html')

# def view_detail(request):
#     booking_obj=Booking.objects.all()
#     booking=Booking.objects.filter(tickets_num)
#     value = request.POST.get('search','')
#     seat_num
#     return value-booking

def add_points(request):
            if request.POST.get(''):
                profil = get_object_or_404(Event, created_by=request.user)
                profil.seats = F('seats') + 10
                profil.save(update_fields=["seats"])
                return render(request, 'event_detail.html')
