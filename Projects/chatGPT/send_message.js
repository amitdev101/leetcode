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
typeAndSend("It's working");
