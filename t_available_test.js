function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function simulateMouseMove() {
    const x = getRandomInt(0, window.innerWidth);
    const y = getRandomInt(0, window.innerHeight);
    const event = new MouseEvent('mousemove', {
        bubbles: true,
        cancelable: true,
        view: window,
        clientX: x,
        clientY: y
    });
    document.dispatchEvent(event);
}

function simulateTyping() {
    const inputFields = document.querySelectorAll('input, textarea');
    if (inputFields.length > 0) {
        const inputField = inputFields[getRandomInt(0, inputFields.length - 1)];
        inputField.focus();
        inputField.value += String.fromCharCode(getRandomInt(65, 90)); // Random uppercase letter
        inputField.dispatchEvent(new Event('input', { bubbles: true }));
    }
}

function humanLikeActivity() {
    const actions = [simulateMouseMove, simulateTyping];
    const action = actions[getRandomInt(0, actions.length - 1)];
    action();
}

// Ensure activity every 10 to 30 seconds, even if the tab isn't active
setInterval(humanLikeActivity, getRandomInt(10000, 30000)); // 10 to 30 seconds
