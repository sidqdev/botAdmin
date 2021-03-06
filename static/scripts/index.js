let base_link = location.protocol + '//' + location.host;

let current_chat_id = -1;

let current_chat_list = 'all-chats';

function set_current_style(data){
    data.forEach((element) => {
        var chat_id = element['chat_id'];
        var elem = document.getElementById('chat-' + String(chat_id));
        if(elem){
            if(chat_id == current_chat_id){
                elem.style['background-color'] = '#e8f6f8';
            }else{
                elem.style['background-color'] = 'white';
            }
        }
    })
}

function insertParam(key, value) {
    key = encodeURIComponent(key);
    value = encodeURIComponent(value);

    if (history.pushState) {
        var newurl = window.location.protocol + "//" + window.location.host 
        + window.location.pathname + '?' + key + '=' + value;
        window.history.pushState({path:newurl},'',newurl);
    }
    
}

document.getElementById('all-chats').classList.add('pressed');

var chat_list = new Vue({
    el: '#chats',
    data: {
        chats: [],
        openedChatCount: 0
    },
    methods: {
        setChats: function(chatType){

            document.getElementById(chatType).classList.add('pressed');

            current_chat_list = chatType;
            if (chatType == 'all-chats'){
                document.getElementById("opened-chats").classList.remove('pressed');
                document.getElementById("closed-chats").classList.remove('pressed');
                axios.get(base_link + '/getChats').then(res => {
                    let chats = [];
                    let opened = 0;
                    res.data.forEach((element) => {
                        element['item_id'] = 'chat-' + String(element['chat_id']);
                        element['last_message']['content'] = element['last_message']['content'].slice(0, 60);
                        chats.push(element);
                        if (element['status'] == 'opened') opened++;

                    })
                    this.chats = chats;
                    this.openedChatCount = opened;
                    set_current_style(res.data);
                });
            }else if(chatType == 'opened-chats'){
                document.getElementById("all-chats").classList.remove('pressed');
                document.getElementById("closed-chats").classList.remove('pressed');
                axios.get(base_link + '/getChats').then(res => {
                    let chats = [];
                    res.data.forEach((element) => {
                      if(element.status == 'opened'){
                        element['item_id'] = 'chat-' + String(element['chat_id']);
                        element['last_message']['content'] = element['last_message']['content'].slice(0, 60);
                        chats.push(element);
                      }
                    })
                    this.chats = chats;
                    this.openedChatCount = this.chats.length;
                    set_current_style(res.data);
                });
            }else{
                document.getElementById("opened-chats").classList.remove('pressed');
                document.getElementById("all-chats").classList.remove('pressed');
                axios.get(base_link + '/getChats').then(res => {
                    let chats = [];
                    let opened = 0;
                    res.data.forEach((element) => {
                      if (element['status'] == 'opened') opened++;
                      if(element.status == 'closed'){
                        element['item_id'] = 'chat-' + String(element['chat_id']);
                        element['last_message']['content'] = element['last_message']['content'].slice(0, 60);
                        chats.push(element);
                      }
                    })
                    this.chats = chats;
                    this.openedChatCount = opened;
                    set_current_style(res.data);
                });
            }
        },
        chooseChat: function(chat_id){
            console.log('chat-' + String(chat_id));
            userInfo.setUser(chat_id)
            new_chat = document.getElementById('chat-' + String(chat_id));
            old_chat = document.getElementById('chat-' + String(current_chat_id));
            if(old_chat){
                old_chat.style['background-color'] = 'white';
            }
            if(new_chat){
                new_chat.style['background-color'] = '#e8f6f8';
            }
            current_chat_id = chat_id;
            chat.updateChat(chat_id);
            insertParam('current_chat_id', current_chat_id);
            document.getElementById('chat-items').scrollTop = document.getElementById('chat-items').scrollHeight;
        }
    }
})

