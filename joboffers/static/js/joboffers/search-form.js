document.addEventListener('dal-init-function', function () {

  yl.registerFunction( 'your_autocomplete_function', function ($, element) {
    yl.functions['select2']($, element);

    $(element).on('select2:selecting', function(event) {
      const data = event.params.args.data;
      const tagId = data.id

      $(`input[name="tags"][value="${tagId}"]`).prop('checked', true)

      const inputHtml = `<input type="checkbox" name="tags" value="${tagId}" checked>`
      const labelHtml = `<label class="label label-primary">${data.text} ${inputHtml}</label>`;

      $('#id_tags').append($(labelHtml))
      $(element).select2('close')
      event.preventDefault()
    })
  });
});
