function ajax_data_post_json() {
    var form = $('form');

        form.ajaxForm({
            dataType: "json",
            'beforeSend': function() {

            },
			'error': function(){
				alert('Error on server. Attempt later, please!');

				return false;
			},
			'success': function(data, status, xhr){
			    var input_error = $('#input-text-error');
                var rotate_error = $('#rot-error');

                if ('errors' in data) {
                    $('#status_msg').show().html('Помилки валідації! Виправте їх!.');
                    if ('input_text' in data.errors) {
                        input_error.html(data.errors.input_text);
                        input_error.parent().addClass('has-error');

                    } else {
                        input_error.html('');
                        input_error.parent().removeClass('has-error');
                    }
                    if ('rot' in data.errors) {
                        rotate_error.html(data.errors.rot);
                        rotate_error.parent().addClass('has-error');
                    } else {
                        rotate_error.html('');
                        rotate_error.parent().removeClass('has-error');
                    }
                } else {
                    $('#input-text-error').html('');
                    $('#rot-error').html('');
                    $('#status_msg').hide();
                    input_error.parent().removeClass('has-error');
                    rotate_error.parent().removeClass('has-error');
                }


                if ('crypt' in data) {
                    $("#result-field").html('Результат: Зашифрований текст');
                } else if ('encrypt' in data) {
                    $("#result-field").html('Результат: Розшифрований текст');
                } else {
                    $("#result-field").html('Результат');
                }

                $("textarea[name='output-text']").html(data.output_text);
			}
        });
}

// Function for build chart
function charts(data,ChartType){
    var c=ChartType;
    var jsonData=data;
    google.load("visualization", "1", {packages:["corechart"], callback: drawVisualization});
    function drawVisualization(){
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Літера');
        data.addColumn('number', 'Кількіть літер');
        $.each(jsonData, function(i,jsonData){
            if (jsonData != undefined) {
                var value=jsonData.value;
                var name=jsonData.name;
                data.addRows([[name, value]]);
            }
        });

        var options = {
        title : "Частота кожного введеного символу в тексті.",
        colorAxis: {colors: ['#54C492', '#cc0000']},
        datalessRegionColor: '#dedede',
        defaultColor: '#dedede'
        };

        var chart;
        if(c=="ColumnChart")
            chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));

        chart.draw(data, options);
        $('#frequency-diagram').show();
    }
}

function countChars(inpdata) {
    var json = [];
    var len_data = inpdata.length;

//    Counting value of every char of input data
    for ( var i = 0; i < len_data; i++ ) {
        var code = inpdata.charCodeAt(i);

        if (json[code] === undefined) {
            if (code === 10) { // for new line char
                json[10] = {'name': "\\n", "value": 1};
            } else if (code === 32) { // for space char
                json[32] = {'name': "' '", "value": 1};
            } else {
                json[code] = {'name': inpdata[i], "value": 1};
            }
        } else {
            json[code].value += 1;
        }
    }

  return json;
}

function ajax_eng_words(type, url, success){
    $.ajax({
        type:type,
        url:url,
        dataType:"text",
        restful:true,
        cache:false,
        timeout:20000,
        async:true,
        beforeSend :function(data) { },
        success:function(data){
            success.call(this, data);
        },
        error:function(data){
            alert("Error In Connecting");
            return false;
        }
    });
}

function stripchars(string) {
    string = string.replace(RegExp('[^a-z ]','g'), ' ');
    string = string.replace(RegExp(' {2,}','g'), ' ');
    string = string.replace(RegExp('^ ','g'), '');
    string = string.replace(RegExp(' $','g'), '');
    return string;
}

function encrypt(str, rot) { // this func is only for the file
    var encrypted = "";

    for (var i = 0; i < str.length; i++) {
        var shift = str.charCodeAt(i) - rot;
        if ( shift < 97 )
            shift += 26;
        encrypted += String.fromCharCode(shift);
    }

    return encrypted;
}

function infoMessage(textdata) { // textdata - data from input field
    url='/static/txt/wordsEn.txt';
    ajax_eng_words('GET',url, function(data){ // data - string of English words

        var inpdata = textdata.toLowerCase(); //

        inpdata = stripchars(inpdata); // delete all chars exclude latins and spaces
        inpdata = inpdata.split(' '); // array of input words
        if ( inpdata.length > 200)
            inpdata.length = 200

//--------------------------------------------------------------------
// Check if input data is valid words
        var counter = 0;
        for ( var i = 0; i < inpdata.length; i++ ) {
            var patt = new RegExp('\\s'+inpdata[i]+'\\s', 'g');
            if ( patt.test(data) )
                counter += 1;
        }
        if (inpdata == '')
            inpdata.length = -1;

        if (counter == inpdata.length) {
            $('#info-msg div div').html('<p>Введений текст незашифрований! Кожне слово міститься в англійському\
            словнику.</p>');
        } else {
            var flagRot = 0;
            for ( var rot = 1; rot < 26; rot++ ) { // rot = i
                var counter2 = 0;
                for ( var i = 0; i < inpdata.length; i++ ) {
                    var word = encrypt(inpdata[i], rot);
                    var patt = new RegExp('\\s'+word+'\\s', 'g');

                    if ( patt.test(data) )
                        counter2 += 1;
                }

                if (counter2 == inpdata.length) { // if encrypted is in Eng dict
                    flagRot = rot;
                    rot = 26; // exit from loop
                }
            }

            if ( flagRot != 0 ) {
                $('#info-msg div div').html('Введений текст Зашифрований в ROT ' + flagRot );
            } else {
                $('#info-msg div div').html('Введений текст або містись помилки, або зашифрований не шифром Цезаря,\
                або деякі слова не є словами англійської мови, або містить власні назви!');
            }
        }
        $('#info-msg').show();

    });
}


$(document).ready(function (){
    ajax_data_post_json();
    $('#input-text').click(function(){
        $('#info-msg').hide();
//        $('#frequency-diagram').hide();

        return false;
    });

    $('#input-text').focusout(function() {
        var input = $("#input-text").val();
        var json_data = countChars(input);

        charts(json_data,"ColumnChart");
        infoMessage(input);
    });
});