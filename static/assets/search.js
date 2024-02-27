function searchText() {
    var searchInput = document.getElementById('searchInput').value.toLowerCase();
    var content = document.getElementById('content').getElementsByTagName('p');
    var searchResults = document.getElementById('searchResults');
    searchResults.innerHTML = '';

    for (var i = 0; i < content.length; i++) {
        var text = content[i].textContent.toLowerCase();
        if (text.includes(searchInput)) {
            var result = document.createElement('p');
            result.innerHTML = content[i].innerHTML.replace(new RegExp(searchInput, 'gi'), '<span class="highlight">$&</span>');
            searchResults.appendChild(result);
        }
    }

    if (searchResults.innerHTML === '') {
        var noResults = document.createElement('p');
        noResults.textContent = 'No matching results found.';
        searchResults.appendChild(noResults);
    }
}
