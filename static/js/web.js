$(document).ready(function() {
	if(window.location.pathname=="/") {
		$("header nav li a[href='/']").parent().addClass("active");
	} else {
		$("header nav li.active").removeClass("active");
		$("header nav li a[href='/"+window.location.pathname.split("/")[1]+"/']").parent().addClass("active");
	}

	var $searchModal=$("div#searchResult");
	var $iframeGoogle=$searchModal.find("div.modal-dialog div.modal-content div.modal-body iframe#google");

	function buscar() {
		var text=$("input.search").val();
		if(text===undefined || text=="") {
			text=$("form#search-form input.form-control.input-lg").val();
			$("input.search").val(text);
		}
		$iframeGoogle.attr("src","/static/search.html?q="+text);
	}
	
	$("form#search-form").bind("submit",function(a) {
		buscar();
		$searchModal.modal("show");
		return false;
	});
	
	$("form#search-form.form-control.input-lg,div#searchResult input.search").bind("keydown",function(a) {
		if (a.keyCode == 13) {
			buscar();
			$searchModal.modal("show");
			return false;
		}
	});
	
	$("span.input-group-btn button.btn.btn-default.btn-lg").bind("click",function(a) {
		buscar();
		$searchModal.modal("show");
	});
	
	$searchModal.on("hide.bs.modal",function() {
		$("div#searchResult input.search").val("");
	});
});

function iframeHeight(val) {
	var $iframeGoogle=$("div#searchResult div.modal-dialog div.modal-content div.modal-body iframe#google");
	$iframeGoogle.css("height",val+"px");
}



// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
