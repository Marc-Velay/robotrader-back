
# Paths within the api

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from api.views import *

urlpatterns = {
    #Authentication urls
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get-token/', CustomObtainAuthToken.as_view()),

    #User-related urls
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'^users/add/$', UserAddView.as_view(), name="add_users"),
    url(r'^users/update/(?P<pk>[0-9]+)/$', UserUpdateView.as_view(), name="update_users"),
    url(r'^users/delete/(?P<pk>[0-9]+)/$', UserDeleteView.as_view(), name="delete_users"),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetailsView.as_view(), name="user_details"),

    #Portfolio related urls
    url(r'^portfolio/',include([
        url(r'^add/$', CreatePortfolioView.as_view(), name="add_portfolio"),
        url(r'^update/(?P<pk>[0-9]+)/$', UpdatePortfolioView.as_view(), name="update_portfolio"),
        url(r'^delete/(?P<pk>[0-9]+)/$', PortfolioView.as_view(), name="delete_portfolio"),
        url(r'^list/$', PortfolioList.as_view(), name="list_portfolio"),
        url(r'^item/(?P<pk>[0-9]+)/$', GetItemsFromPortfolio.as_view(), name="get_item_portfolio"),
        url(r'^item/link/(?P<pk>[0-9]+)/$', LinkItemToPortfolio.as_view(), name="link_portfolio"),
        url(r'^item/remove/(?P<pk>[0-9]+)/$', RemoveItemFromPortfolio.as_view(), name="remove_item_portfolio"),
        url(r'^get/(?P<pk>[0-9]+)/$', PortfolioView.as_view(), name="get_portfolio"),
    ])),

    #Item management urls
    url(r'^items/new/$', CreateView.as_view(), name="create_item"),
    url(r'^items/(?P<pk>[0-9]+)/$', DetailsView.as_view(), name="get_item"),
    url(r'^(?P<item>[a-zA-Z0-9]+)/',include([
        url(r'^(?P<year>[0-9]{4})/$', Item_year.as_view(), name="year"),
        url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', Item_day.as_view(), name="day"),
        url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', Item_month.as_view(), name="month"),
        url(r'^last24/$', Item_last24.as_view(), name="last 24 hours"),
        url(r'^(?P<start>[0-9]{10})/(?P<end>[0-9]{10})/$', Item_epoch.as_view(), name="epoch"),
        url(r'^all/$', Item_all.as_view(), name="all"),
        url(r'^firstEntry/$', Item_firstEntry.as_view(), name="first_entry"),
        url(r'^lastEntry/$', Item_lastEntry.as_view(), name="last_entry"),
        url(r'^addData/$', Item_addData.as_view(), name="add_data"),
        url(r'^predictions/add/$', Item_predictions_add.as_view(), name="predictions"),
        url(r'^predictions/get/$', Item_predictions_get.as_view(), name="predictions"),
        url(r'^validations/add/$', Item_validations_add.as_view(), name="test"),
        url(r'^validations/get/$', Item_validations_get.as_view(), name="test")
    ])),

}

urlpatterns = format_suffix_patterns(urlpatterns)
