from django.http import JsonResponse
from .models import Command
from .utils import allow_cors

def receive_command(request):
    if request.method == "POST":
        command_text = request.POST.get('command_text')
        Command.objects.create(command_text=command_text)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


def telegram_bot(request):
    # command = request.GET.get('command', '')
    # Forward this command to the Chrome extension (this will be polling, not real-time)
    # You'd typically save this to a database, but for simplicity, we'll just return it
    # return JsonResponse({"command": command})
    return receive_command(request)


def fetch_command(request):
    try:
        # Fetch the latest unexecuted command
        command = Command.objects.filter(executed=False).latest('timestamp')
        command.executed = True
        command.save()
        print(command.command_text)
        return JsonResponse({'command': command.command_text})
    except Command.DoesNotExist:
        return JsonResponse({'command': None})

@allow_cors
def chrome_extension(request):
    # Here you'd typically fetch the command from the database, but for simplicity:
    # command = request.GET.get('command', '')
    return fetch_command(request)


def send_to_telegram(request):
    if request.method == "POST":
        response = request.POST.get('response')
        # ? Here you should call the function to send a message to the bot
        
        return JsonResponse({"response":response})