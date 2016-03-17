$(document).ready(function (){
    var pageLink = $('#info-msg');

    pageLink.click(function(event){

        $.ajax({
            'url': '/diagr2/',
            'dataType': "json",
            'type': 'get',
            'success': function(data, status, xhr){
                var html = $(data);

                $('#info-msg div div').append($('#footer div').text());
                $('#info-msg div div').append(data.code);
            }
        });

        return false;
    });
});