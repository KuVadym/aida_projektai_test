import re
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Events

class PublicEventsSerializer(serializers.ModelSerializer):
    highlighted_title = serializers.SerializerMethodField()
    highlighted_description = serializers.SerializerMethodField()

    class Meta:
        model = Events
        fields = ['id', 'title', 'description', 'date', 'location', 'organaizer',
                  'highlighted_title', 'highlighted_description']

    @extend_schema_field(serializers.CharField())
    def get_highlighted_title(self, obj):
        return self._highlight_text(obj.title)

    @extend_schema_field(serializers.CharField())
    def get_highlighted_description(self, obj):
        return self._highlight_text(obj.description)

    def _highlight_text(self, text):
        request = self.context.get('request')
        if not request:
            return text
        search_query = request.query_params.get('search', '')
        exact = request.query_params.get('exact', 'false').lower() == 'true'
        if not search_query:
            return text

        if exact:
            pattern = re.compile(rf'\b{re.escape(search_query)}\b', re.IGNORECASE)
        else:
            pattern = re.compile(re.escape(search_query), re.IGNORECASE)

        return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
    

class MyEventsSerializer(PublicEventsSerializer):
    attendees = serializers.SerializerMethodField()

    class Meta(PublicEventsSerializer.Meta):
        fields = PublicEventsSerializer.Meta.fields + ['attendees']

    @extend_schema_field(serializers.ListField(child=serializers.EmailField()))
    def get_attendees(self, obj):
        return []
    

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'title', 'description', 'date', 'location', 'organaizer']