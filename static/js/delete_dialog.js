$(document).ready(function () {
    $('#delete-dialog').on('show.bs.modal', function (event) {
        var deleteButton = $(event.relatedTarget);
        var deleteForm = $('#' + deleteButton.attr('data-form-id'));
        var modal = $(this);
        modal.find('#yes-button').unbind().click(function () {
            deleteForm.submit();
        });
    });
});