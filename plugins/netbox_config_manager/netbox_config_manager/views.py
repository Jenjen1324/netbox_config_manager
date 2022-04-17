from netbox.views.generic import ObjectEditView, ObjectDeleteView, ObjectListView, ObjectView
from netbox_config_manager.forms import GraphQLQueryForm
from netbox_config_manager.models import GraphQLQuery
from netbox_config_manager.tables import GraphQLQueryTable


class GraphQLQueryListView(ObjectListView):
    queryset = GraphQLQuery.objects.all()
    # filterset = filtersets.VRFFilterSet
    # filterset_form = forms.VRFFilterForm
    table = GraphQLQueryTable


class GraphQLQueryView(ObjectView):
    queryset = GraphQLQuery.objects.all()

    class Meta:
        model = GraphQLQuery


class GraphQLQueryEditView(ObjectEditView):
    queryset = GraphQLQuery.objects.all()
    form = GraphQLQueryForm


class GraphQLQueryDeleteView(ObjectDeleteView):
    queryset = GraphQLQuery.objects.all()
