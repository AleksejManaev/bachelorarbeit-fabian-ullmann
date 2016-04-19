$.fn.dataTable.ext.search.push(
    function (settings, data, dataIndex) {
        if (settings.sInstance != 'thesis-table') {
            return true;
        }
        var filter_checkbox = document.getElementById("filter-checkbox").checked;
        if (filter_checkbox) {
            var completed = document.getElementsByClassName("completed")[dataIndex].checked;
            return !completed;
        }
        else {
            return true;
        }
    }
);

$(document).ready(function () {
    <!-- Jede Spalte der Tabelle mit einem nicht-leeren th-Element innerhalb von tfoot erhält eine Searchbox -->
    $('#placements-table tfoot th').each(function () {
        if ($(this).html()) {
            var title = $(this).text();
            $(this).html('<input id="footer-search" type="text" placeholder="' + title + '" style="width: 130px;" />');
        }
    });

    $('#thesis-table tfoot th').each(function () {
        if ($(this).html()) {
            var title = $(this).text();
            $(this).html('<input id="footer-search" type="text" placeholder="' + title + '" style="width: 130px;" />');
        }
    });

    <!-- Tabelleninitialisierung -->
    var placement_table = $('#placements-table').DataTable({
        "columnDefs": [
            {"searchable": false, "orderable": false, "targets": [0, 1, 10]},
            {"orderDataType": "dom-checkbox", "targets": 9},
            {"orderDataType": "dom-select", "targets": 8},
        ],
        "order": [[9, "asc"]],
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

    var thesis_table = $('#thesis-table').DataTable({
        "columnDefs": [
            {"searchable": false, "orderable": false, "targets": [0, 9]},
            {"orderDataType": "dom-select", "targets": [4, 5]},
            {"orderDataType": "dom-checkbox", "targets": 8},
            {"type": 'de_date', targets: 6}
        ],
        "order": [[6, "asc"]],
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
    var placement_state = placement_table.state.loaded();
    if (placement_state) {
        placement_table.columns().eq(0).each(function (colIdx) {
            var colSearch = placement_state.columns[colIdx].search;

            if (colSearch.search) {
                $('input', placement_table.column(colIdx).footer()).val(colSearch.search);
            }
        });

        placement_table.draw();
    }

    var thesis_state = thesis_table.state.loaded();
    if (thesis_state) {
        thesis_table.columns().eq(0).each(function (colIdx) {
            var colSearch = thesis_state.columns[colIdx].search;

            if (colSearch.search) {
                $('input', thesis_table.column(colIdx).footer()).val(colSearch.search);
            }
        });

        thesis_table.draw();
    }

    <!-- Suchfunktion für jede Searchbox -->
    placement_table.columns().every(function () {
        var that = this;

        $('#footer-search', this.footer()).on('keyup change', function () {
            if (that.search() !== this.value) {
                that
                    .search(this.value)
                    .draw();
            }
        });
    });

    thesis_table.columns().every(function () {
        var that = this;

        $('#footer-search', this.footer()).on('keyup change', function () {
            if (that.search() !== this.value) {
                that
                    .search(this.value)
                    .draw();
            }
        });
    });

    $('#filter-checkbox').click(function () {
        thesis_table.draw();
    });
});


