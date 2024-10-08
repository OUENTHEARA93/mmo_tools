$(document).ready(function() {

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



    // When the "Check All" checkbox is clicked
        $('#checkAll').on('change', function() {
            var isChecked = $(this).is(':checked');

            // Set all row checkboxes to the same state
            $('.account-checkbox').prop('checked', isChecked);
        });

        // If any row checkbox is unchecked, uncheck "Check All"
        $('.account-checkbox').on('change', function() {
            if (!$('.account-checkbox').is(':checked')) {
                $('#checkAll').prop('checked', false);
            }
        });

        // Show the form modal when "Add New" is clicked
            $('#importAccountsBtn').click(function() {
                $('#addFacebookAccountModal').modal('show');
            });

        // Submit form via AJAX
            $('#submitAccountsBtn').click(function() {
                let accountsData = {
                    bulk_data: $('#bulk_data').val()
                };

                $.ajax({
                    url: '/facebook/accounts/bulk_add',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(accountsData),
                    success: function(response) {
                        $('#addFacebookAccountModal').modal('hide');

                    }
                });
            });

});

//    // Show the form modal when "Add New" is clicked
//            $('#importAccountsBtn').click(function() {
//                $('#addFacebookAccountModal').modal('show');
//            });
//
//        // Submit form via AJAX
//            $('#submitAccountsBtn').click(function() {
//                let accountsData = {
//                    bulk_data: $('#bulk_data').val()
//                };
//
//                $.ajax({
//                    url: '/facebook/accounts/bulk_add',
//                    type: 'POST',
//                    contentType: 'application/json',
//                    data: JSON.stringify(accountsData),
//                    success: function(response) {
//                        $('#addFacebookAccountModal').modal('hide');
//
//                    }
//                });
//            });
//
//
//
//
//
//    document.getElementById('search').addEventListener('keyup', function() {
//    // Get the search input value
//    const searchValue = this.value.toLowerCase();
//
//    // Get all table rows
//    const rows = document.querySelectorAll('table tbody tr');
//
//    rows.forEach(row => {
//      // Get the Page Name column (assuming it's the third column, index 2)
//      const pageNameCell = row.cells[4];
//
//      if (pageNameCell) {
//        const pageName = pageNameCell.textContent.toLowerCase();
//
//        // Show row if the Page Name matches the search value, otherwise hide it
//        if (pageName.includes(searchValue)) {
//          row.style.display = '';
//        } else {
//          row.style.display = 'none';
//        }
//      }
//    });
//
//
//
//
//
//
//    // Toggle password visibility
//    $('.toggle-password').on('click', function () {
//
//        var mask = $(this).siblings('.password-mask');
//        var originalValue = $(this).data('value');
//
//        if (mask.text() === '****') {
//            mask.text(originalValue);  // Show password
//            $(this).removeClass('fa-eye').addClass('fa-eye-slash');  // Change icon
//        } else {
//            mask.text('****');  // Hide password
//            $(this).removeClass('fa-eye-slash').addClass('fa-eye');  // Change icon
//        }
//    });
//
//    // Toggle 2FA visibility
//    $('.toggle-twofa').on('click', function () {
//        var mask = $(this).siblings('.twofa-mask');
//        var originalValue = $(this).data('value');
//
//        if (mask.text() === '****') {
//            mask.text(originalValue);  // Show 2FA
//            $(this).removeClass('fa-eye').addClass('fa-eye-slash');  // Change icon
//        } else {
//            mask.text('****');  // Hide 2FA
//            $(this).removeClass('fa-eye-slash').addClass('fa-eye');  // Change icon
//        }
//    });