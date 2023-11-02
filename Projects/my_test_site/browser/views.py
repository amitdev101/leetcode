from django.http import JsonResponse

from my_test_site import utils
import json

def receive_command(request):
    if request.method == "POST":
        data = utils.get_post_data(request)
        print("data from client : ", data)
        client_data = request.POST.get('client')
        response = dict()
        response["client"] = client_data
        response["status"] = "success"
        print("response from server to client : ", response )
        return JsonResponse(response)
    return JsonResponse({'status': 'error'})

def send_command(request):
    response = dict()
    response["status"] = "success"
    return JsonResponse(response)