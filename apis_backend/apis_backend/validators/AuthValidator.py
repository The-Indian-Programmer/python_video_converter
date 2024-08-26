from marshmallow import Schema, fields, ValidationError
from django.http import JsonResponse
from functools import wraps

class RegisterSchema(Schema):
    email = fields.Email(required=True, unique=True, error_messages={'unique': 'Email already exists', 'required': 'Email is required', 'invalid': 'Invalid email'})
    password = fields.Str(required=True, error_messages={'required': 'Password is required'} )
    
    
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    

class AdminLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
    
class RefreshTokenSchema(Schema):
    token = fields.Str(required=True)
    

class AuthValidator:
    def __init__(self):
        self.errors = {}
    
    def validate(self, data, schema):
        try:
            result = schema().load(data)
            return {'status': True, 'data': result}
        except ValidationError as err:
            self.errors = err.messages
            return {'status': False, 'message': 'Validation error', 'data': self.errors}
    
    def register(self, data):
        return self.validate(data, RegisterSchema)
    
    def login(self, data):
        return self.validate(data, LoginSchema)
    
    def adminLogin(self, data):
        return self.validate(data, AdminLoginSchema)
    
    def refreshToken(self, data):
        return self.validate(data, RefreshTokenSchema)
    
    
    def validate_request(schema_name):
        def decorator(func):
            @wraps(func)
            def wrapped_view(request, *args, **kwargs):
                validator = AuthValidator()
                data = request.data if request.method == 'POST' else request.GET
                if schema_name == 'register':
                    validation_result = validator.register(data)
                elif schema_name == 'login':
                    validation_result = validator.login(data)
                elif schema_name == 'adminLogin':
                    validation_result = validator.adminLogin(data)
                elif schema_name == 'refreshToken':
                    validation_result = validator.refreshToken(data)
                else:
                    return JsonResponse({'status': False, 'message': 'Invalid schema name'}, status=400)
                
                if not validation_result['status']:
                    return JsonResponse(validation_result, status=400)
            
                return func(request, *args, **kwargs)
            return wrapped_view
        return decorator