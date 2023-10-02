document.getElementById("readData").addEventListener("click", function() {
    browser.tabs.executeScript({
        code: 'document.body.innerText'
    }).then((results) => {
        // results[0] contains the output of the executed script
        document.getElementById("output").textContent = results[0];
    });
});
