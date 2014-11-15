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

	$('.alert').delay(4000).fadeOut(1000);
});

function iframeHeight(val) {
	var $iframeGoogle=$("div#searchResult div.modal-dialog div.modal-content div.modal-body iframe#google");
	$iframeGoogle.css("height",val+"px");
}