var chat = new Vue({
    el: '#chat',
    data: {
        chat: [],
        file: '????'
    },
    methods: {
        updateChat: function(chat_id){
            if (chat_id != -1){
                axios.get(base_link + '/getChat', {params: {'chat_id': chat_id}}).then(res =>{
                    let chat = res.data;
                    chat.forEach((message) => {
                        if(message.message_type == 'time_splitter'){
                            message.user = 'common';
                        }else{
                            message.user = message.user_id == 0 ? 'me' : 'user';
                            this.statusLabel = message.status == 'opened' ? '?????????????? ??????' : '?????????????? ??????';
                            this.status = message.status == 'opened' ? 'closed': 'opened';
                            if (!['text', 'action'].includes(message.message_type)){
                                message.content = base_link + '/static/' + message.content;
                            }
                        }
                    })

                    let temp_chat = this.chat;
                    this.chat = chat;

                    setTimeout(function(){
                        if(temp_chat.length != chat.length){
                            document.getElementById('chat-items').scrollTop = document.getElementById('chat-items').scrollHeight + 100;
                        }
                    }, 30)
                })
            }   
        },
        sendMessage: function(){
            this.file = '????';
            elem = document.getElementById('input-message');
            file = document.getElementById('input-file');
            text = elem.value;
            elem.value = '';
            console.log(text);
            let formData = new FormData();
            formData.append('chat_id', current_chat_id);
            formData.append('user_id', 0);

            if (file.files.length){
                console.log(file.files[0]);
                message_type = file.files[0].type.split('/')[0];
                if(!['audio', 'video', 'image'].includes(message_type)){
                    message_type = 'document';
                }
                console.log(message_type);
                formData.append('file', file.files[0]);
                formData.append('message_type', message_type);

            }else{
                formData.append('content', text);
                formData.append('message_type', 'text');
            }
            
            file.value = null;
            axios.post(base_link + '/sendMessage',
             formData).then(res =>{
                 console.log(res.data);
             })
            
             document.getElementById('chat-items').scrollTop = document.getElementById('chat-items').scrollHeight + 1000;
        },
        overload: function(e, link){
            bp = new BigPicture({
                el: e.target,
                imgSrc: link
            })
            bp.prev()
        },
        uploadFile: function(){
            file = document.getElementById('input-file');
            if (file.files.length){
                file = file.files[0];
                console.log(file);
                this.file = '????' + file.name;
            }
            else this.file = '????';
        }
        // changeStatus: function(status){
        //     let formData = new FormData();
        //     formData.append('chat_id', current_chat_id);
        //     formData.append('status', status);
        //     axios.post(base_link + '/setChatStatus', formData);
        // }
    }
})

let userInfo = new Vue({
    el: '#user-info',
    data: {
        name: '?????? ????????????????????????', 
        photo: base_link + '/static/images/default.png',
        link: 'none',
        comment: '?????????????????????? ?? ????????????????????????',
        statusLabel: '?????????????? ??????',
        status: 'opened',
        harvesteds: []
    },
    methods:{
        setUser: function(user_id){
            axios.get(base_link + '/getUserInfo', {params: {user_id: user_id}}).then(res => {
                this.name = res.data.name;
                this.photo = base_link + '/static/images/'+res.data.photo;
                this.statusLabel = res.data.status == 'opened' ? '?????????????? ??????' : '?????????????? ??????';
                this.status = res.data.status == 'opened' ? 'closed': 'opened';
                if(res.data.user_name != 'none'){
                    this.link = 'https://t.me/' + res.data.user_name;
                }
                console.log(res.data.comment);
                this.comment = res.data.comment;
            })
        },
        saveText: function(){
            let comment = document.getElementById('user-comment').value;
            let user_id = current_chat_id;
            let formData = new FormData();

            formData.append('comment', comment);
            formData.append('user_id', user_id);
            
            axios.post(base_link + '/updateUserComment', formData)
        },
        changeStatus: function(){

            let formData = new FormData();
            formData.append('chat_id', current_chat_id);
            formData.append('status', this.status);
            this.status = this.status == 'opened' ? 'closed': 'opened';
            this.statusLabel = this.status == 'opened' ? '?????????????? ??????': '?????????????? ??????';
            axios.post(base_link + '/setChatStatus', formData);
        },
        setHarvested: function(){
            axios.get(base_link + '/getHarvestedMessages').then(res => {
                this.harvesteds = res.data;
            })
        },
        sendHarvested: function(){
            harvested_id = document.getElementById('selectHarvested').value;
            console.log(harvested_id);
            let formData = new FormData();
            formData.append('chat_id', current_chat_id);
            formData.append('harvested_id', harvested_id);
            formData.append('user_id', 0);
            
            axios.post(base_link + '/sendHarvestedMessages', formData)
        }
    }
})


const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());


if (params.current_chat_id){
    current_chat_id = params.current_chat_id;
    userInfo.setUser(current_chat_id);
}

setTimeout(function(){
    document.getElementById('chat-items').scrollTop = document.getElementById('chat-items').scrollHeight}, 1000);

function update(){
    chat_list.setChats(current_chat_list);
    chat.updateChat(current_chat_id);
    userInfo.setHarvested();
}

setInterval(update, 750);