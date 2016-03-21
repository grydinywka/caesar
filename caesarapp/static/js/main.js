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

function test(data) {
    alert(data);
}

function stripchars(string) {
    string = string.replace(RegExp('[^a-z ]','g'), ' ');
    string = string.replace(RegExp(' {2,}','g'), ' ');
    return string;
}

function infoMessage(textdata) {
    url='http://127.0.0.1:8000/static/txt/wordsEn.txt';
    ajax_eng_words('GET',url, function(data){
        var wordsEn = data.split('\n');
        var inpdata = textdata.toLowerCase(); //
        inpdata = stripchars(inpdata); // delete all chars exclude latins and spaces
        inpdata = inpdata.split(' ');

        test(inpdata);
        $('#info-msg div div').html(wordsEn.length);
        $('#info-msg').show();
    });
}

$(document).ready(function (){
    ajax_data_post_json();
    $('#input-text').focusout(function() {
        var input = document.getElementById("input-text");
        var json_data = countChars(input.value);

        charts(json_data,"ColumnChart");
        infoMessage(input.value);
    });
});