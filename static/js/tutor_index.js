$(document).ready(function () {
    <!-- Jede Spalte der Tabelle mit einem nicht-leeren th-Element innerhalb von tfoot erhält eine Searchbox -->
    $('#placements-table tfoot th').each(function () {
        if ($(this).html()) {
            var title = $(this).text();
            $(this).html('<input id="footer-search" type="text" placeholder="' + title + '" />');
        }
    });

    <!-- Tabelleninitialisierung -->
    var table = $('#placements-table').DataTable({
        "columnDefs": [
            {"searchable": false, "orderable": false, "targets": [0, 8]},
            {"orderDataType": "dom-text", "targets": 5},
            {"orderDataType": "dom-checkbox", "targets": 7},
            {"orderDataType": "dom-select", "targets": 6}
        ],
        "order": [[7, "desc"]],
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
    var state = table.state.loaded();
    if (state) {
        table.columns().eq(0).each(function (colIdx) {
            var colSearch = state.columns[colIdx].search;

            if (colSearch.search) {
                $('input', table.column(colIdx).footer()).val(colSearch.search);
            }
        });

        table.draw();
    }

    <!-- Suchfunktion für jede Searchbox -->
    table.columns().every(function () {
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