// initializes the contextmenu on installation.
chrome.runtime.onInstalled.addListener(function() {
    chrome.contextMenus.create({
        "title": "NoClick: Get a gist",
        "id": 'noClick',
        "contexts": ["link"],
    });
});

// the listener function, run when someone right clicks the extension's menu in contextmenu.
function contextClicked(info, tab) {
    if (info.menuItemId === "noClick") {
        if (!info.linkUrl) return;

        url = 'http://noclick-api.jrtzicmdwr.us-east-2.elasticbeanstalk.com/summarize';
        url += "?url=" + info.linkUrl + "&num=3";

        chrome.tabs.executeScript(tab.id, {
            file: "script.js"
        }, function() {})
    }
}

// Used to render stuff onto the pop up page.
function renderStatus(statusText) {
    document.getElementById('status').textContent = statusText;
}

// calls the listener.
chrome.contextMenus.onClicked.addListener(contextClicked);