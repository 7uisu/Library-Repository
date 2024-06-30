$(document).ready(function () {
    $('#id_pen_names').select2({
        ajax: {
            url: '/pen-name-autocomplete/',  // Correct URL for pen name autocomplete
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term,
                    page: params.page
                };
            },
            processResults: function (data, params) {
                params.page = params.page || 1;
                return {
                    results: data.results,
                    pagination: {
                        more: (params.page * 10) < data.count
                    }
                };
            },
            cache: true
        },
        placeholder: 'Search Pen Names',
        escapeMarkup: function (markup) {
            return markup;
        },
        minimumInputLength: 1
    });
});
