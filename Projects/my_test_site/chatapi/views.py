import json
import time
from django.shortcuts import redirect, render
import redis
import json5,re
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

# Connect to Redis (default host: 127.0.0.1, port: 6379, using database 0)
redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

# @csrf_exempt
def store_data(request, key):
    """
    Accepts POST requests with JSON data and stores the payload in Redis under the provided key.
    Expects a JSON payload with a "response" key. If the key isn't provided in the payload,
    it uses the dynamic key from the URL.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            response_text = data.get("response")
            if response_text is not None:
                redis_client.set(key, response_text)
            else:
                redis_client.set(key, json.dumps(data))
                redis_client.rpush(key+"list", json.dumps(data))
            print("Stored key =", key)
            return JsonResponse({"status": "success", "key": key})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)


def get_data(request, key):
    """
    Retrieves stored JSON data from Redis for the given key.
    """
    data = redis_client.get(key)
    if data:
        # return JsonResponse({"data": json.loads(data)})
        return JsonResponse({"data": data})
    return JsonResponse({"data": None})

def delete_data(request, key):
    """
    Deletes the stored JSON data from Redis for the given key.
    """
    redis_client.delete(key)
    return JsonResponse({"status": "deleted"})


def extract_json(text):
    json_objects = []
    # json_pattern = re.compile(r'\{.*?\}|\[.*?\]', re.DOTALL)
    """Extracts JSON content from a given text."""
    # json_pattern = re.compile(r'\{.*?\}|\[.*?\]', re.DOTALL)
    # This pattern looks for JSON objects that end with a quote then a closing brace.
    json_pattern = re.compile(r'\{.*?"\}|\[.*?\]', re.DOTALL)

    for match in json_pattern.findall(text):
        try:
            parsed_json = json5.loads(match)  # json5 handles more flexible JSON formats
            json_objects.append(parsed_json)
        except Exception as e:
            print("Exception = ",e)
            print("input was = ", match)
            continue  # Skip invalid JSON structures
    chat_content = ""
    for obj in json_objects:
        print("json_obj = ", obj)  # Extracted JSON objects
        if 'v' in obj:
            chat_content += str(obj['v'])

    chat_content = chat_content.encode("utf-16", "surrogatepass").decode("utf-16", "ignore")
    # print("final chat content = ", chat_content)

    return chat_content

def index(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        print("user input " , user_input)
        redis_client.set("chat_input", user_input)
        key = "chat_response"
        redis_client.delete(key)

        """
        Streams the value stored in Redis under the given key.
        If the data changes, it yields the full new value.
        It checks for changes every `interval` seconds (default: 1 sec),
        and stops streaming if no changes occur for `timeout` seconds (default: 10 sec).
        Both values are customizable via query parameters.
        """
        # Get customizable parameters from query string with defaults.
        try:
            check_interval = float(request.GET.get("interval", 1))
            stop_timeout = float(request.GET.get("timeout", 90))
        except ValueError:
            return HttpResponse("Invalid interval or timeout parameter", status=400)

        # # Try to fetch the initial data
        # initial_data = redis_client.get(key)
        # print("inital data = " , initial_data)
        # if initial_data is None:
        #     return HttpResponse(f"No data found for key: {key}", status=404)

        # # Determine the Content-Type based on the initial data
        # initial_data_str: str = initial_data.strip()
        # if initial_data_str.startswith("{") or initial_data_str.startswith("["):
        #     content_type = "application/json"
        # else:
        #     content_type = "text/plain"
        
        content_type = "text/plain"

        def data_stream():
            last_data = ""
            last_change = time.time()

            # Yield the initial data immediately.
            # yield extract_json(last_data)

            while True:
                time.sleep(check_interval)
                print("waiting for data")
                current_data = redis_client.get(key)
                if current_data and current_data != last_data:
                    # Data has changed; yield the new data.
                    yield extract_json(current_data)
                    last_data = current_data
                    last_change = time.time()
                else:
                    # No change detected; if we've waited too long, break the loop.
                    if time.time() - last_change >= stop_timeout:
                        break

        return StreamingHttpResponse(data_stream(), content_type=content_type)

    return render(request, "chat_index.html")

def chatpage(request):
    """
    Retrieves the full chat page HTML stored under the Redis key 'chatpage'
    and returns it as an HTTP response.
    """
    # if request.method == "POST":
    #     # Get the submitted chat input and set the Redis key 'chat_input'
    #     chat_input = request.POST.get("chat_input", "")
    #     redis_client.set('chat_input', chat_input)
        # Redirect to avoid resubmission on refresh
        # return redirect('chat-page-data')
    # Attempt to retrieve the chat page data from Redis.
    page_data = redis_client.get('chatpage')
    
    if page_data:
        # Convert the binary data to a string.
        page_content = page_data
    else:
        page_content = "<p>No chat page data found.</p>"
    
    # Return the content as an HTTP response with a content type of HTML.
    # return HttpResponse(page_content, content_type="text/html")
    # Render the template with the chat page content.
    return render(request, 'chatpage.html', {'page_content': page_content})

