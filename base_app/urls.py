from django.urls import path

from base_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<slug:_filial_slug>", views.home_filial, name="main_filial"),
    path("<slug:_filial_slug>/contracts/", views.show_contracts, name="contracts"),
    path("<slug:_filial_slug>/test/", views.show_test, name="test"),
    path(
        "<slug:_filial_slug>/contracts/<slug:_contract_slug>",
        views.show_operations,
        name="operations",
    ),
    path(
        "<slug:_filial_slug>/contracts/<slug:_contract_slug>/<slug:_operation_slug>",
        views.show_choice_operation,
        name="choice_operation",
    ),
    path(
        "<slug:_filial_slug>/contracts/<slug:_contract_slug>/<slug:_operation_slug>/load_file",
        views.event_load_file,
        name="event_load_file",
    ),
    path(
        "<slug:_filial_slug>/contracts/<slug:_contract_slug>/<slug:_operation_slug>/search_goods",
        views.event_search_goods,
        name="event_search_goods",
    ),
    path(
        "<slug:_filial_slug>/contracts/<slug:_contract_slug>/<slug:_operation_slug>/load_stocks",
        views.event_load_stock,
        name="event_load_stock",
    ),
    path("<slug:_filial_slug>/reports/", views.show_reports, name="reports"),
    path(
        "<slug:_filial_slug>/<slug:_reports_slug>",
        views.show_reports_operation,
        name="choice_reports",
    ),
    path(
        "<slug:_filial_slug>/<slug:_reports_slug>/sverki",
        views.report_sverki,
        name="report_sverki",
    ),
    path("accounts/login/", views.NotFound.as_view(), name="not_groups"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
