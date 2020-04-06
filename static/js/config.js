var  API_ROOT='http://localhost:8080/backend';

$(document).ready(function () {
    $.ajax({
        type: 'POST',
        url: API_ROOT,
        data: { 
            'config': true, 
        },
        success: function(data){
            var res = data.split("\n")
            for(i=1;i<res.length;i++){
                $('#backup_list').append('<button type="button" id=file"'+i+'" class="list-group-item list-group-item-action" data-toggle="modal" data-target="#exampleModal" data-whatever="'+res[i]+'">'+res[i]+'</button>');
            }
        },
        error: function(){
            alert("Errore di connessione.");
        }
    });
});

var date = "";
$('#exampleModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('whatever') // Extract info from data-* attributes
    date = recipient
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-body p').val(recipient)
  })

$("#confirmbutton").click(
    function(){
        console.log(date)
        $('#confirmbutton').attr("disabled",true).html('Salvataggio...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
        $.ajax({
            type: 'POST',
            url: API_ROOT,
            data: { 
                'config': false, 
                'date': date
            },
            error: function(){
                setTimeout(function(){ $('#confirmbutton').attr("disabled",true).html('Training del modello...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');}, 10000);
                setInterval(function() {
                    $('#confirmbutton').attr("disabled",true).html('Riavvio del server...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                    $.ajax({ 
                        url  : API_ROOT,
                        type : "POST"
                    })
                    .done(function() {
                        $('#confirmbutton').attr("disabled",true).html('Completato  <span class="fas fa-check"></span>');
                        window.location.replace('index.html')
                    });
                }, 7000);
            }
        })
    }
)