// ==UserScript==
// @name         ChatGPT Auto Filler from Redis (Optimized)
// @namespace    http://tampermonkey.net/
// @version      3.2
// @description  Fetches chat input from Redis, submits it in ChatGPT, and deletes it after use.
// @author       Zibran
// @match        https://chatgpt.com/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    const REDIS_API_URL = "http://127.0.0.1:8000/api/get/chat_input/";
    const DELETE_REDIS_API_URL = "http://127.0.0.1:8000/api/delete/chat_input/";
    const CHECK_INTERVAL = 5000; // Check Redis every 5 seconds

    let lastMessage = null; // Store the last used message to prevent re-submission

    function fetchChatInput(callback) {
        GM_xmlhttpRequest({
            method: "GET",
            url: REDIS_API_URL,
            headers: { "Accept": "application/json" },
            onload: function(response) {
                try {
                    let data = JSON.parse(response.responseText);
                    if (data.data && data.data !== lastMessage) {
                        console.log("✅ New message found in Redis:", data.data);
                        lastMessage = data.data;
                        callback(data.data);
                    } else {
                        console.log("⚠️ No new chat_input found in Redis.");
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
            let sendButton = document.querySelector('button[data-testid="send-button"]');
            if (sendButton) {
                sendButton.click();
                console.log("🚀 Message submitted:", message);
                deleteRedisKey(); // Delete key after sending
            } else {
                console.log("⚠️ Send button not found, trying Enter key.");
                element.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                }));
                deleteRedisKey(); // Delete key after sending
            }
        }, 1500); // Wait a bit before submitting
    }

    function deleteRedisKey() {
        GM_xmlhttpRequest({
            method: "DELETE",
            url: DELETE_REDIS_API_URL,
            onload: function(response) {
                console.log("🗑️ Redis key deleted after submission.");
            },
            onerror: function(error) {
                console.error("❌ Failed to delete Redis key:", error);
            }
        });
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
