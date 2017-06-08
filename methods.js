function upload(form) {
    var request = Object();
    var formData = new FormData();
    request.select = Object();
    request.filter = Object();
    request.select.movie = Object();
    request.select.book = Object();

    request.select.movie.movieTitle = form.elements['Movie Name'].checked;
    request.select.movie.castname = form.elements['Movie Cast'].checked;
    request.select.movie.dirname = form.elements['Movie Director'].checked;
    request.select.movie.movieGenre = form.elements['Movie Genres'].checked;
    request.select.movie.movielang = form.elements['Movie Languages'].checked;
    request.select.movie.movieRating = form.elements['Movie Rating'].checked;
    request.select.movie.releaseYear = form.elements['Movie Release Year'].checked;
    request.select.movie.runtime = form.elements['Movie Runtime'].checked;
    request.select.movie.famousAwards = form.elements['Movie Famous Awards'].checked;
    request.select.movie.otherAwards = form.elements['Movie Other Awards'].checked;
    request.select.movie.writername = form.elements['Movie Writers'].checked;

    request.select.book.bookTitle = form.elements['Book Title'].checked;
    request.select.book.authorname = form.elements['Book Author'].checked;
    request.select.book.pubname = form.elements['Book Publisher'].checked;
    request.select.book.bookRating = form.elements['Book Rating'].checked;
    request.select.book.pubYear = form.elements['Book Publishing Year'].checked;
    request.select.book.booklang = form.elements['Book Language'].checked;
    request.select.book.bookpages = form.elements['Book Pages'].checked;
    request.select.book.bookGenre = form.elements['Book Genre'].checked;

    request.filter.movie = Object();
    request.filter.book = Object();
    request.filter.movie.movieTitle = form.elements['movieTitle'].value;
    request.filter.movie.castname = form.elements['castname'].value;
    request.filter.movie.dirname = form.elements['dirname'].value;
    request.filter.movie.movieGenre = form.elements['movieGenre'].value;
    request.filter.movie.movielang = form.elements['movielang'].value;
    request.filter.movie.movieRating = form.elements['movieRating'].value;
    request.filter.movie.releaseYear = Object();
    request.filter.movie.releaseYear.start = form.elements['releaseYear'].value;
    request.filter.movie.releaseYear.end = form.elements['releaseyearend'].value;
    request.filter.movie.famousAwards = form.elements['famousAwards'].value;
    request.filter.movie.otherAwards = form.elements['otherAwards'].value;
    request.filter.movie.writername = form.elements['writername'].value;
    request.filter.book.authorname = form.elements['authorname'].value;
    request.filter.book.pubname = form.elements['pubname'].value;
    request.filter.book.pubYear = form.elements['pubYear'].value;
    request.filter.book.booklang = form.elements['booklang'].value;
    request.filter.book.bookGenre = form.elements['bookGenre'].value;
    request.filter.book.bookRating = form.elements['bookRating'].value;
    request.filter.book.bookTitle = form.elements['bookTitle'].value;
    formData.append('data', JSON.stringify({'request': request}));

    $.ajax({
        url: '/query',
        data: formData,
        processData: false,
        contentType: false,
        type: 'POST',
        beforeSend: function (msg) {
            document.getElementById("table-display").style.display = 'none';
            document.getElementById("table-container").style.display = 'none';
            document.getElementById("loader-display").style.display = 'block';
        },
        success: function (data) {
            if (data['code'] == 0) {
                document.getElementById("loader-display").style.display = 'none';
                document.getElementById("table-container").style.display = 'block';
                document.getElementById("table-display").style.display = 'block';
                var div = document.getElementById('table-display');
                div.innerHTML = (data['result'])
            }
            else {
                alert('Error in fetching data from RDF')
            }

        },
        error: function () {
            alert('Error in Ajax call');
        }
    });

    return false;
}