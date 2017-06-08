'''
Error Codes
'''
INT_OK = 0
INT_QUERY_FAILURE = -1000
INT_ERROR = -2000

'''
End points
'''
sparql_endpoint = 'http://localhost:3030/CSCI586/query'

'''
Query Template
'''
QUERY = 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>' \
        'PREFIX ont:<http://www.semanticweb.org/dnaid/ontologies/2017/2/csci586_group6#>' \
        'SELECT {select_vars} WHERE {{{clauses}}}'\


MOVIE_CLAUSE = '?movie rdf:type ont:Movie.'
BOOK_CLAUSE = '?book rdf:type ont:Book.'
BOOK_MOVIE_CLAUSE = '?movie ont:adaptedFrom ?book'

'''
Movie Ontologies
{property : ontology}
'''
MOVIE_CLASS = 'Movie'
MOVIE_ONTO_DICT = {'movieTitle': {'ont': 'movieTitle'},
                   'director': {'ont': 'directedBy'},
                   'dirname': {'ont': 'name'},
                   'cast': {'ont': 'actedIn'},
                   'castname': {'ont': 'name'},
                   'releaseYear': {'ont': 'releaseYear'},
                   'mlang': {'ont': 'madeIn'},
                   'movielang': {'ont': 'language'},
                   'movieRating': {'ont': 'movieRating'},
                   'runtime': {'ont': 'runtime'},
                   'writer' : {'ont' : 'movieWrittenBy'},
                   'writername': {'ont': 'name'},
                   'otherAwards' : {'ont' : 'awardName'},
                   'famousAwards' : {'ont' : 'awardName'},
                   'oawards' : {'ont' : 'hasWonOtherAwards'},
                   'fawards' : {'ont' : 'hasWonFamousAwards'},
                   'movieGenre' : {'ont' : 'genreName'},
                   'mgenre' : {'ont' : 'hasMovieGenre'}
                   }

'''
Book Ontologies
'''
BOOK_CLASS = 'Book'
BOOK_ONTO_DICT = {
    'bookTitle': {'ont': 'bookTitle'},
    'author': {'ont': 'bookWrittenBy'},
    'authorname': {'ont': 'name'},
    'pubname': {'ont': 'name'},
    'publisher': {'ont': 'publishedBy'},
    'bookRating': {'ont': 'bookRating'},
    'pubYear': {'ont': 'publishYear'},
    'blang': {'ont': 'writtenIn'},
    'booklang': {'ont': 'language'},
    'bookpages': {'ont': 'numberOfPages'},
    'book' : {'ont' : 'adaptedFrom'},
    'bookGenre' : {'ont' : 'genreName'},
    'bgenre' : {'ont' : 'hasBookGenre'},
}

'''
Indirections
'''
INDIRECTIONS = {'movieTitle': ['movie', 'f'],
                'director': ['movie', 'f'],
                'dirname': ['director', 'f'],
                'castname': ['cast', 'f'],
                'cast': ['movie', 'r'],
                'writer': ['movie', 'f'],
                'writername': ['writer', 'f'],
                'releaseYear': ['movie', 'f'],
                'mlang': ['movie', 'f'],
                'movielang': ['mlang', 'f'],
                'mgenre': ['movie', 'f'],
                'movieGenre': ['mgenre', 'f'],
                'fawards': ['movie', 'f'],
                'famousAwards': ['fawards', 'f'],
                'otherAwards' : ['oawards', 'f'],
                'oawards' : ['movie', 'f'],
                'movieRating': ['movie', 'f'],
                'runtime': ['movie', 'f'],
                'bookTitle': ['book', 'f'],
                'book': ['movie', 'f'],
                'author': ['book', 'f'],
                'authorname': ['author', 'f'],
                'publisher': ['book', 'f'],
                'pubname': ['publisher', 'f'],
                'bookRating': ['book', 'f'],
                'pubYear': ['book', 'f'],
                'blang': ['book', 'f'],
                'booklang': ['blang', 'f'],
                'bookpages': ['book', 'f'],
                'bookGenre' : ['bgenre', 'f'],
                'bgenre' : ['book','f'],

                }

'''
Column to name mapping
'''
NAME_MAPPING = {'movieTitle' : 'Movie Name',
                'castname' : 'Movie Cast',
                'dirname' : 'Movie Director',
                'movieGenre' : 'Movie Genre',
                'movielang' : 'Movie Languages',
                'movieRating' : 'Movie Rating (out of 10)',
                'releaseYear' : 'Movie Release Year',
                'runtime' : 'Movie Runtime',
                'famousAwards' : 'Movie Famous Awards',
                'otherAwards' : 'Movie Other Awards',
                'writername' : 'Movie Writers',
                'bookTitle' : 'Book Title',
                'authorname' : 'Book Author',
                'pubname' : 'Book Publisher',
                'bookRating' : 'Book Rating (out of 5)',
                'pubYear' : 'Book Publish Year',
                'booklang' : 'Book Language',
                'bookpages' : 'Book Pages',
                'bookGenre' : 'Book Genre'
                }


'''
Filtering Fields
'''
FILTER_CALUSE = 'FILTER({query})'
REGEX_QUERY = 'regex(?{var},"{val}","i")'
GREATER_EQUAL_QUERY = '?{var}>={val}'
RANGE_QUERY = '?{var}>={start} && ?{var}<={end}'
FILTER_MAP = {'movieTitle' : 'regex',
              'castname' : 'regex',
              'dirname' : 'regex',
              'movieGenre' : 'regex',
              'movielang' : 'regex',
              'releaseYear' : 'range',
              'famousAwards' : 'regex',
              'otherAwards' : 'regex',
              'writername' : 'regex',
              'bookTitle' : 'regex',
              'authorname' : 'regex',
              'pubname' : 'regex',
              'bookRating' : '>=',
              'pubYear' : '>=',
              'booklang' : 'regex',
              'bookGenre' : 'regex',
              'movieRating' : '>='}
