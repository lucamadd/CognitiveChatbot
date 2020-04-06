var  API_ROOT='http://localhost:8080/backend';
var currentAvatar="images/user.png";

function chat(box){
    $( "#chatMessages" ).append(box);
    $( "#chatMessages" ).append('<div class="chatPlaceholder"></div>');
    $('html, body').animate({scrollTop:$(document).height()}, 'slow');
    
}
function boxBot(text,attachment){
    var box='<div class="chat_text">'+
    '    <img src="images/bot.png" alt="Avatar" style="width:100%;">'+
    '    <p class="custom_text">' + text;
    if (attachment!=undefined){
        box= box + '<br/>'+ attachment;
    }
    box= box + '</p>'+
    '    <span class="time-right">' + currentTime() +  '</span>'+
    '</div>';
    return box;
}
function boxUser(text){
    return '<div class="chat_text darker">' +
    '       <img src="' + currentAvatar + '" alt="Avatar" class="right" style="width:100%;">'+
    '        <p class="custom_text">' + text + '</p>'+
    '       <span class="time-left">' + currentTime() + '</span>'+
    '   </div>';
}

function currentTime(){
    var today = new Date();
    var minutes = today.getMinutes() < 10 ? '0' + today.getMinutes() : today.getMinutes();
    var seconds = today.getSeconds() < 10 ? '0' + today.getSeconds() : today.getSeconds();
    var time = today.getHours() + ":" + minutes + ":" + seconds;
    return time;
}
function initChat(){
    callBot('Ciao!');
}

function userAsk(){
    var userMsg=$('#userMsg').val();
    $('#userMsg').val("");
    chat(boxUser(userMsg));
    callBot(userMsg);
}

function callBot(msg){
    $.ajax({
        type: 'POST',
        url: API_ROOT,
        data: { 
            'msg': msg, 
        },
        success: function(data){
            var jsonData=JSON.parse(data);
            if ($("#avatar-avatar-canvas").is(':visible')){
                web.message(jsonData.message, "", "", "");
            }else{
                $('#audio').html('<iframe style="visibility:hidden" src="data:audio/mp3;base64,' +
                jsonData.responseSpeech + '" allow="autoplay">');
            }
            chat(boxBot(jsonData.message,jsonData.attachment));
        }
    });
}



function addAction(){
    var activeTab;
    if ($('#tag_simple').val() != '')
        activeTab = 'Azione semplice';
    /*
    if ($('#tag_complex').val() != '')
        activeTab = 'Azione complessa';
    */
    if ($('#tag_post').val() != '')
        activeTab = 'Richiesta POST'
    console.log(activeTab)

    if (activeTab == 'Azione semplice') {
        var data = {}
        data.tag = $('#tag_simple').val();
        $('#tag_simple').val("");
        data.patterns = $('#patterns_simple').val();
        $('#patterns_simple').val("");
        data.responses = $('#responses_simple').val();
        $('#responses_simple').val("");
        data.contextSet = $('#context-set_simple').val();
        $('#context-set_simple').val("");
        if ($('#context-filter_simple').val() != "") {
            data.contextFilter = $('#context-filter_simple').val();
            $('#context-filter_simple').val("");
        }
        sendAction(data);
    }
    else if (activeTab == 'Azione complessa') {
        var data = {}

    } 
    else if (activeTab == 'Richiesta POST') {
        var data = {}
        if ($('#tag_post').val() != "") {
            data.tag = $('#tag_post').val();
            $('#tag_post').val("");
        }
        if ($('#patterns_post').val() != "") {
            data.patterns = $('#patterns_post').val();
            $('#patterns_psot').val("");
        }
        if ($('#responses_post').val() != "") {
            data.responses = $('#responses_post').val();
            $('#responses_post').val("");
        }
        if ($('#context-set_post').val() != "") {
            data.contextSet = $('#context-set_post').val();
            $('#context-set_post').val("");
        }
        if ($('#context-filter_post').val() != "") {
            data.contextFilter = $('#context-filter_post').val();
            $('#context-filter_post').val("");
        }
        if ($('#url_post').val() != "") {
            data.url = $('#url_post').val();
            $('#url_post').val("");
        }
        if ($('#params_post').val() != "") {
            data.params = JSON.stringify($('#params_post').val());
            $('#params_post').val("");
            console.log(JSON.stringify($('#params_post').val()))
        }
        console.log(data.params)
        //sendAction(data);
    }
}


function sendAction(data){
    $('#addAction').attr("disabled",true).html('Training del modello...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
    $.ajax({
        type: 'POST',
        url: API_ROOT,
        data: {
            'tag': data.tag,
            'patterns': data.patterns,
            'responses': data.responses,
            'context_set': data.contextSet,
            'context_filter': data.contextFilter
        },
        error: function(){
            $('#addAction').attr("disabled",true).html('Salvataggio...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            setInterval(function() {
                $('#addAction').attr("disabled",true).html('Riavvio del server...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                $.ajax({ 
                    url  : API_ROOT,
                    type : "POST"
                })
                .done(function() {
                    $('#addAction').attr("disabled",true).html('Completato  <span class="fas fa-check"></span>');
                    location.reload();
                });
            }, 7000);
        }
    })
}



$("#userForm").submit(function(e){
    e.preventDefault();
    userAsk();
});