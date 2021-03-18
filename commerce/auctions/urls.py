from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name='index'),
    path("login/", views.login_view, name='login'),
    path("logout", views.logout_view, name='logout'),
    path("register/", views.register, name='register'),
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('detail/<int:pk>', views.ListingDetailView.as_view(), name='view'),
    path('watchlist/', views.ListingListView.as_view(), name='watch'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:pk>', views.CategoryListingContent.as_view(), name='content'),
    path('bid/<int:pk>', views.make, name='bid'),

    path('add/<int:pk>', views.add_watch, name='add'),
    path('delete/<int:pk>', views.remove_watch, name='remove'),
    path('close/<int:pk>', views.close, name='close'),

]
