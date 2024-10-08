   // Prevent default right-click context menu
    $(document).on('contextmenu', function (e) {
        e.preventDefault();
    });

    // Show context menu on right-click on table row
    $('table tbody tr').on('contextmenu', function (e) {
        var rowId = $(this).data('id');  // Get the row ID

        // Position the context menu at the mouse pointer location
        $('#context-menu').css({
            top: e.pageY + 'px',
            left: e.pageX + 'px',
            display: 'block'
        }).data('rowId', rowId);  // Store row ID for later use

        return false;  // Prevent the browser's default menu
    });

    // Hide context menu on any click outside
    $(document).click(function () {
        $('#context-menu').hide();
    });

    // Handle Edit button action
    $('#context-select').on('click', function () {
        var rowId = $('#context-menu').data('id');
        alert('Select row: ' + rowId);
        $('#context-menu').hide();
    });

    // Handle Edit button action
    $('#context-unselect').on('click', function () {
        var rowId = $('#context-menu').data('rowId');
//        alert('Unselect row: ' + rowId);
        $('#context-menu').hide();
    });

    // Handle Edit button action
    $('#context-edit').on('click', function () {
        var rowId = $('#context-menu').data('rowId');
//        alert('Edit row: ' + rowId);
        $('#context-menu').hide();
    });


    // Handle Delete button action
    $('#context-delete').on('click', function () {
        var rowId = $('#context-menu').data('rowId');
//        alert('Delete row: ' + rowId);
        $('#context-menu').hide();
    });

    // Handle View button action
    $('#context-view').on('click', function () {
        var rowId = $('#context-menu').data('rowId');
        alert('View row: ' + rowId);
        $('#context-menu').hide();
    });

    // Handle Edit button action
    $('#context-update').on('click', function () {
        var rowId = $('#context-menu').data('rowId');
//        alert('Update row: ' + rowId);
        $('#context-menu').hide();
    });
    // Handle Edit button action
    $('#context-copy').on('click', function () {
        var rowId = $('#context-menu').data('rowId');
//        alert('Update row: ' + rowId);
        $('#context-menu').hide();
    });

    // Handle submenu (More Actions)
    $('.dropdown-submenu > a').on('click', function (e) {
        var submenu = $(this).next('ul');
        submenu.toggle();  // Toggle the submenu visibility
        e.stopPropagation();
        e.preventDefault();
    });


//        $(document).ready(function() {

        // Show the form modal when "Add New" is clicked
            $('#addNewBtn').click(function() {
                $('#addWebsiteModal').modal('show');
            });

            // Submit form via AJAX
            $('#submitWebsiteBtn').click(function() {
                let websiteData = {
                    domain: $('#domain').val(),
                    hosting: $('#hosting').val(),
                    gmail: $('#gmail').val(),
                    password: $('#password').val(),
                    link: $('#link').val(),
                    adsnetwork: $('#adsnetwork').val(),
                    earning: $('#earning').val(),
                    status: $('#status').val(),
                    description: $('#description').val(),
                };

                $.ajax({
                    url: '/add_website',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(websiteData),
                    success: function(response) {
                        $('#addWebsiteModal').modal('hide');
                        // Optionally, refresh the page or clear form inputs
                        location.reload();
                    }
                });
            });
//        });