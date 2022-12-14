from entity.models import Entity
from rest_framework import serializers


class EntitySerializer(serializers.ModelSerializer):
    """
    Отдельный сериализер для Entity
    """

    value = serializers.IntegerField()
    properties = serializers.SerializerMethodField(read_only=True)

    def get_properties(self, obj):
        result_dict = {}
        for prop in obj.properties.all():
            result_dict[prop.key] = prop.value
        return result_dict

    class Meta:
        model = Entity
        fields = [
            "value",
            "properties",
        ]


class EntityCreateSerializer(serializers.ModelSerializer):
    """
    Отдельный сериализер для создания Entity
    Хотя EntitySerializer тоже бы вполне сошел
    """

    value = serializers.IntegerField()

    class Meta:
        model = Entity
        fields = [
            "value",
        ]
