import requests

cookies = {
    'datr': '8uupZlCR2uqV8AWE67fA8GWy',
    'ps_l': '1',
    'ps_n': '1',
    'abra_csrf': 'RC5piFE75eK35OxXOObZNv',
    'wd': '1536x363',
    'dpr': '1.25',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.meta.ai/',
    'Origin': 'https://www.meta.ai',
    'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'datr=8uupZlCR2uqV8AWE67fA8GWy; ps_l=1; ps_n=1; abra_csrf=RC5piFE75eK35OxXOObZNv; wd=1536x363; dpr=1.25',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-GPC': '1',
    'Priority': 'u=0',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

params = {
    'locale': 'user',
}

files = {
    'av': (None, '0'),
    'access_token': (None, 'ABRAQWZAKSmVCRm9vWVVHN0EweXZANSG5vZAkZAqYTRWSExRSUc2Q3dJOEZAfeUZAGRTc1UFJjeHpMa0xWakh2elA1MnRFTUtuN0JpdG1GQmZAuX3NLN2YydGE3X05Uc2tLZAG5lRlFMcjR5SHRKM2cwT21vWmdaRDNpNEpBc3pwcXdzTEM2YmZAHZAlFULXRleTFXWjM4ZAjZANMy0zaHVJZAGFuSVVjbzl1RzMtV3BtbzJPTmFsaVFMMW5XUQZDZD'),
    '__user': (None, '0'),
    '__a': (None, '1'),
    '__req': (None, '8'),
    '__hs': (None, '20145.HYP:abra_pkg.2.1...0'),
    'dpr': (None, '1'),
    '__ccg': (None, 'GOOD'),
    '__rev': (None, '1020404362'),
    '__s': (None, 'h3zt4k:p20ud9:6efv5w'),
    '__hsi': (None, '7475647238998894935'),
    '__dyn': (None, '7xeUmwlEnwn8K2Wmh0no6u5U4e0yoW3q32360CEbo19oe8hw2nVE4W099w8G1Dz81s8hwnU2lwv89k2C1Fwc60D85m1mzXwae4UaEW4U2FwNwmE2eU5O0EoS0raazo11E2ZwrUdUco9E3Lwr86C1nw4xxW2W5-fwmU3yw'),
    '__csr': (None, 'gsj9-J5WGJkIF4rBmGChFm8x6uVUG7qBz44E-GgC00kmSmiE9o2ew6mwvVB82K0GjwbTxi8EIWx64k083x5ajyJw7GrCBy9A08KgjiU0EW0byG582vU-0Vo5092GbxTy8dA0dkDU1lr8jiSvBo7A9ypi2Hq2r2tBCokxe32dwn40DEd205nhO1h02kwC9B851lwLoR2Fk1wix51glo4oGw'),
    '__comet_req': (None, '46'),
    'lsd': (None, 'AVrs85QL4Pw'),
    'jazoest': (None, '2897'),
    '__spin_r': (None, '1020404362'),
    '__spin_b': (None, 'trunk'),
    '__spin_t': (None, '1740559758'),
    '__jssesw': (None, '1'),
    'fb_api_caller_class': (None, 'RelayModern'),
    'fb_api_req_friendly_name': (None, 'useAbraSendMessageMutation'),
    'variables': (None, '{"message":{"sensitive_string_value":"test"},"externalConversationId":"f5c50b62-c3c5-4bc0-8b22-8fdc90b57ed3","offlineThreadingId":"7300436828258233368","suggestedPromptIndex":null,"flashPreviewInput":null,"promptPrefix":null,"entrypoint":"ABRA__CHAT__TEXT","icebreaker_type":"TEXT_V2","attachments":[],"attachmentsV2":[],"activeMediaSets":null,"activeCardVersions":[],"activeArtifactVersion":null,"userUploadEditModeInput":null,"reelComposeInput":null,"qplJoinId":"fb989272ef29dcb0f","gkAbraArtifactsEnabled":false,"model_preference_override":null,"threadSessionId":"7af32f96-2147-440f-8c9f-993ebe3606c1","__relay_internal__pv__AbraPinningConversationsrelayprovider":false,"__relay_internal__pv__AbraArtifactsEnabledrelayprovider":false,"__relay_internal__pv__WebPixelRatiorelayprovider":1,"__relay_internal__pv__AbraSearchInlineReferencesEnabledrelayprovider":true,"__relay_internal__pv__AbraComposedTextWidgetsrelayprovider":false,"__relay_internal__pv__AbraSearchReferencesHovercardEnabledrelayprovider":true,"__relay_internal__pv__AbraCardNavigationCountrelayprovider":true,"__relay_internal__pv__AbraDebugDevOnlyrelayprovider":false,"__relay_internal__pv__AbraHasNuxTourrelayprovider":true,"__relay_internal__pv__AbraQPSidebarNuxTriggerNamerelayprovider":"meta_dot_ai_abra_web_message_actions_sidebar_nux_tour","__relay_internal__pv__AbraSurfaceNuxIDrelayprovider":"12177","__relay_internal__pv__AbraFileUploadsrelayprovider":false,"__relay_internal__pv__AbraQPDocUploadNuxTriggerNamerelayprovider":"meta_dot_ai_abra_web_doc_upload_nux_tour","__relay_internal__pv__AbraQPFileUploadTransparencyDisclaimerTriggerNamerelayprovider":"meta_dot_ai_abra_web_file_upload_transparency_disclaimer","__relay_internal__pv__AbraUpsellsKillswitchrelayprovider":true,"__relay_internal__pv__AbraIcebreakerImagineFetchCountrelayprovider":20,"__relay_internal__pv__AbraImagineYourselfIcebreakersrelayprovider":false,"__relay_internal__pv__AbraEmuReelsIcebreakersrelayprovider":false,"__relay_internal__pv__KadabraArtifactsRewriteV2relayprovider":false,"__relay_internal__pv__AbraArtifactsDisplayHeaderV2relayprovider":false,"__relay_internal__pv__AbraArtifactEditorDebugModerelayprovider":false,"__relay_internal__pv__AbraArtifactSharingrelayprovider":false,"__relay_internal__pv__AbraArtifactEditorSaveEnabledrelayprovider":false,"__relay_internal__pv__AbraArtifactEditorDownloadHTMLEnabledrelayprovider":false,"__relay_internal__pv__AbraArtifactsRenamingEnabledrelayprovider":false}'),
    'server_timestamps': (None, 'true'),
    'doc_id': (None, '9521084381284826'),
}

# response = requests.post('https://graph.meta.ai/graphql', params=params, cookies=cookies, headers=headers, files=files)