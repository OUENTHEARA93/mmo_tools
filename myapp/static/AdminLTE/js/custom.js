//   // Prevent default right-click context menu
//    $(document).on('contextmenu', function (e) {
//        e.preventDefault();
//    });
//
//    // Show context menu on right-click on table row
//    $('table tbody tr').on('contextmenu', function (e) {
//        var rowId = $(this).data('id');  // Get the row ID
//
//        // Position the context menu at the mouse pointer location
//        $('#context-menu').css({
//            top: e.pageY + 'px',
//            left: e.pageX + 'px',
//            display: 'block'
//        }).data('rowId', rowId);  // Store row ID for later use
//
//        return false;  // Prevent the browser's default menu
//    });
//
//    // Hide context menu on any click outside
//    $(document).click(function () {
//        $('#context-menu').hide();
//    });
//
//    // Handle Edit button action
//    $('#context-select').on('click', function () {
//        var rowId = $('#context-menu').data('rowId');
////        alert('Select row: ' + rowId);
//        $('#context-menu').hide();
//    });
//
//    // Handle Edit button action
//    $('#context-unselect').on('click', function () {
//        var rowId = $('#context-menu').data('rowId');
////        alert('Unselect row: ' + rowId);
//        $('#context-menu').hide();
//    });
//
//    // Handle Edit button action
//    $('#context-edit').on('click', function () {
//        var rowId = $('#context-menu').data('rowId');
////        alert('Edit row: ' + rowId);
//        $('#context-menu').hide();
//    });
//
//
//    // Handle Delete button action
//    $('#context-delete').on('click', function () {
//        var rowId = $('#context-menu').data('rowId');
////        alert('Delete row: ' + rowId);
//        $('#context-menu').hide();
//    });
//
//    // Handle View button action
//    $('#context-view').on('click', function () {
//        var rowId = $('#context-menu').data('rowId');
//        alert('View row: ' + rowId);
//        $('#context-menu').hide();
//    });
//
//    // Handle Edit button action
//    $('#context-update').on('click', function () {
//        var rowId = $('#context-menu').data('rowId');
////        alert('Update row: ' + rowId);
//        $('#context-menu').hide();
//    });
//    // Handle Edit button action
//    $('#context-copy').on('click', function () {
//        var rowId = $('#context-menu').data('rowId');
////        alert('Update row: ' + rowId);
//        $('#context-menu').hide();
//    });
//
//    // Handle submenu (More Actions)
//    $('.dropdown-submenu > a').on('click', function (e) {
//        var submenu = $(this).next('ul');
//        submenu.toggle();  // Toggle the submenu visibility
//        e.stopPropagation();
//        e.preventDefault();
//    });

// When the "Check All" checkbox is clicked
        $('#checkAll').on('change', function() {
            var isChecked = $(this).is(':checked');

            // Set all row checkboxes to the same state
            $('.row-checkbox').prop('checked', isChecked);
        });

        // If any row checkbox is unchecked, uncheck "Check All"
        $('.row-checkbox').on('change', function() {
            if (!$('.row-checkbox').is(':checked')) {
                $('#checkAll').prop('checked', false);
            }
        });