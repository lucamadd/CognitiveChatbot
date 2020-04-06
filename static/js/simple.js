var  API_ROOT='http://localhost:8080/backend';

var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	next_fs = $(this).parent().next();
	
	//activate next step on progressbar using the index of next_fs
	$("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
	
	//show the next fieldset
	next_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".previous").click(function(){
	if(animating) return false;
	animating = true;
	
	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();
	
	//de-activate current step on progressbar
	$("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");
	
	//show the previous fieldset
	previous_fs.show(); 
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		}, 
		duration: 800, 
		complete: function(){
			current_fs.hide();
			animating = false;
		}, 
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(".submit").click(function(){
	return false;
})

$("#tag").on("change paste keyup", function () {
	var text = $(this).val();
	if (text.length > 0) {
		document.getElementById("button1").disabled = false;
	}
	else {
		document.getElementById("button1").disabled = true;
	}
});
$("#pattern").on("change paste keyup", function () {
	var text = $(this).val();
	if (text.length > 0) {
		document.getElementById("button2").disabled = false;
	}
	else {
		document.getElementById("button2").disabled = true;
	}
});
$("#response").on("change paste keyup", function () {
	var text = $(this).val();
	if (text.length > 0) {
		document.getElementById("button3").disabled = false;
	}
	else {
		document.getElementById("button3").disabled = true;
	}
});
$("#context_set").on("change paste keyup", function () {
	var text = $(this).val();
	if (text.indexOf(' ') >= 0) {
		document.getElementById("button4").disabled = true;
	}
	else {
		document.getElementById("button4").disabled = false;
	}
});

var maxField = 10; //Input fields increment limitation
var addButton = $('#addField'); //Add button selector
var wrapper = $('.field_wrapper'); //Input field wrapper
var x = 1; //Initial field counter is 1
var fieldHTML = '<div><input class="multiple-input" type="text" name="patterns[]" value=""/><input type="button" class="remove-button" id = "removeField" value="Rimuovi" ></input></div>'; //New input field html 


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
	$(this).parent('div').remove(); //Remove field html
	x--; //Decrement field counter
});		

var maxField2 = 10; //Input fields increment limitation
var addButton2 = $('#addField2'); //Add button selector
var wrapper2 = $('.field_wrapper2'); //Input field wrapper
var x2 = 1; //Initial field counter is 1
var fieldHTML2 = '<div><input class="multiple-input" type="text" name="responses[]" value=""/><input type="button" class="remove-button" id = "removeField2" value="Rimuovi" ></input></div>'; //New input field html 


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
	$(this).parent('div').remove(); //Remove field html
	x2--; //Decrement field counter
});	

var maxField3 = 10; //Input fields increment limitation
var addButton3 = $('#addMulti'); //Add button selector
var wrapper3 = $('.field_wrapper3'); //Input field wrapper
var x3 = 0; //Initial field counter is 0
var fieldHTML3 = '<div><input class="multiple-input" type="text" name="multi[]" value=""/><input type="button" class="remove-button" id = "removeField3" value="Rimuovi" ></input></div>'; //New input field html 


//Once add button is clicked
$(addButton3).click(function(){
	//Check maximum number of input fields
	if(x3 < maxField3){ 
		x3++; //Increment field counter
		$(wrapper3).append(fieldHTML3); //Add field html
	}
});

//Once remove button is clicked
$(wrapper3).on('click', '#removeField3', function(e){
	e.preventDefault();
	$(this).parent('div').remove(); //Remove field html
	x3--; //Decrement field counter
});	

function addAction(){
    var data = {}
    var tag;
    var context_set;
    var context_filter;
    var patterns = [];
    var responses = [];
    var multi = [];
    var multiStr = '';
    tag = $('#tag').val();
    context_set = $('#context_set').val();
    context_filter = $('#context_filter').val();
    $("input[name='patterns[]']").each(function() {
        patterns.push($(this).val());
    });
    $("input[name='responses[]']").each(function() {
        responses.push($(this).val());
    });
    $("input[name='multi[]']").each(function() {
        multi.push($(this).val());
    });

    if (tag != "") {
        data.tag = tag;
    }
    if (patterns.length > 0) {
        for (i=0;i<patterns.length;i++){
            if (patterns[i] === ""){
                delete patterns[i];
            }
        }
        patterns = patterns.filter(Boolean);
        data.patterns = JSON.stringify(patterns);
    }
    if (responses.length > 0) {
        for (i=0;i<responses.length;i++){
            if (responses[i] === ""){
                delete responses[i];
            }
        }
        responses = responses.filter(Boolean);
        data.responses = JSON.stringify(responses);
    }
    if (multi.length > 0) {
        for (i=0;i<multi.length;i++){
            if (multi[i] === ""){
                delete multi[i];
            } else {
                if (i == multi.length-1)
                    multiStr += multi[i];
                else
                    multiStr += multi[i] + '§';
            }
        }
        multi = multi.filter(Boolean);

        for (i=0;i<responses.length;i++){
            responses[i] += '<multi>' + multiStr + '</multi>'
        }
        data.responses = JSON.stringify(responses);
    }
    data.contextSet = context_set;
    if (context_filter != "") {
        data.contextFilter = context_filter;
    }
    $("#addButton").remove();
    $("#backButton").attr("disabled",true);
    $('#addButton2').attr("hidden",false).attr("disabled",true).html('Training del modello<span class="one">.</span><span class="two">.</span><span class="three">.</span>​');
    if (tag == "" || patterns[0] == "" || responses[0] == ""){
        alert('Uno o più campi sono mancanti!')
    } else {
        if (context_filter != ""){            
            $('#addButton2').attr("hidden",false).attr("disabled",true).html('Training del modello<span class="one">.</span><span class="two">.</span><span class="three">.</span>​');
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
                    setTimeout(function(){     $('#addButton2').attr("hidden",false).attr("disabled",true).html('Salvataggio<span class="one">.</span><span class="two">.</span><span class="three">.</span>​');}, 10000);
                    setInterval(function() {
                            $('#addButton2').attr("hidden",false).attr("disabled",true).html('Riavvio del server<span class="one">.</span><span class="two">.</span><span class="three">.</span>​');

                        $.ajax({ 
                            url  : API_ROOT,
                            type : "POST"
                        })
                        .done(function() {
                                $('#addButton2').attr("hidden",false).attr("disabled",true).html('Completato!');

                            window.location.replace('index.html')
                        });
                    }, 7000);
                }
            })
        } else {
                $('#addButton2').attr("hidden",false).attr("disabled",true).html('Training del modello<span class="one">.</span><span class="two">.</span><span class="three">.</span>​');

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
                    setTimeout(function(){     $('#addButton2').attr("hidden",false).attr("disabled",true).html('Salvataggio<span class="one">.</span><span class="two">.</span><span class="three">.</span>​');}, 10000);
                    setInterval(function() {
                            $('#addButton2').attr("hidden",false).attr("disabled",true).html('Riavvio del server<span class="one">.</span><span class="two">.</span><span class="three">.</span>​');

                        $.ajax({ 
                            url  : API_ROOT,
                            type : "POST"
                        })
                        .done(function() {
                                $('#addButton2').attr("hidden",false).attr("disabled",true).html('Completato!');
                            window.location.replace('index.html')
                        });
                    }, 7000);
                }
            })
        }
    } 
}
