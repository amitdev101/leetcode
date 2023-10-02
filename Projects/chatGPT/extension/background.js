// // Listen for messages from the popup script
// browser.runtime.onMessage.addListener(function(message, sender, sendResponse) {
//     if (message.action === 'executeCode') {
//         browser.tabs.executeScript({
//             code: message.code
//         }).then(sendResponse);
//     }
//     return true; // indicates the response is sent asynchronously
// });

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'executeCode') {
        chrome.tabs.executeScript({
            code: message.code
        }, function(result) {
            sendResponse(result);
        });
    }
    return true; // indicates the response is sent asynchronously
});
