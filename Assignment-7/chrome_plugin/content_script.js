
const html = document.documentElement.outerHTML;
chrome.runtime.sendMessage({ type: "PAGE_VISIT", html: html, url: window.location.href });
