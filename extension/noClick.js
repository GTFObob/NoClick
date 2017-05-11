// initializes the contextmenu on installation.
chrome.runtime.onInstalled.addListener(function() {
	chrome.contextMenus.create({
	    "title": "NoClick",
	    "id": 'noClick',
	    "contexts": ["link"],
	  });
});

// the listener function, run when someone right clicks the extension's menu in contextmenu.
function contextClicked(info, tab) {
    if (info.menuItemId === "noClick") {
    	articleTopic();
    }
}

// Used to render stuff onto the pop up page.
function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}

// calls the listener.
chrome.contextMenus.onClicked.addListener(contextClicked);
