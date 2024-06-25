function cleanUpHtmlContent() {
    const problematicDiv = document.querySelector('.dark');

    if (!problematicDiv) {
        console.error('The specified element was not found on the page.');
        return;
    }

    // Flag to indicate the task is complete
    let taskCompleted = false;

    function removeProblematicElements(element) {
        if (taskCompleted) {
            return; // Prevent further processing once task is completed
        }

        try {
            const spans = element.querySelectorAll('span');
            spans.forEach(span => {
                if (span.textContent.trim().toLowerCase() === 'java' && span.parentNode) {
                    span.parentNode.removeChild(span);
                }
            });

            const buttons = element.querySelectorAll('button');
            buttons.forEach(button => {
                if (button.parentNode) {
                    button.parentNode.removeChild(button);
                }
            });

            const svgs = element.querySelectorAll('svg');
            svgs.forEach(svg => {
                if (svg.parentNode) {
                    svg.parentNode.removeChild(svg);
                }
            });

            element.querySelectorAll('*').forEach(node => {
                node.removeAttribute('style');
            });

            const codeBlocks = element.querySelectorAll('code');
            codeBlocks.forEach(code => {
                code.className = ''; // Remove all classes
            });

            console.log('Cleaned HTML content:', problematicDiv.innerHTML);

            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = problematicDiv.innerHTML;

            document.body.appendChild(tempDiv);

            const range = document.createRange();
            range.selectNodeContents(tempDiv);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);

            document.execCommand('copy');
            document.body.removeChild(tempDiv);

            alert('The cleaned content has been copied to the clipboard. You can now paste it into your document.');

            taskCompleted = true; // Set the task as complete to prevent further alerts

        } catch (error) {
            console.error('Error during element removal:', error);
        }
    }

    // Set up a MutationObserver to handle dynamic changes in the DOM
    const observer = new MutationObserver(mutations => {
        if (taskCompleted) {
            return; // Exit if task is already completed
        }

        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    removeProblematicElements(node);
                }
            });
        });
    });

    // Observe changes to the body and subtree
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // Initial cleanup call
    removeProblematicElements(problematicDiv);

    // Disconnect the observer after cleanup to avoid unnecessary operations
    setTimeout(() => {
        observer.disconnect();
        console.log('MutationObserver disconnected.');
    }, 5000); // Adjust the timeout as needed
}

// Execute the cleanup function when the extension icon is clicked
cleanUpHtmlContent();
