from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Events

class EventFilter(filters.FilterSet):
    search = filters.CharFilter(method='filter_search')
    exact = filters.BooleanFilter(method='filter_search')  # для підтримки exact=true
    date = filters.DateFilter(field_name='date')
    location = filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = Events
        fields = ['date', 'location']

    def filter_search(self, queryset, name, value):
        exact = self.data.get('exact', 'false').lower() == 'true'
        if exact:
            return queryset.filter(
                Q(title__iexact=value) | Q(description__iexact=value)
            )
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )