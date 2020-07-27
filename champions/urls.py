from django.urls import path
from . import views

urlpatterns = [
    path('', views.champions),
    path('champions/', views.champions),
    path('champion/<str:champion_name>/', views.champion, name='urlname'),
    path('about/', views.about),
    path('1v1_simulator/', views.fight_simulator),
    path('get/ajax/champion_graph/', views.get_graph_data, name="get_graph_data"),
    path('get/ajax/1v1_simulation/', views.get_simulation_results, name="get_simulation_results"),
    # path('import_data/', views.import_data)
]
