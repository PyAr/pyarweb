document.addEventListener('dal-init-function', function () {

  yl.registerFunction( 'your_autocomplete_function', function ($, element) {
    yl.functions['select2']($, element);

    $(element).on('select2:selecting', function(event) {
      const data = event.params.args.data;
      const tagId = data.id
      $(`input[name="tags"][value="${tagId}"]`).prop('checked', true)
      $(element).select2('close')
      event.preventDefault()
    })
  });
});
