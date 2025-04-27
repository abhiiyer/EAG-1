
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "PAGE_VISIT") {
    fetch("http://localhost:5000/upload_url_text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: msg.url, html: msg.html })
    }).then(res => res.text()).then(console.log).catch(console.error);
  }
});
