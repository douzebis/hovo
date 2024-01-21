function exportCookies() {
  browser.cookies.getAll({ domain: ".google.com" }, function (cookies) {
    // Handle the cookies as needed
    console.log(cookies);

    // You can export the cookies in your desired format (e.g., JSON)
    var exportedCookies = JSON.stringify(cookies);

    // Send the exported cookies to the popup.js for display
    browser.runtime.sendMessage({ action: 'displayCookies', cookies: exportedCookies });
  });
}

// Add a listener for the extension button click
browser.browserAction.onClicked.addListener(exportCookies);
