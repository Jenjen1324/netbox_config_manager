from django.urls import path, include

from netbox.views.generic import ObjectJournalView, ObjectChangeLogView
from .models import GraphQLQuery
from .template_editor.urls import urlpatterns as template_editor_patterns
from . import views

graphql_query_patterns = [
    # ASNs
    path('', views.GraphQLQueryListView.as_view(), name='graphqlquery_list'),
    path('add/', views.GraphQLQueryEditView.as_view(), name='graphqlquery_add'),
    # path('import/', views.GraphQLQueryEditView.as_view(), name='config_template_import'),
    # path('edit/', views.GraphQLQueryEditView.as_view(), name='config_template_bulk_edit'),
    # path('delete/', views.GraphQLQueryEditView.as_view(), name='config_template_bulk_delete'),
    path('<int:pk>/', views.GraphQLQueryView.as_view(), name='graphqlquery'),
    path('<int:pk>/edit/', views.GraphQLQueryEditView.as_view(), name='graphqlquery_edit'),
    path('<int:pk>/delete/', views.GraphQLQueryDeleteView.as_view(), name='graphqlquery_delete'),
    path('<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='graphqlquery_changelog',
         kwargs={'model': GraphQLQuery}),
    path('<int:pk>/journal/', ObjectJournalView.as_view(), name='graphqlquery_journal',
         kwargs={'model': GraphQLQuery}),
]


urlpatterns = [
    path('template_editor/', include(template_editor_patterns)),
    path('graphqlquery/', include(graphql_query_patterns))
]
