from flask import Flask, request, Response
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# The target website to proxy
TARGET_URL = 'https://meta.ai'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def proxy(path):
    # Build the upstream URL
    url = f"{TARGET_URL}/{path}"
    if request.query_string:
        url = f"{url}?{request.query_string.decode()}"
    app.logger.info("Upstream URL: %s", url)

    # Prepare headers: force the Host header to be meta.ai
    headers = dict(request.headers)
    headers['Host'] = 'meta.ai'
    if 'User-Agent' not in headers:
        headers['User-Agent'] = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/111.0.0.0 Safari/537.36'
        )

    try:
        # Forward the request and follow redirects internally
        resp = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=True
        )
    except Exception as e:
        app.logger.error("Error during upstream request: %s", e)
        return Response(f"Error fetching upstream: {e}", status=500)

    # Remove hop-by-hop headers before returning the response
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers_out = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers_out)

if __name__ == '__main__':
    # Listen on all interfaces on port 8080
    app.run(host='0.0.0.0', port=8080)
