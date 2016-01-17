$(document).ready(function () {
    $('#placements-table tfoot th').each(function () {
        if ($(this).html()) {
            var title = $(this).text();
            $(this).html('<input id="footer-search" type="text" placeholder="' + title + '" />');
        }
    });

    var table = $('#placements-table').DataTable({
        "columnDefs": [
            {"searchable": false, "orderable": false, "targets": [0, 1, 10]},
            {"orderDataType": "dom-text", "targets": 6},
            {"orderDataType": "dom-checkbox", "targets": [7, 9]},
            {"orderDataType": "dom-select", "targets": 8},
        ],
        "order": [[8, "desc"]],
        "dom": 't<"row"<"col-sm-6 col-sm-offset-1"p>>',
        "language": {
            "zeroRecords": "Keine Einträge gefunden",
            "paginate": {
                "previous": "Zurück",
                "next": "Weiter"
            }
        }
    });

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