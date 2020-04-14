from rest_framework import serializers

from fight_covid19.maps.models import HealthEntry


class HealthEntryFormSerializer(serializers.HyperlinkedModelSerializer):
    """Serializers for Health Entry"""

    class Meta:
        model = HealthEntry
        fields = [
            "age",
            "gender",
            "fever",
            "cough",
            "difficult_breathing",
            "self_quarantine",
            "latitude",
            "longitude",
            "unique_id",
        ]


class HealthEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = HealthEntry
        fields = [
            "age",
            "gender",
            "fever",
            "cough",
            "difficult_breathing",
            "self_quarantine",
            "latitude",
            "longitude",
            "unique_id",
            "creation_timestamp",
        ]
