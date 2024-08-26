from django.http import JsonResponse

def home_page(request):
    print("Home page view")
    return JsonResponse({"message": "Hello, world!"})