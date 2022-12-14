from entity.models import Entity
from entity.serializers import EntityCreateSerializer
from entity.serializers import EntitySerializer
from rest_framework import viewsets
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class EntityView(viewsets.ModelViewSet):

    permission_classes = [
        IsAuthenticated,
    ]
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    queryset = Entity.objects.filter()
    serializer_class = EntitySerializer

    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    def _fix_weird_key(self, key: str) -> str:
        return key[key.find("[") + 1 : key.find("]")]

    def _is_weird_key(self, key: str) -> bool:
        return "[" in key and "]" in key

    def _patch_request_data(self, data: dict) -> dict:
        copy_of_data = data.copy()
        fix_dict = {}
        for key, value in copy_of_data.items():
            print(f"{key}: {value}")
            if self._is_weird_key(key):
                fix_dict[self._fix_weird_key(key)] = value
        copy_of_data.update(fix_dict)
        return copy_of_data

    def create(self, request: Request) -> Response:
        self.serializer_class = EntityCreateSerializer
        request._full_data = self._patch_request_data(request.data)
        return super().create(request)
