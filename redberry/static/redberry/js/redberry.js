var Redberry = {

    _init_event_handlers: function(){
        $('.close').click(function(){
            var el = $(this).attr('data-dismiss')
            $(this).closest('.' + el).slideUp(function(){
                $(this).remove()
            })
        })
    },

    init: function(){
        Redberry._init_event_handlers()
    }
}

$(document).ready(function(){
    Redberry.init()
})
