document.addEventListener('dal-init-function', function () {

  yl.registerFunction( 'your_autocomplete_function', function ($, element) {
    var $element = $(element);

    var ajax = {
      url: $element.attr('data-autocomplete-light-url'),
      dataType: 'json',
      delay: 250,

      data: function (params) {
        var data = {
          q: params.term, // search term
          page: params.page,
          create: $element.attr('data-autocomplete-light-create') && !$element.attr('data-tags'),
          forward: yl.getForwards($element)
        };

        return data;
      },
      cache: true
    };

    function createTag(params) {
      var term = $.trim(params.term);

      if (term === '') {
        return null;
      }


      return {
        id: '_q',
        text: `Buscar '${params.term}'`,
        term: params.term
      };
    };

    $element.select2({
      debug: true,
      containerCssClass: ':all:',
      createTag: createTag,
      tags: true,
      placeholder: $element.attr('data-placeholder') || '',
      language: $element.attr('data-autocomplete-light-language'),
      minimumInputLength: 0,
      allowClear: !$element.is('[required]'),
      ajax: ajax,
      with: null
    });

    // function log(name, event) {
    //   console.log(name);
    //   console.log(event);
    // }

    // $element.on("select2:open", function (e) { log("select2:open", e); });
    // $element.on("select2:close", function (e) { log("select2:close", e); });
    // $element.on("select2:select", function (e) { log("select2:select", e); });
    // $element.on("select2:unselect", function (e) { log("select2:unselect", e); });

    $element.on('select2:selecting', function(event) {
      const data = event.params.args.data;
      const tagId = data.id;

      if (tagId == '_q') {
        return;
      }

      $(`input[name="tags"][value="${tagId}"]`).prop('checked', true);

      const inputHtml = `<input type="checkbox" name="tags" value="${tagId}" checked>`;
      const labelHtml = `<label class="label label-primary">${data.text} ${inputHtml}</label>`;

      $('#id_tags').append($(labelHtml));
      $(element).select2('close');
      event.preventDefault();
    });
  });
});
