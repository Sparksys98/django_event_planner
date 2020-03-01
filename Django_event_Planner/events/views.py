from django.contrib import messages
from django.db.models import F
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, CreateForm, BookForm
from django.contrib import messages
from .models import Event, Booking
from datetime import datetime

def home(request):
    events=Event.objects.filter(datetime__gte=datetime.today())
    search_result=''
    search=request.GET.get("search")
    if search:
        search_term = request.GET['search']
        events=events.filter(Q(title__icontains=search)|Q(description__icontains=search)|Q(added_by__username__icontains=search)).distinct()
        # events=Event.objects.filter(datetime__gte=datetime.today())
    context = {
    "events": events,
    "search_result": search_result, }
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


def event_list(request):
    if request.user.is_anonymous:
        return redirect("login")
    events = Event.objects.filter(datetime__gte=datetime.today())
    context = {"events": events}
    return render(request, 'event_list.html', context)

def my_list(request):
    events = Event.objects.all()
    context = {"events": events}
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
    #Trying the booking code here, but it's not working
    if request.method == "POST":
        tickets = request.POST.get('tickets')
        # Trying to do the rest of the logic here...

    #    return redirect('event-list')
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
    events=Event.objects.all()
    context= {"events":events}
    return render(request,'dashboard.html',context)

# def view_detail(request):
#     booking_obj=Booking.objects.all()
#     booking=Booking.objects.filter(tickets_num)
#     value = request.POST.get('search','')
#     seat_num
#     return value-booking

def booking(request,event_id):
    event = Event.objects.get(id=event_id)
    seats = event.seats
    form = BookForm()
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            tickets = form.save(commit=False)
            tickets.tickets_num = event
            tickets.save()
            event = Event.objects.get(id=event_id)
            event.seats =  event.seats - tickets.tickets
            if event.seats < 0:
                messages.warning(request, 'Not Available!!')
                return redirect('event-detail',event_id)
            event.save()

        return redirect('event-book',event_id)
    context = {
        "event": event,
        "form": form,
    }
    return render(request, 'booking.html', context)
