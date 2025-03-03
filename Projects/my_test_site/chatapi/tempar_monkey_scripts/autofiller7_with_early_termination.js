// ==UserScript==
// @name         ChatGPT Auto Filler with API Capture & Redis Storage (Streaming, Progress Updates & Early Termination)
// @namespace    http://tampermonkey.net/
// @version      4.7
// @description  Fetches chat input from Redis, submits it in ChatGPT, intercepts streaming API responses, updates progress in real time, and can terminate early upon detecting a termination string. Includes extensive logging and a toggle button.
// @match        https://chatgpt.com/*
// @run-at       document-start
// @grant        GM_xmlhttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// @grant        GM_addElement
// ==/UserScript==

(function() {
    'use strict';

    // Debug flag to control logging verbosity
    const DEBUG = true;

    // Endpoints for your Django API
    const REDIS_API_URL = "http://127.0.0.1:8000/api/get/chat_input/";
    const DELETE_REDIS_API_URL = "http://127.0.0.1:8000/api/delete/chat_input/";
    const SAVE_RESPONSE_TO_REDIS_URL = "http://127.0.0.1:8000/api/set/chat_response/";
    const SAVE_PROGRESS_URL = "http://127.0.0.1:8000/api/set/chat_response/"; // Endpoint for progress updates
    const CHECK_INTERVAL = 5000; // Check Redis every 5 seconds

    let lastMessage = null; // To prevent duplicate submissions
    let scriptEnabled = GM_getValue("scriptEnabled", true); // Retrieve saved state

    // Variable to accumulate streaming response chunks
    let cumulativeResponse = "";

    // Logging helper functions
    function logInfo(message, data) {
        if (DEBUG) console.log("[INFO]", message, data || "");
    }
    function logWarn(message, data) {
        if (DEBUG) console.warn("[WARN]", message, data || "");
    }
    function logError(message, data) {
        if (DEBUG) console.error("[ERROR]", message, data || "");
    }

    logInfo("Main script loaded at document-start. Starting up...");

    // Create a floating toggle button at the top-right corner
    function createToggleButton() {
        logInfo("Creating toggle button...");
        let button = document.createElement("button");
        button.id = "toggle-script-btn";
        button.innerText = scriptEnabled ? "⏸ Pause Auto-Fill" : "▶ Start Auto-Fill";
        button.style.position = "fixed";
        button.style.top = "10px";
        button.style.right = "10px";
        button.style.zIndex = "10000";
        button.style.backgroundColor = scriptEnabled ? "red" : "green";
        button.style.color = "white";
        button.style.border = "none";
        button.style.padding = "10px 15px";
        button.style.borderRadius = "5px";
        button.style.cursor = "pointer";
        button.style.fontSize = "14px";
        document.addEventListener("DOMContentLoaded", function() {
            document.body.appendChild(button);
            logInfo("Toggle button appended to document.");
        });
        button.addEventListener("click", () => {
            scriptEnabled = !scriptEnabled;
            GM_setValue("scriptEnabled", scriptEnabled);
            button.innerText = scriptEnabled ? "⏸ Pause Auto-Fill" : "▶ Start Auto-Fill";
            button.style.backgroundColor = scriptEnabled ? "red" : "green";
            logInfo("Toggle button clicked. Script is now", scriptEnabled ? "ACTIVE" : "PAUSED");
        });
        logInfo("Toggle button created.");
    }

    // Fetch chat input from Redis via your Django API
    function fetchChatInput(callback) {
        if (!scriptEnabled) {
            logInfo("Script is paused. Skipping fetchChatInput.");
            return;
        }
        logInfo("Fetching chat input from Redis...");
        GM_xmlhttpRequest({
            method: "GET",
            url: REDIS_API_URL,
            headers: { "Accept": "application/json" },
            onload: function(response) {
                logInfo("Received response from Redis GET:", response.responseText);
                try {
                    let data = JSON.parse(response.responseText);
                    if (data.data && data.data !== lastMessage) {
                        logInfo("New message found in Redis:", data.data);
                        lastMessage = data.data;
                        callback(data.data);
                    } else {
                        logInfo("No new chat_input found in Redis or duplicate message.");
                    }
                } catch (e) {
                    logError("Error parsing Redis response:", e);
                }
            },
            onerror: function(error) {
                logError("Error fetching from Redis:", error);
            }
        });
    }

    // Wait for an element to appear on the page
    function waitForElement(selector, callback, timeout = 10000) {
        logInfo("Waiting for element:", selector);
        const startTime = Date.now();
        const interval = setInterval(() => {
            const element = document.querySelector(selector);
            if (element) {
                clearInterval(interval);
                logInfo("Element found:", selector);
                callback(element);
            }
            if (Date.now() - startTime > timeout) {
                clearInterval(interval);
                logWarn("Element not found within timeout:", selector);
            }
        }, 500);
    }

    // Insert the message into ChatGPT's input field and trigger submission
    function insertAndSubmitMessage(element, message) {
        if (!scriptEnabled) {
            logInfo("Script is paused. Skipping insertAndSubmitMessage.");
            return;
        }
        logInfo("Inserting message into ChatGPT input field:", message);
        element.innerHTML = message;
        element.dispatchEvent(new Event('input', { bubbles: true }));

        setTimeout(() => {
            let sendButton = document.querySelector('button[data-testid="send-button"]');
            if (sendButton) {
                logInfo("Send button found. Clicking send button...");
                sendButton.click();
                logInfo("Message submitted via send button:", message);
                deleteRedisKey();
            } else {
                logWarn("Send button not found. Attempting to submit using Enter key.");
                element.dispatchEvent(new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                }));
                logInfo("Message submitted via Enter key:", message);
                deleteRedisKey();
            }
        }, 1500);
    }

    // Delete the Redis key after submission
    function deleteRedisKey() {
        logInfo("Attempting to delete Redis key...");
        GM_xmlhttpRequest({
            method: "DELETE",
            url: DELETE_REDIS_API_URL,
            onload: function(response) {
                logInfo("Redis key deleted successfully. Response:", response.responseText);
            },
            onerror: function(error) {
                logError("Failed to delete Redis key:", error);
            }
        });
    }

    // Send the captured final response to Redis via your Django API
    function sendResponseToRedis(responseText) {
        logInfo("Sending captured final response to Redis...", responseText);
        GM_xmlhttpRequest({
            method: "POST",
            url: SAVE_RESPONSE_TO_REDIS_URL,
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({ response: responseText }),
            onload: function(response) {
                logInfo("Final ChatGPT response saved to Redis.", response.responseText);
            },
            onerror: function(error) {
                logError("Failed to save final response to Redis:", error);
            }
        });
    }

    // Update progress in Redis via your Django API
    function updateProgressToRedis(progressText) {
        logInfo("Updating progress to Redis...", progressText);
        GM_xmlhttpRequest({
            method: "POST",
            url: SAVE_PROGRESS_URL,
            headers: {
                "Content-Type": "application/json"
            },
            data: JSON.stringify({ response: progressText }),
            onload: function(response) {
                logInfo("Progress updated in Redis.", response.responseText);
            },
            onerror: function(error) {
                logError("Failed to update progress to Redis:", error);
            }
        });
    }

    // Inject fetch-interception code as an external script to bypass CSP restrictions
    function injectFetchInterceptor() {
        logInfo("Injecting fetch interception code via external script...");
        const code = `
            (function() {
                console.log("Setting up fetch interception for streaming responses...");
                const TERMINATION_STRING = "[DONE]";  // Adjust termination string as needed.
                const originalFetch = window.fetch;
                window.fetch = async function(url, options) {
                    if (url.includes("/backend-api/conversation")) {
                        console.log("Intercepting API request to:", url);
                        console.log("Request options:", options);
                    }
                    const response = await originalFetch(url, options);
                    if (url.includes("/backend-api/conversation")) {
                        console.log("Capturing streaming response from:", url);
                        try {
                            const clone = response.clone();
                            if (clone.body) {
                                const reader = clone.body.getReader();
                                const decoder = new TextDecoder("utf-8");
                                let result = "";
                                let done = false;
                                while (!done) {
                                    const { done: doneReading, value } = await reader.read();
                                    done = doneReading;
                                    if (value) {
                                        const chunk = decoder.decode(value, { stream: true });
                                        result += chunk;
                                        console.log("Received chunk:", chunk);
                                        // Dispatch progress update event for each chunk (non-cumulative: only the new chunk)
                                        const chunkEvent = new CustomEvent("capturedResponseChunk", { detail: { chunk: chunk } });
                                        window.dispatchEvent(chunkEvent);
                                        // Check for termination string in the current chunk
                                        if (chunk.includes(TERMINATION_STRING)) {
                                            console.log("Termination string detected. Ending stream early.");
                                            done = true;
                                            break;
                                        }
                                    }
                                }
                                result += decoder.decode();
                                console.log("Captured streaming response body:", result);
                                // Dispatch final event with full response.
                                const finalEvent = new CustomEvent("capturedResponse", { detail: { response: result } });
                                window.dispatchEvent(finalEvent);
                            } else {
                                console.log("No body in the streaming response.");
                            }
                        } catch (e) {
                            console.error("Error during streaming response interception:", e);
                        }
                    }
                    return response;
                };
            })();
        `;
        const blob = new Blob([code], { type: 'text/javascript' });
        const scriptUrl = URL.createObjectURL(blob);
        GM_addElement(document.head, 'script', { src: scriptUrl });
    }

    // Listen for progress events (each chunk) and update cumulative response and Redis progress.
    window.addEventListener("capturedResponseChunk", function(e) {
        const chunk = e.detail.chunk;
        cumulativeResponse += chunk;
        logInfo("Received chunk event:", chunk);
        updateProgressToRedis(cumulativeResponse);
    });

    // Listen for the final captured response event dispatched by the injected script.
    window.addEventListener("capturedResponse", function(e) {
        logInfo("Main script received final captured response event:", e.detail.response);
        sendResponseToRedis(e.detail.response);
    });

    // Monitor Redis for new messages to send to ChatGPT.
    function startMonitoring() {
        logInfo("Starting monitoring of Redis for new messages...");
        setInterval(() => {
            if (!scriptEnabled) {
                logInfo("Script is paused. Skipping monitoring cycle.");
                return;
            }
            logInfo("Heartbeat: Checking Redis for new messages...");
            fetchChatInput((message) => {
                waitForElement('p[data-placeholder="Ask anything"]', (element) => {
                    insertAndSubmitMessage(element, message);
                });
            });
        }, CHECK_INTERVAL);
    }

    // Initialize the script components.
    createToggleButton();
    startMonitoring();
    injectFetchInterceptor();

    document.addEventListener("DOMContentLoaded", () => {
        logInfo("DOM fully loaded and parsed.");
    });
})();
