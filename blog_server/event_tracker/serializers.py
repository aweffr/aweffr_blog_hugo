from rest_framework import serializers

from .models import Event, EventHealth


class HealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventHealth
        fields = ['type', 'heart_rate', 'calories']


class EventSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=Event.CHOICES_TYPE)
    health = HealthSerializer(many=False)

    def create(self, validated_data):
        if validated_data['type'] == Event.HEALTH:
            return self.create_health_event(validated_data)

    def create_health_event(self, validated_data):
        print('validated_data=', validated_data)

        health = EventHealth()
        health.type = validated_data['health']['type']
        health.heart_rate = validated_data['health']['heart_rate']
        health.calories = validated_data['health']['calories']
        health.save()

        event = Event(
            type=validated_data['type'],
            create_at=validated_data.get('create_at'),
            start_at=validated_data.get('start_at'),
            duration=validated_data.get('duration'),
            health=health,
        )
        event.save()

        return event

    class Meta:
        model = Event
        fields = ['type', 'create_at', 'start_at', 'duration', 'modified_at', 'health']
