from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
User = get_user_model()


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Аккаунт создан', 201)

@api_view(['POST'])
def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect('http://127.0.0.1:3000/')
    