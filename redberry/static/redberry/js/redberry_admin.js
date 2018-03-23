var RedberryAdmin = {

    _init_rich_text: function(){
        $('.rich-editable').trumbowyg({
            btns: [
                ['preformatted'],
                ['viewHTML'],
                ['undo', 'redo'], // Only supported in Blink browsers
                ['formatting'],
                ['strong', 'em', 'del'],
                ['superscript', 'subscript'],
                ['link'],
                ['insertImage'],
                ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
                ['unorderedList', 'orderedList'],
                ['horizontalRule'],
                ['table'],
                ['fullscreen']
            ],
            autogrow: true
        });
    },

    init: function(){
        RedberryAdmin._init_rich_text()
    }
}

$(document).ready(function(){
    RedberryAdmin.init()
})
