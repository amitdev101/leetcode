from django.shortcuts import redirect, render
from chatapi.views import redis_client

def paste_page(request):
    return render(request, "paste.html")

def formatter_view(request, room_id="default"):
    key = f"room:{room_id}"
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        if content:
            redis_client.set(key, content)
        # Simply redirect to GET after POST so that the new content is shown
        return redirect(request.path)
    else:
        content = redis_client.get(key) or ""
        return render(request, "formatter.html", {"room_id": room_id, "content": content})
