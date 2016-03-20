function ajax_data_post_json() {
    var form = $('form');

        form.ajaxForm({
            dataType: "json",
            'data': {
                'custom_input': $('input[name="rot"]').val(), "FRUIT": "selected"
            },
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
                    $('#status_msg').show().html('Помилка валідації! Виправте їх!.');
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
                data.addRows([ [name, value]]);
            }
        });

        var options = {
        title : "Частота кожного символу в тексті.",
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

// func for checking if it is latin char; 65 == 'A', 90 == 'Z', 97 == 'a', 122 == 'z'
function is_latin(code){
    if ( ((code >= 97) && (code <= 122)) || ((code >= 65) && (code <= 90)) ) {
        return true;
    }
    return false;
}

function countQuantityLatin(inpdata) {
    var lenLatin = 26;
    var json = new Array(lenLatin);
    var len_data = inpdata.length;

    inpdata = inpdata.toLowerCase();

//    dump default data in json = [{'name': 'a', 'value': 0},...,{'name': 'z', 'value': 0}]
    for (var i = 0; i < lenLatin; i++) {
        json[i] = {'name': String.fromCharCode(97+i), "value": 0};
    }

//    Counting value of every letter of input data
    for ( var i = 0; i < len_data; i++ ) {
        var code = inpdata.charCodeAt(i)-97;

        if (is_latin(inpdata.charCodeAt(i)) === true) {
            json[code].value += 1;
        }
    }

  return json;
}

function countQuantityChars(inpdata) {
    var json = [];
    var len_data = inpdata.length;

//    Counting value of every char of input data
    for ( var i = 0; i < len_data; i++ ) {
        var code = inpdata.charCodeAt(i);

        if (json[code] === undefined) {
            if (code === 10) {
                json[10] = {'name': "\\n", "value": 1};
            } else if (code === 32) {
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

function beginChart(){
    var input = document.getElementById("input-text");
    var json_data = countQuantityChars(input.value);

    charts(json_data,"ColumnChart");
}

$(document).ready(function (){
    ajax_data_post_json();
    charts(data,ChartType);
    is_latin(code);
    countQuantityChars(inpdata);
    sendCode();
});