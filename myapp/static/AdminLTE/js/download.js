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


document.getElementById('pasteLinkDownload').addEventListener('click', function() {
            $('#downloadVideoModal').modal('show');

                // Paste clipboard content into the Video Links field-->
                navigator.clipboard.readText().then(text => {
                  document.getElementById('videoLinks').value = text;
                }).catch(err => {
                  console.error('Failed to read clipboard contents: ', err);
                });
        });

        function scrapeVideoInfo(url, index) {
            fetch('/scrape_video_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: url})
            })
            .then(response => response.json())
            .then(data => {
                let tableBody = document.querySelector('#videoTable tbody');
                let newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td><input type='checkbox' class="row-checkbox" data-url=${url} data-title=${data.title}></td>
                    <td>${index}</td>
                    <td><i class="far fa-folder"></i> Movies</td>
                    <td><i class="fab fa-tiktok"></i> TikTok</td>
                    <td>${data.title}</td>
                    <td>${data.size}</td>
                    <td>${data.duration}</td>
                    <td><a href="">${url}</a></td>
                    <td><span class="status"></span></td>
                    <td>Content Movies</td>
                `;
                tableBody.appendChild(newRow);
            })
            .catch(err => {
                console.error('Error fetching video info:', err);
            });
        }

        document.getElementById('startDownloadBtn').addEventListener('click', function() {
            $('#downloadVideoModal').modal('hide');
            let urls = document.getElementById('videoLinks').value.split('\n');

                urls.forEach((url, index) => {
                    if (url.trim() !== '') {
                        scrapeVideoInfo(url, index + 1);
                    }
            });

            let rows = document.querySelectorAll('#videoTable tbody tr');
            rows.forEach(row => {
                let url = row.children[2].innerText;

                startDownload(url, row);
            });
        });

        function startDownload(url, row) {
            fetch('/download_video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: url})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    row.children[3].innerText = 'Completed';
                } else {
                    row.children[3].innerText = 'Failed';
                }
            });
        }

$('#startDownloadButton').on('click', function() {

            // Collect selected videos
            $('.row-checkbox:checked').each(function() {
                const videoUrl = $(this).data('url');
                const videoTitle = $(this).data('title');
                const statusCell = $(this).closest('tr').find('.status');

                // Update status to 'Downloading'
                 statusCell.removeClass('badge badge-success badge-danger').addClass('badge badge-info').text('Downloading');

                // Send AJAX request to download video
                $.ajax({
                    url: '/download',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        video_url: videoUrl,
                        title: videoTitle
                    }),
                    success: function(response) {
                        if (response.status === 'success') {
                            statusCell.removeClass('badge-info').addClass('badge-success').text('Completed');
                        } else {
                            statusCell.removeClass('badge-info').addClass('badge-danger').text('Failed');
                        }
                    },
                    error: function() {
                        statusCell.removeClass('badge-info').addClass('badge-danger').text('Error');
                    }
                });
            });
        });



// When the "Check All" checkbox is clicked
        $('#checkAll').on('change', function() {
            var isChecked = $(this).is(':checked');

            // Set all row checkboxes to the same state
            $('.row-checkbox').prop('checked', isChecked);
        });

        // If any row checkbox is unchecked, uncheck "Check All"
        $('.row-checkbox').on('change', function() {
            if (!$('.video-checkbox').is(':checked')) {
                $('#checkAll').prop('checked', false);
            }
        });

});
