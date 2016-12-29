var RedberryAdmin = {

    _init_rich_text: function(){
        $.getScript( "https://cdn.quilljs.com/1.1.8/quill.js", function( data, textStatus, jqxhr ) {
            var quill = new Quill('.rich-editable', {
                theme: 'snow'
            })

            $('.rich-editable').closest('form').submit(function(){

                $('.rich-editable').each(function(){
                    var textarea_id = $(this).attr('data-id')
                    $('textarea#' + textarea_id).text( $(this).find('.ql-editor').html() )

                    console.log(textarea_id)
                    console.log($(this).find('.ql-editor').html())
                })
                return true
            })

        });
    },

    init: function(){
        RedberryAdmin._init_rich_text()
    }
}

$(document).ready(function(){
    RedberryAdmin.init()
})
