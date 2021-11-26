document.addEventListener('dal-init-function', function () {

  yl.registerFunction( 'your_autocomplete_function', function ($, element) {
    const $element = $(element);

    const ajax = {
      url: $element.attr('data-autocomplete-light-url'),
      dataType: 'json',
      delay: 250,

      data: function (params) {
        const data = {
          q: params.term, // search term
          page: params.page,
          create: $element.attr('data-autocomplete-light-create') && !$element.attr('data-tags'),
          forward: yl.getForwards($element)
        };

        return data;
      },
      processResults: function (data) {
        const tagsEl = Array.from(document.querySelectorAll('input[name="tags"]'));
        const selectedTags = tagsEl.map(function (element) { return element.value; });
        data.results = data.results.filter(function (result) {
          return !selectedTags.includes(result.id);
        });
        return data;
      },
      cache: true
    };

    function createTag(params) {
      const term = $.trim(params.term);

      return {
        id: params.term,
        text: `Buscar '${params.term}'`,
        search: true
      };
    };

    $element.select2({
      debug: true,
      containerCssClass: ':all:',
      createTag: createTag,
      tags: true,
      multiple: false,
      placeholder: $element.attr('data-placeholder') || '',
      language: $element.attr('data-autocomplete-light-language'),
      minimumInputLength: 0,
      allowClear: !$element.is('[required]'),
      ajax: ajax,
      with: null
    });

    function log(name, event) {
      console.log(name, event);
    }

    $element.on("select2:select", function(event){
      document.querySelector('#filter-form').submit();
    });

    $element.on("select2:select", function (e) { log("select2:select", e); });
    $element.on("select2:open", function (e) { log("select2:open", e); });
    $element.on("select2:close", function (e) { log("select2:close", e); });
    $element.on("select2:unselect", function (e) { log("select2:unselect", e); });
    $element.on("select2:change", function (e) { log("select2:change", e); });


    $element.on('select2:selecting', function(event) {
      console.log('select2:selecting::', event);
      // Crea los labels que van abajo
      const data = event.params.args.data;
      console.log("data::", data);

      if (data.search) {
        // console.log('submitting...');
        // document.querySelector('#filter-form').submit();
        return;
      }

      if (data.prevented) {
        e.preventDefault();
        return;
      }


      $(`input[name="tags"][value="${data.id}"]`).prop('checked', true);
      const inputHtml = `<input type="checkbox" name="tags" value="${data.id}" checked>`;
      const labelHtml = `<label class="label label-primary">${data.text} ${inputHtml}</label>`;
      $('#id_tags').append($(labelHtml));
      $(element).select2('close');
      event.preventDefault();
    });
  });
});
