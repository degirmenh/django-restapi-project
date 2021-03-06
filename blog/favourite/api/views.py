from rest_framework.generics import ListCreateAPIView

from favourite.api.serializers import FavouriteListCreateAPISerializer
from favourite.models import Favourite


class FavouriteListCreateAPIView(ListCreateAPIView):

    serializer_class = FavouriteListCreateAPISerializer

    def get_queryset(self):
        queryset = Favourite.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
