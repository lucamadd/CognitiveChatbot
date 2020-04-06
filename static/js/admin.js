var  API_ROOT='http://localhost:8080/backend';
$(document).ready(function () {

    var navListItems = $('div.setup-panel div a'),
        allWells = $('.setup-content'),
        allNextBtn = $('.nextBtn');

    allWells.hide();

    navListItems.click(function (e) {
        e.preventDefault();
        var $target = $($(this).attr('href')),
            $item = $(this);

        if (!$item.hasClass('disabled')) {
            navListItems.removeClass('btn-success').addClass('btn-default');
            $item.addClass('btn-success');
            allWells.hide();
            $target.show();
            $target.find('input:eq(0)').focus();
        }
    });

    allNextBtn.click(function () {
        var curStep = $(this).closest(".setup-content"),
            curStepBtn = curStep.attr("id"),
            nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
            curInputs = curStep.find("input[type='text'],input[type='url']"),
            isValid = true;

        $(".form-group").removeClass("has-error");
        for (var i = 0; i < curInputs.length; i++) {
            if (!curInputs[i].validity.valid) {
                isValid = false;
                $(curInputs[i]).closest(".form-group").addClass("has-error");
            }
        }

        if (isValid) nextStepWizard.removeAttr('disabled').trigger('click');
    });

    $('div.setup-panel div a.btn-success').trigger('click');

    var maxField = 10; //Input fields increment limitation
    var addButton = $('#addField'); //Add button selector
    var wrapper = $('.field_wrapper'); //Input field wrapper
    var x = 1; //Initial field counter is 1
    var fieldHTML = '<div class="row" style="margin-top:20px;"><div class="col-11"><input class="form-control" type="text" name="patterns[]" value=""/></div><div class="col-1"><a href="javascript:void(0);" id="removeField" class="btn btn-danger"><i class="fas fa-minus"></i></a></div></div>'; //New input field html 
    
    
    //Once add button is clicked
    $(addButton).click(function(){
        //Check maximum number of input fields
        if(x < maxField){ 
            x++; //Increment field counter
            $(wrapper).append(fieldHTML); //Add field html
        }
    });
    
    //Once remove button is clicked
    $(wrapper).on('click', '#removeField', function(e){
        e.preventDefault();
        $(this).parent('div').parent().remove(); //Remove field html
        x--; //Decrement field counter
    });

    var maxField2 = 10; //Input fields increment limitation
    var addButton2 = $('#addField2'); //Add button selector
    var wrapper2 = $('.field_wrapper2'); //Input field wrapper
    var x2 = 1; //Initial field counter is 1
    var fieldHTML2 = '<div class="row" style="margin-top:20px;"><div class="col-11"><input class="form-control" type="text" name="responses[]" value=""/></div><div class="col-1"><a href="javascript:void(0);" id="removeField2" class="btn btn-danger"><i class="fas fa-minus"></i></a></div></div>'; //New input field html 
    
    
    //Once add button is clicked
    $(addButton2).click(function(){
        //Check maximum number of input fields
        if(x2 < maxField2){ 
            x2++; //Increment field counter
            $(wrapper2).append(fieldHTML2); //Add field html
        }
    });
    
    //Once remove button is clicked
    $(wrapper2).on('click', '#removeField2', function(e){
        e.preventDefault();
        $(this).parent('div').parent().remove(); //Remove field html
        x2--; //Decrement field counter
    });
});
$("form").submit(function(e){
    e.preventDefault();
});

function addAction(){
    var data = {}
    var tag;
    var context_set;
    var context_filter;
    var patterns = [];
    var responses = [];
    tag = $('#tag').val();
    context_set = $('#context_set').val();
    context_filter = $('#context_filter').val();
    $("input[name='patterns[]']").each(function() {
        patterns.push($(this).val());
    });
    $("input[name='responses[]']").each(function() {
        responses.push($(this).val());
    });

    if (tag != "") {
        data.tag = tag;
    }
    if (patterns.length > 0) {
        data.patterns = JSON.stringify(patterns);
    }
    if (responses.length > 0) {
        data.responses = JSON.stringify(responses);
    }
    data.contextSet = context_set;
    if (context_filter != "") {
        data.contextFilter = context_filter;
    }
    console.log(data)
    if (tag == "" || patterns[0] == "" || responses[0] == ""){
        alert('Uno o più campi sono mancanti!')
    } else {
        if (context_filter != ""){            
            $('#addButton').attr("disabled",true).html('Training del modello...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
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
                    setTimeout(function(){ $('#addButton').attr("disabled",true).html('Salvataggio...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');}, 10000);
                    setInterval(function() {
                        $('#addButton').attr("disabled",true).html('Riavvio del server...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                        $.ajax({ 
                            url  : API_ROOT,
                            type : "POST"
                        })
                        .done(function() {
                            $('#addButton').attr("disabled",true).html('Completato  <span class="fas fa-check"></span>');
                            window.location.replace('index.html')
                        });
                    }, 7000);
                }
            })
        } else {
            $('#addButton').attr("disabled",true).html('Training del modello...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
            $.ajax({
                type: 'POST',
                url: API_ROOT,
                data: {
                    'tag': data.tag,
                    'patterns': data.patterns,
                    'responses': data.responses,
                    'context_set': data.contextSet
                },
                error: function(){
                    setTimeout(function(){ $('#addButton').attr("disabled",true).html('Salvataggio...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');}, 10000);
                    setInterval(function() {
                        $('#addButton').attr("disabled",true).html('Riavvio del server...  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>');
                        $.ajax({ 
                            url  : API_ROOT,
                            type : "POST"
                        })
                        .done(function() {
                            $('#addButton').attr("disabled",true).html('Completato  <span class="fas fa-check"></span>');
                            window.location.replace('index.html')
                        });
                    }, 7000);
                }
            })
        }
    }
    
}