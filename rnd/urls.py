from django.urls import path

from rnd import views

app_name = 'rnd'

urlpatterns = [
    path('', views.home, name='home'),
    path('contracts/', views.contracts_list, name='contracts'),
    path('contracts/<slug:slug>', views.contract_detail, name='contract'),
    # path('contracts/<slug:contr_slug>/load_file/', views.load_order, name='load_order'),
    # path('contracts/<slug:contr_slug>/goods_one/', views.check_one_goods_in_pg, name='check_one'),
    # path('contracts/<slug:contr_slug>/goods_all/', views.check_all_goods_in_pg, name='check_all'),
    # path('contracts/<slug:contr_slug>/stock_store_group/', views.get_stock_store_by_group_id_contract, name='get_stock')
]
