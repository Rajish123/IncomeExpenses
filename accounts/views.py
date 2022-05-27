from .models import *
from .serializers import *
from .utils import Util

from rest_framework import generics,status,views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

import jwt

from drf_yasg .utils import swagger_auto_schema
from drf_yasg import openapi

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email = user_data['email'])
        # create token for user and use that to send it to their email
        # gives two token i.e, refresh token and access token
        # create user id to create access token
        token = RefreshToken.for_user(user).access_token
        # this returns like google.com without protocal
        current_site = get_current_site(request).domain
        # returns to this link when user verify token
        relativeLink = reverse('email-verify')
        absurl = 'https://' + current_site + relativeLink + '?token='+str(token)
        email_body = "Hi!"+user.username+"Use link below to verify your email \n" + absurl

        data = {
            'domain': current_site,
            'email_body': email_body,
            'to_email':[user.email,],
            'email_subject': 'Verify your email'
        }
        Util.send_email(data)
        return Response({
            'data':user_data,
            'status':status.HTTP_201_CREATED
        })
        
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer 
    token_param_config = openapi.Parameter(
        'token',in_ = openapi.IN_QUERY,description = 'Token please', type = openapi.TYPE_STRING
    )
    # tell swagger which field to create in parameter
    # manual_parameters:we need to specify parameter which need to be configured
    @swagger_auto_schema(manual_parameters = [token_param_config])

    def get(self, request):
        # we get token from link sent to respective emal represented as token ={line31}
        token = request.GET.get('token')
        # once we get token, we decode it and get which user was encoded in it
        try:
            payload = jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id = payload['user_id'])
            if not user.is_verified():
                user.is_verified = True
                user.save()
                return Response({
                    'email': 'Successfully activated'},
                    status = status.HTTP_200_OK
                )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {'email':'Activation Expired'},
                status = status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {'email':'Invalid token'},
                status =status.HTTP_400_BAD_REQUEST
            )