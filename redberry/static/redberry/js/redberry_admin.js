var RedberryAdmin = {

    _init_rich_text: function(){
        $.getScript( "https://cdn.quilljs.com/1.1.8/quill.js", function( data, textStatus, jqxhr ) {

            $('.rich-editable').each(function(){
                var quill = new Quill("#" + $(this).attr('id'), {
                    theme: 'snow'
                })
            })

            $('.rich-editable').closest('form').submit(function(){

                $('.rich-editable').each(function(){
                    var textarea_id = $(this).attr('id')
                    var edited_text = $(this).find('.ql-editor').html()

                    $('textarea#' + textarea_id).text( edited_text )

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
