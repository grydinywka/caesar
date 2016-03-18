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
                if ('crypt' in data) {
                    $("#result-field").html('Результат: Зашифрований текст');
                } else if ('encrypt' in data) {
                    $("#result-field").html('Результат: Розшифрований текст');
                }

                $("textarea[name='output-text']").html(data.output_text);
//                $('textarea').attr('value', data.output_text);
			}
        });
}

$(document).ready(function (){
//    $("input[name='crypt']").click(function() {
//
//
//        return false;
//    });
    ajax_data_post_json();
});