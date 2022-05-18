from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import User

from .serializers import UserDetailSerialzier


class ProfileRetrieveView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerialzier
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user
