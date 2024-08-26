

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from ..services.AuthService import authService
from ..validators.AuthValidator import AuthValidator
from django.utils.decorators import method_decorator

class AuthController(APIView):
    def __init__(self):
        self.authService = authService()
    # parser_classes = (FormParser, MultiPartParser)
    

    allEndPoints = {
        "register": "register",
        "login": "login",
        "adminLogin": "adminLogin",
        "refreshToken": "refreshToken"
    }

    def post(self, request):
        case = self.allEndPoints.get(request.path.split('/')[-1])
        if case:
            return getattr(self, case)(request)
        else:
            return Response({'status': False, 'message': 'Invalid endpoint'}, status=status.HTTP_400_BAD_REQUEST)
        
    
    # @method_decorator(AuthValidator.validate_request('register'))
    def register(self, request):
        try:
            form_data = request.data
            files = request.FILES
            response = self.authService.register(form_data, files)
            return JsonResponse(response, status=response['code'])
        except Exception as error:
            return JsonResponse({'status': False, 'message': str(error)}, status=500)
        
    def login(self, request):
        try:
            form_data = request.POST
            response = self.authService.login(form_data)
            return JsonResponse(response, status=response['code'])
        except Exception as error:
            print('error', error)
            return JsonResponse({'status': False, 'message': str(error)}, status=500)
        
    def adminLogin(self, request):
        try:
            form_data = request.POST
            response = self.authService.adminLogin(form_data)
            return JsonResponse(response, status=response['code'])
        except Exception as error:
            return JsonResponse({'status': False, 'message': str(error)}, status=500)
        

    def refreshToken(self, request):
        try:
            user_data = request.user
            response = self.authService.refreshToken(user_data)
            return JsonResponse(response, status=response['code'])
        except Exception as error:
            return JsonResponse({'status': False, 'message': str(error)}, status=500)