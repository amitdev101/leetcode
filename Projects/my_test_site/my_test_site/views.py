import io
import gzip
import json
import requests
import time
from django.http import StreamingHttpResponse
from django.shortcuts import render
from .meta_ai_request import cookies,files,headers,params

PRINT_LOGS = True

def index(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        print("user input " , user_input)
        url = "https://graph.meta.ai/graphql?locale=user"
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
        #     "Accept": "*/*",
        #     "Accept-Language": "en-US,en;q=0.5",
        #     # "Accept-Encoding": "gzip, deflate, br, zstd",
        #     "Referer": "https://www.meta.ai/",
        #     "Origin": "https://www.meta.ai",
        #     "DNT": "1",
        #     "Connection": "keep-alive",
        #     "Cookie": "datr=8uupZlCR2uqV8AWE67fA8GWy; wd=1536x391; dpr=1.25; abra_csrf=RC5piFE75eK35OxXOObZNv",
        #     "Sec-Fetch-Dest": "empty",
        #     "Sec-Fetch-Mode": "cors",
        #     "Sec-Fetch-Site": "same-site",
        #     "Sec-GPC": "1",
        #     "Priority": "u=0",
        #     "Pragma": "no-cache",
        #     "Cache-Control": "no-cache",
        #     "TE": "trailers",
        # }

        # payload = {
        #     "av": "0",
        #     "access_token": "ABRAQWZALYlhpcm11dzNXSTA3Ny0xMEFTeU9iV2J0ZAjlFbTg1RkNqRHZAXZA09HaTZAGYUR2aFd1YjhHN0FqRUpiU3VHOFVTTnhjbl9wamtQb1dQUjRhRUJmc3J2S2o3U1hzQ2tNOW1VbHBWMG4yMG9NZA3YxOWdyUVZAzZAXJqYjF3SGgydXAyVEVBM085V3d0ZA1NqYkQ2YzU3WDNROHBZAYmh4bDk1b3QzZAGN0aHpLWFRPd0FQeDJvQQZDZD",
        #     "__user": "0",
        #     "__a": "1",
        #     "__req": "8",
        #     "__hs": "20134.HYP:abra_pkg.2.1...0",
        #     "dpr": "1",
        #     "__ccg": "GOOD",
        #     "__rev": "1020149304",
        #     "__s": ":l3xsmr:yf7ahq",
        #     "__hsi": "7471610793729470002",
        #     "__dyn": "7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D85m1mzXwae4UaEW4U2FwNwmE2eU5O0EoS10w5NyES0gq0Lo6-3u362q0XU6O1FwlU18ouwKxvzU5K0UE",
        #     "__csr": "g8qaPJaJGL9WV9Bu8CCBiz8-6pe48GuUy22m00kuyqiE9Ef86m10w4Lw5mX6whIN3zQ1pg0Bt6DgGq5Ai046V5x103-AmF89oc9Q0ha2Waxa5U1s9XdwqoPo5q09Tg7yuu0kOqG_jLAP0uIStgyEloR1ggbide5A7oyzjwp40DE9V2jKgAM7N7c09eaEhkhD2w11l8bycC5o4W1V7d2FE",
        #     "__comet_req": "46",
        #     "lsd": "AVo4dhsiB3w",
        #     "jazoest": "2974",
        #     "__spin_r": "1020149304",
        #     "__spin_b": "trunk",
        #     "__spin_t": "1739619950",
        #     "__jssesw": "1",
        #     "fb_api_caller_class": "RelayModern",
        #     "fb_api_req_friendly_name": "useAbraSendMessageMutation",
        #     "variables": json.dumps({
        #         "message": {"sensitive_string_value": user_input},
        #         # above the user input
        #         "externalConversationId": "f7f30817-213b-4796-980c-ab7c7041aec0",
        #         "offlineThreadingId": "7297251759842551145", 
        #         "threadSessionId": "c91f92f6-76b1-4171-b8af-37bdababaae0",
        #         "suggestedPromptIndex": None,
        #         "flashPreviewInput": None,
        #         "promptPrefix": None,
        #         "entrypoint": "ABRA__CHAT__TEXT",
        #         "icebreaker_type": "TEXT_V2",
        #         "attachments": [],
        #         "attachmentsV2": [],
        #         "activeMediaSets": None,
        #         "activeCardVersions": [],
        #         "activeArtifactVersion": None,
        #         "userUploadEditModeInput": None,
        #         "reelComposeInput": None,
        #         "qplJoinId": "fa3916b05a676e87b",
        #         "gkAbraArtifactsEnabled": False,
        #         "model_preference_override": None,
        #         "__relay_internal__pv__AbraPinningConversationsrelayprovider": False,
        #         "__relay_internal__pv__AbraArtifactsEnabledrelayprovider": False,
        #         "__relay_internal__pv__WebPixelRatiorelayprovider": 1,
        #         "__relay_internal__pv__AbraSearchInlineReferencesEnabledrelayprovider": True,
        #         "__relay_internal__pv__AbraComposedTextWidgetsrelayprovider": False,
        #         "__relay_internal__pv__AbraSearchReferencesHovercardEnabledrelayprovider": True,
        #         "__relay_internal__pv__AbraCardNavigationCountrelayprovider": True,
        #         "__relay_internal__pv__AbraDebugDevOnlyrelayprovider": False,
        #         "__relay_internal__pv__AbraHasNuxTourrelayprovider": True,
        #         "__relay_internal__pv__AbraQPSidebarNuxTriggerNamerelayprovider": "meta_dot_ai_abra_web_message_actions_sidebar_nux_tour",
        #         "__relay_internal__pv__AbraSurfaceNuxIDrelayprovider": "12177",
        #         "__relay_internal__pv__AbraFileUploadsrelayprovider": False,
        #         "__relay_internal__pv__AbraQPDocUploadNuxTriggerNamerelayprovider": "meta_dot_ai_abra_web_doc_upload_nux_tour",
        #         "__relay_internal__pv__AbraQPFileUploadTransparencyDisclaimerTriggerNamerelayprovider": "meta_dot_ai_abra_web_file_upload_transparency_disclaimer",
        #         "__relay_internal__pv__AbraArtifactsRenamingEnabledrelayprovider": False,
        #         "__relay_internal__pv__AbraArtifactEditorDebugModerelayprovider": False,
        #         "__relay_internal__pv__AbraArtifactSharingrelayprovider": False,
        #         "__relay_internal__pv__AbraArtifactEditorSaveEnabledrelayprovider": False,
        #         "__relay_internal__pv__AbraArtifactEditorDownloadHTMLEnabledrelayprovider": False,
        #     }),
        #     "server_timestamps": "true",
        #     # "doc_id": "9989258121106915",
        # }
        
        # files_data = {key: (None, value) for key, value in payload.items()}

        # cookies = {
        #     'datr': '8z6zZ47cCBteonajt9lNN6ZH',
        #     'wd': '1536x391',
        #     'dpr': '1.25',
        #     'abra_csrf': 'nm_DSKjmpHVdZ50KduAaJQ',
        # }

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
        #     'Accept': '*/*',
        #     'Accept-Language': 'en-US,en;q=0.5',
        #     'Referer': 'https://www.meta.ai/',
        #     'Origin': 'https://www.meta.ai',
        #     'DNT': '1',
        #     'Sec-GPC': '1',
        #     'Connection': 'keep-alive',
        #     # 'Cookie': 'datr=8z6zZ47cCBteonajt9lNN6ZH; wd=1536x391; dpr=1.25; abra_csrf=nm_DSKjmpHVdZ50KduAaJQ',
        #     'Sec-Fetch-Dest': 'empty',
        #     'Sec-Fetch-Mode': 'cors',
        #     'Sec-Fetch-Site': 'same-site',
        #     'Priority': 'u=0',
        #     'Pragma': 'no-cache',
        #     'Cache-Control': 'no-cache',
        # }

        # params = {
        #     'locale': 'user',
        # }

        # files = {
        #     'av': (None, '0'),
        #     'access_token': (None, 'ABRAQWZAKaUlkVHpEZAXFsU05KUVBya0RzdURhc1B4VGxybDAtaXgxYjExVHp0LUhORW9ReWx2ZAnl6N3dhYmVpUzVkVTNuNjFqRjFQdHdUT3ROVnRWNEhLcWlPRXhZAQTJzNlhKMm9sV2hWLUFRMTdFZATRYNGtBczRCUUZAXRkNzRWQ2cTVqRVVkNi1zdzllcHAtMmxmcnVoM0wxUUw4V2x4dmJQaVR5NXV0WXNhM1ZA0cGNn'),
        #     '__user': (None, '0'),
        #     '__a': (None, '1'),
        #     '__req': (None, 'w'),
        #     '__hs': (None, '20136.HYP:abra_pkg.2.1...0'),
        #     'dpr': (None, '1'),
        #     '__ccg': (None, 'GOOD'),
        #     '__rev': (None, '1020162270'),
        #     '__s': (None, ':k08mgw:mylulf'),
        #     '__hsi': (None, '7472385425817791270'),
        #     '__dyn': (None, '7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D85m1mzXwae4UaEW4U2FwNwmE2eU5O0EoS10w5NyES0gq0Lo6-3u362q0XU6O1FwlU18ouwKxvzU5K0UE'),
        #     '__csr': (None, 'gvNfbibGPfXmgJaExoKdlx2EOeK2rh9by8W00ksG17xi5WwjU4G14w4sw5DEs3-vamhOBCwlA09nEMeFaw10Zd0Qg0YyEijjg5a0k2qew9C0l24Q489o0O-l04Vw97xCEZPKA1j2oCkwG82r7S9P1uu16x20EwDaViwBga8Z1xADgDw2nabeEhgGsa04pDxehwLbo2rDmxM'),
        #     '__comet_req': (None, '46'),
        #     'lsd': (None, 'AVqjUAscjbc'),
        #     'jazoest': (None, '21037'),
        #     '__spin_r': (None, '1020162270'),
        #     '__spin_b': (None, 'trunk'),
        #     '__spin_t': (None, '1739800307'),
        #     '__jssesw': (None, '1'),
        #     'fb_api_caller_class': (None, 'RelayModern'),
        #     'fb_api_req_friendly_name': (None, 'useAbraSendMessageMutation'),
        #     'variables': (None, '{"message":{"sensitive_string_value": ' + f'"{user_input}" ' + 
        #                   '},"externalConversationId":"f7f30817-213b-4796-980c-ab7c7041aec0","offlineThreadingId":"7297270696784771481","suggestedPromptIndex":null,"flashPreviewInput":null,"promptPrefix":null,"entrypoint":"ABRA__CHAT__TEXT","icebreaker_type":"TEXT_V2","attachments":[],"attachmentsV2":[],"activeMediaSets":null,"activeCardVersions":[],"activeArtifactVersion":null,"userUploadEditModeInput":null,"reelComposeInput":null,"qplJoinId":"f2863848412823fa6","gkAbraArtifactsEnabled":false,"model_preference_override":null,"threadSessionId":"c91f92f6-76b1-4171-b8af-37bdababaae0","__relay_internal__pv__AbraPinningConversationsrelayprovider":false,"__relay_internal__pv__AbraArtifactsEnabledrelayprovider":false,"__relay_internal__pv__WebPixelRatiorelayprovider":1,"__relay_internal__pv__AbraSearchInlineReferencesEnabledrelayprovider":true,"__relay_internal__pv__AbraComposedTextWidgetsrelayprovider":false,"__relay_internal__pv__AbraSearchReferencesHovercardEnabledrelayprovider":true,"__relay_internal__pv__AbraCardNavigationCountrelayprovider":true,"__relay_internal__pv__AbraDebugDevOnlyrelayprovider":false,"__relay_internal__pv__AbraHasNuxTourrelayprovider":true,"__relay_internal__pv__AbraQPSidebarNuxTriggerNamerelayprovider":"meta_dot_ai_abra_web_message_actions_sidebar_nux_tour","__relay_internal__pv__AbraSurfaceNuxIDrelayprovider":"12177","__relay_internal__pv__AbraFileUploadsrelayprovider":false,"__relay_internal__pv__AbraQPDocUploadNuxTriggerNamerelayprovider":"meta_dot_ai_abra_web_doc_upload_nux_tour","__relay_internal__pv__AbraQPFileUploadTransparencyDisclaimerTriggerNamerelayprovider":"meta_dot_ai_abra_web_file_upload_transparency_disclaimer","__relay_internal__pv__AbraUpsellsKillswitchrelayprovider":true,"__relay_internal__pv__AbraIcebreakerImagineFetchCountrelayprovider":20,"__relay_internal__pv__AbraImagineYourselfIcebreakersrelayprovider":false,"__relay_internal__pv__AbraEmuReelsIcebreakersrelayprovider":false,"__relay_internal__pv__AbraArtifactsDisplayHeaderV2relayprovider":false,"__relay_internal__pv__AbraArtifactEditorDebugModerelayprovider":false,"__relay_internal__pv__AbraArtifactSharingrelayprovider":false,"__relay_internal__pv__AbraArtifactEditorSaveEnabledrelayprovider":false,"__relay_internal__pv__AbraArtifactEditorDownloadHTMLEnabledrelayprovider":false,"__relay_internal__pv__AbraArtifactsRenamingEnabledrelayprovider":false}'),
        #     'server_timestamps': (None, 'true'),
        #     'doc_id': (None, '9989258121106915'),
        # }
        # input()

        original_dict = json.loads(files['variables'][1])
        new_dict = original_dict["message"]["sensitive_string_value"] = user_input
        files['variables'] = (None,json.dumps(original_dict))


        def get_nested(data, keys, default=None):
            """
            Retrieve a nested value from a dictionary.
            
            :param data: The dictionary to traverse.
            :param keys: A list of keys representing the path.
            :param default: The value to return if any key is missing.
            :return: The nested value or default.
            """
            for key in keys:
                try:
                    data = data[key]
                except (KeyError, TypeError):
                    return default
            return data

        def pretty_output(llm_input: str):
            llm_json = json.loads(llm_input)
            output = get_nested(llm_json, ['data', 'node', 'bot_response_message','snippet'])
            return output

        def stream_generator():
            decoded_line = None
            while True:
                try:
                    # Use streaming mode with a timeout
                    with requests.post(url, headers=headers, params=params, files=files ,cookies=cookies, stream=True, timeout=120) as response:
        # response = requests.post('https://graph.meta.ai/graphql', params=params, cookies=cookies, headers=headers, files=files)

                        # If the response is gzip-encoded, decode it accordingly.
                        if response.headers.get("Content-Encoding") == "gzip":
                            buf = io.BytesIO(response.content)
                            with gzip.GzipFile(fileobj=buf) as f:
                                # Read the entire content first (if that suits your use case)
                                decoded_output = f.read().decode("utf-8", errors="replace")
                                if PRINT_LOGS : print("decoded_output -> ", decoded_output)
                                # yield decoded_output
                        else:
                            # Otherwise, iterate over response lines
                            for line in response.iter_lines():
                                if line:
                                    decoded_line = line.decode("utf-8", errors="replace") + "\n"
                                    if PRINT_LOGS : print("decoded_line -> ", decoded_line)
                                    output = pretty_output(decoded_line)
                                    if output : 
                                        print(output)
                                        yield output
                    break  # Break the while loop if the request finished successfully
                except (requests.exceptions.ConnectionError, requests.exceptions.ChunkedEncodingError) as e:
                    yield f"Connection error (possibly broken pipe): {e}. Retrying in 5 seconds...\n"
                    time.sleep(5)
                except Exception as e:
                    yield f"Unexpected error: {e}\nRetrying in 5 seconds...\n"
                    # print(e)
                    # return
                    time.sleep(5)

            decoded_line = pretty_output(decoded_line)
            if decoded_line: 
                print(decoded_line)
                yield decoded_line

        # You can either stream the data back to the client or process it as needed.
        # Here we stream it back:
        return StreamingHttpResponse(stream_generator(), content_type="text/plain")
    
    # For GET requests, simply render the form.
    return render(request, "meta_index.html")
