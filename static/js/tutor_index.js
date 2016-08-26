$(document).ready(function () {
    <!-- Jede Spalte der Tabelle mit einem th-Element, das nur Text und keine HTML-Tags enthält, innerhalb von tfoot, erhält eine Searchbox -->
    $('#placements-table tfoot th').each(function () {
        if ($(this).html() && $(this).children().length == 0) {
            var title = $(this).text();
            $(this).html('<input id="footer-search" type="text" placeholder="' + title + '" style="width: 130px;" />');
        }
    });

    $('#thesis-table tfoot th').each(function () {
        if ($(this).html() && $(this).children().length == 0) {
            var title = $(this).text();
            $(this).html('<input id="footer-search" type="text" placeholder="' + title + '" style="width: 130px;" />');
        }
    });

    <!-- Tabelleninitialisierung -->
    var placement_table = $('#placements-table').DataTable({
        "columnDefs": [
            {"searchable": false, "orderable": false, "targets": [0, 1, 12]},
            {"orderDataType": "dom-checkbox", "targets": 11},
            {"orderDataType": "dom-select", "targets": [9, 10]}
        ],
        "order": [[10, "asc"]],
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
            {"searchable": false, "orderable": false, "targets": [0, 13]},
            {"orderDataType": "dom-select", "targets": [7, 8, 11]},
            {"orderDataType": "dom-checkbox", "targets": 12},
            {"orderDataType": "dom-text", "targets": 9, "type": 'de_date'}
        ],
        "order": [[8, "asc"]],
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

    <!-- Buttons zum Togglen von archivierten Praktika bzw. Abschlussarbeiten erstellen und Eventhandling setzen -->
    toggleArchivedPlacementsButton = $("[name='toggle-archived-placements']").bootstrapSwitch();
    toggleArchivedThesesButton = $("[name='toggle-archived-theses']").bootstrapSwitch();

    var toggleArchived = function (event, state) {
        const toggleButton = $(event.target);
        const table = (toggleButton.attr('name') == 'toggle-archived-placements') ? placement_table : (toggleButton.attr('name') == 'toggle-archived-theses') ? thesis_table : false;
        if (!table) return;

        if (state) {
            $.fn.dataTable.ext.search.push(
                function (settings, data, dataIndex) {
                    return !$(table.row(dataIndex).node()).find("[name='archived']").is(':checked');
                }
            );
            table.draw();
        }
        else {
            $.fn.dataTable.ext.search.pop();
            table.draw();
        }
    }

    toggleArchivedPlacementsButton.on('switchChange.bootstrapSwitch', toggleArchived);
    toggleArchivedThesesButton.on('switchChange.bootstrapSwitch', toggleArchived);
});


