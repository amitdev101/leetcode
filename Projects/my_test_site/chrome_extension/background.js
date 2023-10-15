setInterval(function() {
    fetch('http://localhost:8000/myapp/chrome_extension/')
        .then(response => response.json())
        .then(data => {
            const command = data.command;
            if (command) {
                // Execute the command on the web page or wherever necessary
                console.log("Received command:", command);
                // TODO: Implement logic to execute the command on the current tab or as needed.
                const dataToSend = {
                    message: "The message or data you want to send to Telegram"
                };
                
                fetch('http://YOUR_DJANGO_SERVER_URL/send_to_telegram/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        // Add any other necessary headers, e.g. for authentication
                    },
                    body: JSON.stringify(dataToSend)
                })
            }
        });
}, 5000);  // Poll every 5 seconds
