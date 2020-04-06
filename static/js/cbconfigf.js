var  API_ROOT='http://localhost:8080/backend';

$(document).ready( function(){
    if (typeof(Storage) !== "undefined" && sessionStorage.logged == true) {
        showPage();
    } 
})

$("#password").on("change paste keyup", function () {
	var text = $(this).val();
	if (text.length > 0) {
		document.getElementById("loginButton").disabled = false;
	}
	else {
		document.getElementById("loginButton").disabled = true;
	}
});

async function digestMessage(message){
    digest = CryptoJS.SHA256(message).toString(CryptoJS.enc.Hex);
    return digest;
}

async function addAction(){
    var password = $('#password').val();
    $('#password').val("");
    const digestHex = await digestMessage(password);
    data = {}
    $.ajax({
        type: 'POST',
        url: API_ROOT,
        data: {
            'password': digestHex
        },
        error: function() {
            document.getElementById('error').innerHTML = "";
            document.getElementById('error').insertAdjacentHTML('afterbegin','<h3 style="color:red;" class="fs-subtitle">Errore di connessione</h3>')
        },
        success: function(data){
            if (data=='true'){
                if (typeof(Storage) !== "undefined") {
                    sessionStorage.logged = true;
                } else {
                    alert('Sorry! This browser does not support sessionStorage. Please switch to another browser to access this page.');
                    //document.referrer;
                }
                document.getElementById('error').innerHTML = "";
                showPage();
            } else {
                document.getElementById('error').innerHTML = "";
                document.getElementById('error').insertAdjacentHTML('afterbegin','<h3 style="color:red;" class="fs-subtitle">Password errata</h3>')
            }
        }
    })
    console.log(data)
    
    
}

function showPage(){
    $('#login_div').remove();
    document.getElementById('configuration').insertAdjacentHTML('afterbegin','<div class="row" style="text-align: center;">\
    <a style="margin-left: 40%;" href="simple_request.html"><input type="button" id="button1" name="next" class="next action-button" value="Richiesta semplice"/></a>\
    </div><div class="row" style="text-align: center;"><a style="margin-left: 40%;" href="post_request.html"><input type="button" id="button2" name="next" class="next action-button" value="Richiesta POST"/></a></div>\
    <div class="row">\
    <br>\
    <div class="col">\
    </div>\
    </div><a href="change_password.html" style="color: grey;">Cambia password</a>')
}