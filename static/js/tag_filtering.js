// var classNames = ['btn-default', 'included btn-success', 'excluded btn-danger'];
var classNames = ['btn-default', 'included btn-success'];
$('#tags-form .filter_tag').click(function () {
    var $this = $(this),
    $select = $('#' + $this.attr('for'));
    $this.toggleClass(function (i, className, b) {
        var ret_index;
        $.each(classNames, function (index, value) {
            if ($this.hasClass(value)) {
                ret_index = (index + 1) % classNames.length;
                $select.val(ret_index);
            }
        });
        $this.removeClass(classNames.join(' '));
        return classNames[ret_index];
    });
    $('#tags-form').submit();
});

$('#tags-form #reset-btn').click(function() {
    $('#tags-form select').val(0);
    $.each(classNames, function (index, value) {
        $('#tags-form .filter_tag').removeClass(value);
    });
    $('#tags-form .filter_tag').addClass(classNames[0]);
    $('#tags-form').submit();
});

$("#tags-form").submit(function() {
    $('#tags-form select').not(
            $('#tags-form option:selected').not('[value=""]').parent()
    ).prop('disabled', true);
    return true;
});


$("#show-active").click(function() {
    this.form.active.value=this.checked;
    $("#buscar").click();
});
