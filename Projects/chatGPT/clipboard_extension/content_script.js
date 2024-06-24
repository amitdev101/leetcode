function cleanUpHtmlContent() {
    // Select the element that contains the problematic content
    const problematicDiv = document.querySelector('.dark');
  
    if (!problematicDiv) {
      console.error('The specified element was not found on the page.');
      return;
    }
  
    // Function to remove problematic tags and clean the content
    function removeProblematicElements(element) {
      // Remove nested <span> elements with specific conditions
      const spans = element.querySelectorAll('span');
      spans.forEach(span => {
        if (span.textContent.trim().toLowerCase() === 'java') {
          span.remove();
        }
      });
  
      // Remove all button and svg elements
      const buttons = element.querySelectorAll('button');
      buttons.forEach(button => button.remove());
      
      const svgs = element.querySelectorAll('svg');
      svgs.forEach(svg => svg.remove());
  
      // Remove inline styles
      element.querySelectorAll('*').forEach(node => node.removeAttribute('style'));
  
      // Simplify <code> blocks by removing complex formatting classes
      const codeBlocks = element.querySelectorAll('code');
      codeBlocks.forEach(code => {
        code.className = ''; // Remove all classes
      });
    }
  
    // Clean up the problematic content
    removeProblematicElements(problematicDiv);
  
    // Log the cleaned HTML content for verification
    console.log('Cleaned HTML content:', problematicDiv.innerHTML);
  
    // Create a temporary element to copy the cleaned content
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = problematicDiv.innerHTML;
  
    // Append the temporary element to the body
    document.body.appendChild(tempDiv);
  
    // Select the content of the temporary element
    const range = document.createRange();
    range.selectNodeContents(tempDiv);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
  
    // Copy the selected content to the clipboard
    document.execCommand('copy');
  
    // Remove the temporary element from the body
    document.body.removeChild(tempDiv);
  
    // Provide feedback to the user
    alert('The cleaned content has been copied to the clipboard. You can now paste it into your document.');
  }
  
  // Execute the cleanup function
  cleanUpHtmlContent();
  