document.addEventListener('DOMContentLoaded', function() {
    // Define the searchText function
    function searchText() {
        var searchInput = document.getElementById('searchInput');
        if (!searchInput) {
            console.error('Input element with ID "searchInput" not found.');
            return;
        }
        var searchValue = searchInput.value.toLowerCase();
        var content = document.getElementById('content').getElementsByTagName('p');
        var searchResults = document.getElementById('searchResults');
        searchResults.innerHTML = '';

        for (var i = 0; i < content.length; i++) {
            var text = content[i].textContent.toLowerCase();

            if (text.includes(searchValue)) {
                var result = document.createElement('p');
                result.innerHTML = content[i].innerHTML.replace(new RegExp(searchValue, 'gi'), '<span class="highlight">$&</span>');
                searchResults.appendChild(result);
            }
        }

        if (searchResults.innerHTML === '') {
            var noResults = document.createElement('p');
            noResults.textContent = 'No matching results found.';
            searchResults.appendChild(noResults);
        }
    }

    // Attach searchText function to the search button click event
    var searchButton = document.getElementById('searchButton');
    if (searchButton) {
        searchButton.addEventListener('click', searchText);
    } else {
        console.error('Button element with ID "searchButton" not found.');
    }
});
