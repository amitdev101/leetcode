// ==UserScript==
// @name         ChatGPT Auto Filler from Redis (CSP Bypass)
// @namespace    http://tampermonkey.net/
// @version      3.1
// @description  Fetches chat input from Redis and submits it in ChatGPT, continuously checking every 10 seconds
// @author       Zibran
// @match        https://chatgpt.com/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    const REDIS_API_URL = "http://127.0.0.1:8000/api/get/chat_input/";
    const CHECK_INTERVAL = 1000; // Check every 10 seconds

    function fetchChatInput(callback) {
        GM_xmlhttpRequest({
            method: "GET",
            url: REDIS_API_URL,
            headers: { "Accept": "application/json" },
            onload: function(response) {
                try {
                    let data = JSON.parse(response.responseText);
                    if (data.data) {
                        console.log("✅ Found chat_input in Redis:", data.data);
                        callback(data.data);
                    } else {
                        console.log("⚠️ chat_input key not found in Redis.");
                    }
                } catch (e) {
                    console.error("❌ Error parsing Redis response:", e);
                }
            },
            onerror: function(error) {
                console.error("❌ Error fetching from Redis:", error);
            }
        });
    }

    function waitForElement(selector, callback, timeout = 10000) {
        const startTime = Date.now();
        const interval = setInterval(() => {
            const element = document.querySelector(selector);
            if (element) {
                clearInterval(interval);
                callback(element);
            }
            if (Date.now() - startTime > timeout) {
                clearInterval(interval);
                console.log("⏳ ChatGPT input field not found within timeout.");
            }
        }, 500);
    }

    function insertAndSubmitMessage(element, message) {
        element.innerHTML = message;
        element.dispatchEvent(new Event('input', { bubbles: true }));

        setTimeout(() => {
            element.dispatchEvent(new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                keyCode: 13,
                which: 13,
                bubbles: true
            }));
            console.log("🚀 Message submitted:", message);
        }, 1000);
    }

    function startMonitoring() {
        console.log("🟢 ChatGPT Auto Filler is now active...");

        setInterval(() => {
            console.log("💓 Heartbeat: Checking Redis...");
            fetchChatInput((message) => {
                waitForElement('p[data-placeholder="Ask anything"]', (element) => {
                    insertAndSubmitMessage(element, message);
                });
            });
        }, CHECK_INTERVAL);
    }

    // Start monitoring Redis
    startMonitoring();

})();
