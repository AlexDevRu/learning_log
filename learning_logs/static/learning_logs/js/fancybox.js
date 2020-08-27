$('#close_delete_message').click(
    function() {
        $.fancybox.close();
    }
);

$("[data-deletelink]").fancybox({
    beforeLoad: function(instance, slide) {
    	var topic_id = slide.opts.$orig.data('topic_id');
    	var topic_text = slide.opts.$orig.data('topic_text');
        $('#topic_title').text(topic_text);
        console.log("/delete_topic/" + topic_id + "/");
        $('#topic_btn').attr({ 'href': "/delete_topic/" + topic_id + "/" });
    }
});