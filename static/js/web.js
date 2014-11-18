$(document).ready(function() {
	if(window.location.pathname=="/") {
		$("header nav li a[href='/']").parent().addClass("active");
	} else {
		$("header nav li.active").removeClass("active");
		$("header nav li a[href='/"+window.location.pathname.split("/")[1]+"/']").parent().addClass("active");
	}
}