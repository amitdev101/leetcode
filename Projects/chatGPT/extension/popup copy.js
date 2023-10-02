browser.tabs.query({active: true, currentWindow: true}).then(tabs => {
    let currentTab = tabs[0];
    console.log(currentTab.url);
}).catch(error => {
    console.error(error);
});

console.log(document.body.outerHTML);


document.addEventListener("DOMContentLoaded", function() {
    let textarea = document.querySelector('textarea[placeholder="Send a message"]');
    console.log(textarea);
});




document.getElementById('submitBtn').addEventListener('click', function() {
  console.log("Submit button called");
  let fileInput = document.getElementById('fileInput');
  let textArea = document.getElementById('textArea');

  let text = textArea.value;
  if (fileInput.files.length) {
    let reader = new FileReader();
    reader.onload = function() {
      text = reader.result;
      sendMessage(text);
    };
    reader.readAsText(fileInput.files[0]);
  } else {
    sendMessage(text);
  }
});

function typeAndSend(message) {
    // Step 1: Find the textarea using its placeholder
    const textarea = document.querySelector('textarea[placeholder="Send a message"]');
    
    // Check if the textarea exists
    if (!textarea) {
        console.error("Could not find the textarea.");
        return;
    }

    // Step 2: Set the provided message into the textarea
    textarea.value = message;

    // Optional: Trigger any 'input' events that might be associated with the textarea
    const inputEvent = new Event('input', {
        'bubbles': true,
        'cancelable': true
    });
    textarea.dispatchEvent(inputEvent);

    // Step 3: Find the associated button
    const button = document.querySelector('button[data-testid="send-button"]');
    
    // Check if the button exists
    if (!button) {
        console.error("Could not find the send button.");
        return;
    }

    // Step 4: Simulate a click event on the button
    const clickEvent = new MouseEvent('click', {
        'bubbles': true,
        'cancelable': true,
        'view': window
    });
    // button.dispatchEvent(clickEvent);
    // Introduce a delay before clicking the button
    setTimeout(() => {
        button.dispatchEvent(clickEvent);
    }, 1000); // Adjust delay as needed
}

// Usage
// typeAndSend("It's working");


function sendMessage(message) {
  // Split the message into parts of less than 3000 characters
  let parts = [];
  for (let i = 0; i < message.length; i += 3000) {
    parts.push(message.substring(i, i + 3000));
  }

  parts.forEach((part, index) => {
    // Here, you can execute your function to input the text into the website and submit
    // ...
    typeAndSend(`myfile: part ${index}` + part);
  });
}
