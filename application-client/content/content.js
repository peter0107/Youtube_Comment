const observer = new MutationObserver(() => {
    const commentSection = document.querySelector('ytd-comments#comments:has(ytd-comment-view-model)');
    if (commentSection) {
        const {title, img} = findUrl();
        chrome.runtime.sendMessage({ action: "commentFound", img, title });
        observer.disconnect();
    }
});

const findUrl = () => {    
    try {
        const playerElement = document.querySelector('player-microformat-renderer');
        const scriptElement = playerElement.querySelector('script');
        const data = JSON.parse(scriptElement.textContent);

        const title = data.name;
        const img = data.thumbnailUrl[0];

        return { title, img };
    } catch (error) {
        return {title: null, img: null};
    }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message.action === "commentReq"){
        const commentSection = document.querySelector('ytd-comments#comments:has(ytd-comment-view-model)');
        if (commentSection){
            const {title, img} = findUrl();
            chrome.runtime.sendMessage({ action: "commentFound", img, title });
            sendResponse({ status: true });
        } else {
            observer.observe(document.body, { childList: true, subtree: true });
            sendResponse({ status: false });
        }
    }
    else if(message.action === "stopFindCommnet"){
        observer.disconnect();
    }
    else if(message.action === "summarizeReq"){
        const id = "jnEe-uGjACs"
        const commentSection = document.querySelector('ytd-comments#comments:has(ytd-comment-view-model)');
        const summarizeTab = chrome.runtime.getURL('content/summary/index.html') + `?id=${id}`;
        commentSection.innerHTML = `<iframe src="${summarizeTab}" width="100%" height="600px" scrolling="no"></iframe>`
    }
    return true;
});