$('#close_delete_message').click(
    function() {
        $.fancybox.close();
    }
);

$("[data-deletelink]").fancybox({
    beforeLoad: function(instance, slide) {
    	var id = slide.opts.$orig.data('id');
    	var text = slide.opts.$orig.data('text');
    	var url = slide.opts.$orig.data('url');
        $('#title').text(text);
        console.log(url);
        $('#submit_btn').attr({ 'href': url });
    }
});