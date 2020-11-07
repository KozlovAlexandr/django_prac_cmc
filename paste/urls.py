from django.urls import path, include

from . import views

app_name='paste'
urlpatterns = [
    path('', views.show_all,  name='show_all'),
    path('<int:page>/', views.show_page, name='show_page'),
    path('my/', views.show_my_pastes, name='show_my_pastes'),
    path('my/<int:page>/', views.show_my_page, name='show_my_page'),
    path('create/', views.create, name='create'),
    path('<str:paste_hash>/edit/', views.edit, name='edit'),
    path('raw/<str:paste_hash>/', views.download, name='download'),
    path('<str:paste_hash>/', views.detail, name='detail'),
    path('catalog/create/', views.create_catalog, name='create_catalog'),
    path('catalog/<str:catalog_name>/', views.detail_catalog, name='detail_catalog'),
]