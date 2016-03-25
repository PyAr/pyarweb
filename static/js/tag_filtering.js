var classNames = ['btn-default', 'included btn-success', 'excluded btn-danger'];
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
});

$('#tags-form #reset-btn').click(function() {
    $('#tags-form select').val(0);
    $.each(classNames, function (index, value) {
        $('#tags-form .filter_tag').removeClass(value);
    });
    $('#tags-form .filter_tag').addClass(classNames[0]);
});


$('#search-tag').on('keyup', function(event){
    $('.filter_tag:not(:contains("' + $(event.target).val() + '"))').css('display', 'none');
    $('.filter_tag:contains("' + $(event.target).val() + '"), .filter_tag.included').css('display', 'inline-block');
})
