from django.urls import path
from .views import Login, Logout, Signup, home,item_list, create_event, event_detail, event_update
#from events import views
urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('list/', item_list, name='event-list'),
	path('create/', create_event, name='create-event'),
	path('detail/<int:event_id>',event_detail, name='event-detail'),
	path('update/<int:event_id>', event_update, name='event-update'),

]
