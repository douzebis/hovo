document.getElementById('exportButton').addEventListener('click', function () {
  // Trigger the background script to export cookies
  browser.runtime.sendMessage({ action: 'exportCookies' });
});

// Receive the exported cookies and display them
browser.runtime.onMessage.addListener(function (message) {
  if (message.action === 'displayCookies') {
    document.getElementById('cookiesDisplay').textContent = message.cookies;
  }
});
