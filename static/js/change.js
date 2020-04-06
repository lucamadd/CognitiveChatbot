var  API_ROOT='http://10.60.35.4:8080/backend';




$("#new_password").on("change paste keyup", function () {
	var text = $(this).val();
	if (text.length > 5) {
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
    var old_password = $('#old_password').val();
    var new_password = $('#new_password').val();
    var confirm_password = $('#confirm_password').val();


    const old_passwordHex = await digestMessage(old_password);
    const new_passwordHex = await digestMessage(new_password);
    const confirm_passwordHex = await digestMessage(confirm_password);
    $('#old_password').val("");
    $('#new_password').val("");
    $('#confirm_password').val("");
    data = {}
    $.ajax({
        type: 'POST',
        url: API_ROOT,
        data: {
            'old_password': old_passwordHex,
            'new_password': new_passwordHex,
            'confirm_password': confirm_passwordHex
        },
        error: function() {
            document.getElementById('error').innerHTML = "";
            document.getElementById('error').insertAdjacentHTML('afterbegin','<h3 style="color:red;" class="fs-subtitle">Errore di connessione</h3>')
        },
        success: function(data){
            console.log(data)
            if (data=='true'){
                document.getElementById('error').innerHTML = "";
                $('#login_div').remove();
                document.getElementById('error').insertAdjacentHTML('afterbegin','<h3 style="color:#27AE60;" class="fs-subtitle">Password modificata con successo.</h3>')
            } else {
                document.getElementById('error').innerHTML = "";
                document.getElementById('error').insertAdjacentHTML('afterbegin','<h3 style="color:red;" class="fs-subtitle">Controlla i dati e riprova</h3>')
            }
        }
    })
    console.log(data)
}