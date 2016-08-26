$(document).ready(function () {
    <!-- Jede Spalte der Tabelle mit einem nicht-leeren th-Element innerhalb von tfoot erhält eine Searchbox -->
    $('#poster-table tfoot th').each(function () {
        if ($(this).html()) {
            var title = $(this).text();
            $(this).html('<input id="footer-search" type="text" placeholder="' + title + '" style="width: 130px;" />');
        }
    });

    <!-- Tabelleninitialisierung -->
    var poster_table = $('#poster-table').DataTable({
        "columnDefs": [
            {"searchable": false, "orderable": false, "targets": 9},
            {"orderDataType": "dom-checkbox", "targets": [7, 8]},
            {"orderDataType": "dom-text", "targets": 5, "type": 'de_date'}
        ],
        "order": [[5, "asc"]],
        "dom": 't<"row"<"col-sm-6 col-sm-offset-1"p>>',
        "language": {
            "zeroRecords": "Keine Einträge gefunden",
            "paginate": {
                "previous": "Zurück",
                "next": "Weiter"
            }
        },
        stateSave: true
    });

    <!-- Zustand der Searchboxen wiederherstellen -->
    var poster_state = poster_table.state.loaded();
    if (poster_state) {
        poster_table.columns().eq(0).each(function (colIdx) {
            var colSearch = poster_state.columns[colIdx].search;

            if (colSearch.search) {
                $('input', poster_table.column(colIdx).footer()).val(colSearch.search);
            }
        });

        poster_table.draw();
    }

    <!-- Suchfunktion für jede Searchbox -->
    poster_table.columns().every(function () {
        var that = this;

        $('#footer-search', this.footer()).on('keyup change', function () {
            if (that.search() !== this.value) {
                that
                    .search(this.value)
                    .draw();
            }
        });
    });
});