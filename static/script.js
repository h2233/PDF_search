$(document).ready(function() {
  // When the search form is submitted
  $('#search-form').submit(function(event) {
    // Prevent the form from submitting normally
    event.preventDefault();

    // Get the search query from the input field
    var query = $('#search-input').val();

    // Send an AJAX request to the backend with the search query
    $.ajax({
      url: 'http://127.0.0.1:5000/search',
      type: 'GET',
      data: {'search_str': query},
      success: function(data) {
        alert('搜索成功 <!.!> ');
        // Display the search results
        alert('返回结果'+data['data'].length+'条');
        parent = document.getElementById("parent")
        parent.innerHTML=''
        for(var i = data['data'].length-1; i >= 0; i--){
          var search_results = document.createElement("div");
          var download_link = document.createElement("a");
          search_results.innerHTML=data['data'][i];
          download_link.innerHTML='results-link'
          download_link.href="/download/" + data['data'][i]
          parent.appendChild(search_results);
          parent.appendChild(download_link);
          // search_results.html(data['data'][i]);
          // download_link.html('<a href="/download/' + data['data'] + '">Download results</a>');
        }
        // $('#search-results').html(data['data'][0]);
        // // Show the download link
        // $('#download-link').html('<a href="/download/' + data['data'] + '">Download results</a>');
        // $('#download-link').show();
      },
      error: function() {
        // Display an error message if the request fails
        alert('失败 <!.!> ')
        $('#search-results').html('An error occurred while searching.');
      }
    });
  });
});