from django.urls import path
from .views import Login, Logout, Signup, home,event_list, create_event, event_detail, event_update, dashboard, my_list,booking
#from events import views
urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('list/', event_list, name='event-list'),
	path('create/', create_event, name='create-event'),
	path('detail/<int:event_id>',event_detail, name='event-detail'),
	path('update/<int:event_id>', event_update, name='event-update'),
	path('dashboard/', dashboard, name='dashboard'),
	path('my_list/', my_list,name='my-list'),
	path('booking/<int:event_id>', booking,name='event-book'),

	# path('details/', view_detail, name='view-detail')



]
