function getCookie(name) {
  var cookieValue = null;
  if(document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for(var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if(cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

$.ajaxSetup({
  global: true,
  beforeSend: function(xhr, settings) {
      if(!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
          xhr.setRequestHeader("Content-Type", 'application/x-www-form-urlencoded; charset=UTF-8');
      }
  },
  timeout: 8000
});

$('#search input[name="q"]').autocomplete({
  'source': "{% url 'learning_logs:search' %}",
  'minLength': 2,
  'appendTo': "#search"
});