const sendToContent = (action, sendResponse, tryDepth=1) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs.length > 0) {
            chrome.tabs.sendMessage(tabs[0].id, { action: action }, (res) => {
                if(res){
                    sendResponse({status: true});
                }else{
                    // On Fail(content issue): request again
                    if(tryDepth < 10){
                        console.log("On Fail(content issue): request again");
                        setTimeout(() => sendToContent(action, sendResponse, tryDepth + 1), 500);
                    }else{
                        // On Fail(content issue x5): reponse false
                        sendResponse({status: false, error: "content request depth exceed"});
                    }
                }                
            });
        }else{
            // On Fail(background issue): response false
            console.log("On Fail(background issue): response false");
            sendResponse({status: false});
        }
    });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.action === "commentReq"){
        sendToContent("commentReq", sendResponse);
    }
    else if (message.action === "stopFindComment") {
        sendToContent("stopFindComment", sendResponse);
    }
    else if (message.action === "summarizeReq"){
        sendToContent("summarizeReq", sendResponse);
    }
    
    else if (message.action === "commentFound") {
        chrome.runtime.sendMessage(message);
    }
    return true;
});