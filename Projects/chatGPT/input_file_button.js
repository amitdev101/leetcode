function addInputButton() {
    // Create the file input element
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.id = 'fileInput';

    // Create the submit button
    const submitButton = document.createElement('button');
    submitButton.innerText = 'Submit File';
    submitButton.addEventListener('click', processFile);

    // Styling for the fixed position of file input
    fileInput.style.position = 'fixed';
    fileInput.style.top = '10px';
    fileInput.style.right = '120px'; // Adjusted for visibility
    fileInput.style.zIndex = '5000'; // Increased z-index

    // Styling for the fixed position of submit button
    submitButton.style.position = 'fixed';
    submitButton.style.top = '10px';
    submitButton.style.right = '10px'; // Adjusted for visibility
    submitButton.style.zIndex = '5000'; // Increased z-index
    submitButton.style.backgroundColor = 'blue'; // Added background color
    submitButton.style.color = 'white'; // Text color for better contrast
    submitButton.style.padding = '5px 10px'; // Padding for aesthetics
    submitButton.style.border = 'none'; // Removing default borders
    submitButton.style.borderRadius = '5px'; // Rounded corners for aesthetics

    document.body.appendChild(fileInput);
    document.body.appendChild(submitButton);
}


function processFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(event) {
        const content = event.target.result;
        splitAndSend(content);
    };

    reader.readAsText(file);
}

function splitAndSend(content) {
    const charsPerPage = 3000;
    const totalPages = Math.ceil(content.length / charsPerPage);
    const delayMillis = 5000;

    for(let i = 0; i < totalPages; i++) {
        const start = i * charsPerPage;
        const end = start + charsPerPage;
        const pageContent = content.slice(start, end);
        // send_msg(pageContent);
        setTimeout(() => {
            send_msg(pageContent);
        }, delayMillis * i);
    }
}

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

// Your send_msg function goes here.
function send_msg(message) {
    // Your code to send the message.
    // console.log(message); // For demonstration purposes.
    typeAndSend(message);

}

// Invoke the function to add the input button
addInputButton();
