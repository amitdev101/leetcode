// Listen for the browser action icon click
browser.browserAction.onClicked.addListener((tab) => {
    // Inject the content script into the current tab
    browser.tabs.executeScript(tab.id, {
      file: "content_script.js"
    });
  });
  