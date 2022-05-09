import { createHTMLElement,setRandInterval } from './utilities';
import "./assets/sass/input.scss";
import img_monitor_frame from './assets/img/monitor_frame.png';
import img_monitor_engraving from './assets/img/monitor_engraving.png';
import img_transition from './assets/img/transition_animation.gif';
import img_WNFA_heart from './assets/img/heart.gif';
import img_WNFA_logo from './assets/img/logo_grey.png';



function submitPhotoTicket(endpointURL, submitAPIURL, base64) {
    return fetch(endpointURL + submitAPIURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'data': base64,
        })
    });
}

function takePhotoToBase64(video, canvas) {
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg').split(';base64,')[1];
}



function run() {
    const video = document.querySelector("#video");
    const canvas = document.querySelector("#canvas");
    const terminal_layer = document.querySelector("#terminal-layer");
    const transition_gif = document.querySelector("#transition-gif");

    const endpointURL = window.location.hash.split('#')[1];
    const submitAPIURL = "api/submit/ticket";
    const date = new Date();
    let enterKeyFunc;
    let animationProcessing = true;
    let processing = true;
    

    const waitingTextList = [
        {type: "text", text: "---------------", lang: 'en', delay: 0},
        {type: "img", img: img_WNFA_logo, class: 'logo', delay: 0},
        {type: "text", text: "System: WNFA-OS 0.1.2", lang: 'en', delay: 0},
        {type: "text", text: "Date: " + date.toDateString(), lang: 'en', delay: 0},
        {type: "text", text: "---------------", lang: 'en', delay: 0},

        {type: "text", text: "closing camera stream...", lang: 'en', delay: 500},
        {type: "text", text: "core systems online...", lang: 'en', delay: 500},
        {type: "text", text: "thanks for using WNFA...", lang: 'en', delay: 500},
        {type: "text", text: "start text processing sequence...", lang: 'en', delay: 500},
        {type: "break", delay: 500},
        {type: "text", text: "荷叶滴落泪水<br>来不及 浸透书页<br>一百年 一千年<br>点燃一片通电的网", lang: 'cn', delay: 500},
        {type: "break", delay: 500},
        {type: "text", text: "回想 回想<br>那心的铁片<br>也要发出轰响", lang: 'cn', delay: 500},
        {type: "break", delay: 500},
        {type: "text", text: "please wait...", lang: 'en', delay: 500},
    ]

    document.addEventListener('keydown', (e) => {
        if (!animationProcessing && !processing && e.key === "Enter") {
            console.log("yes");
            enterKeyFunc();
        }
    });

    enterKeyFunc =() => {
        animationProcessing = true;
        processing = true;
        transition_gif.classList.add('show');

        setTimeout(()=>{
            const pointer = createHTMLElement('p', '$: _');
            terminal_layer.appendChild(pointer);
            transition_gif.classList.remove('show');
            
            video.pause();
            terminal_layer.classList.add('show');
            video.classList.add('hide');
    
            let listIndex = 0;
            let printTimeout;
            const nextPrint = () => {
                if (listIndex >= waitingTextList.length) {
                        processing = false;
                } else {
                    printTimeout = setTimeout(() => {       
                        const obj = waitingTextList[listIndex];
                        switch(obj.type) {
                            case 'text':
                                terminal_layer.insertBefore(createHTMLElement('p', obj.text, {'class': obj.lang}), pointer);
                                pointer.scrollIntoView(true);
                                break;
                            case 'img':
                                terminal_layer.insertBefore(createHTMLElement('img', '', {'src': obj.img, 'class': obj.class}), pointer);
                                pointer.scrollIntoView(true);
                                break;
                            case 'break':
                                terminal_layer.insertBefore(createHTMLElement('p', '<br>'), pointer);
                                pointer.scrollIntoView(true);
                                break;
                        }
                        listIndex++;
                        nextPrint();       
                    }, waitingTextList[listIndex].delay);
                }
            }
            nextPrint();

            // take photo and submite
            submitPhotoTicket(endpointURL,submitAPIURL, takePhotoToBase64(video, canvas))
            .then(() => {
                processing = false;
                video.play();
                terminal_layer.classList.remove('show');
            })
            .catch((e) => {
                console.log(e);
                processing = false;

            })


        },500);


        


        
    }

    // navigator.mediaDevices.getUserMedia({video: true, audio: false})
    // .then((stream) => {
    //     video.srcObject = stream;
    //     video.play();
    //     processing = false;
    // });
    processing = false;


}


function main() {
    const top_layer = createHTMLElement('div', '', {'id': 'top-layer'});
    const second_layer = createHTMLElement('div', '', {'id': 'second-layer'});

    const top_layer_monitor_frame = createHTMLElement('img', '', {'id': 'monitor-frame', 'src': img_monitor_frame});
    const top_layer_monitor_engraving = createHTMLElement('img', '', {'id': 'monitor-engraving', 'src': img_monitor_engraving});
    
    const second_layer_transition = createHTMLElement('img', '', {'id': 'transition-gif', 'src': img_transition});
    const second_layer_WNFA_heart = createHTMLElement('img', '', {'id': 'WNFA-heart', 'src': img_WNFA_heart});
    const second_layer_terminal= createHTMLElement('div', '', {'id': 'terminal-layer'});
    const second_layer_vide = createHTMLElement('video', '', {'id': 'video'});
    const second_layer_canvas = createHTMLElement('canvas', '', {'id': 'canvas', 'width': '1920', 'height': '1080'});

    top_layer.appendChild(top_layer_monitor_frame);
    top_layer.appendChild(top_layer_monitor_engraving);

    second_layer.appendChild(second_layer_transition);
    second_layer.appendChild(second_layer_WNFA_heart);
    second_layer.appendChild(second_layer_terminal);
    second_layer.appendChild(second_layer_vide);
    second_layer.appendChild(second_layer_canvas);

    window.addEventListener('load', () => {
        document.body.appendChild(top_layer);
        document.body.appendChild(second_layer);
        run();
    });
}


main();