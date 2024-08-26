from django.http import JsonResponse

def returnSuccess(statusCode, message, data):
    return JsonResponse({'status': True, 'message': message, 'data': data}, status=statusCode)

def returnError(statusCode, message):
    return JsonResponse({'status': False, 'message': message}, status=statusCode)

def returnResponse(statusCode, status, message, data):
    return JsonResponse({'status': status, 'message': message, 'data': data}, status=statusCode)



