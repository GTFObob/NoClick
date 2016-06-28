chrome.runtime.onInstalled.addListener(function() {
	chrome.contextMenus.create({
	    "title": "Buzz This",
	    "id": 'noClick',
	    "contexts": ["all"],
	  });
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
    if (info.menuItemId === "noClick") { // here's where you'll need the ID
        
    	var code = 'alert("' + info.selectionText + '")';
    	chrome.tabs.executeScript({code: code});
    }
});


function renderStatus(statusText) {
  document.getElementById('status').textContent = statusText;
}
