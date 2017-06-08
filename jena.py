import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
from common.globalconst import *
from more_itertools import unique_everseen


def convert_to_dataframe(cols, records):
    rec_list = []
    for record in records:
        data_dict = {}
        for col in cols:
            data_dict.update({NAME_MAPPING[col]: record[col]['value']})
        rec_list.append(data_dict)
    pd.set_option('display.max_colwidth', 60)
    df = pd.DataFrame(rec_list)
    columns = df.columns
    df = df[sorted(columns, reverse=True)]
    return df


def get_filter_clauses(type, filter):
    filter_clauses = []
    for field in filter[type]:
        if filter[type][field] != "":
            if FILTER_MAP[str(field)] == 'regex':
                tokens = map(lambda x: x.strip(), str(filter[type][field]).split(','))
                reg_list = [REGEX_QUERY.format(var=str(field), val=str(token)) for token in tokens]
                regex_query = '&&'.join(reg_list)
                filter_clauses.append(FILTER_CALUSE.format(query=regex_query))
            elif FILTER_MAP[str(field)] == '>=':
                greater_equal_query = GREATER_EQUAL_QUERY.format(var=str(field), val=float(filter[type][field]))
                filter_clauses.append(FILTER_CALUSE.format(query=greater_equal_query))
            elif FILTER_MAP[str(field)] == 'range' and filter[type][str(field)]['start'] != '' and \
                            filter[type][str(field)]['end'] != '':
                start = int(filter[type][field]['start'])
                end = int(filter[type][field]['end'])
                range_query = RANGE_QUERY.format(var=field, start=start, end=end)
                filter_clauses.append(FILTER_CALUSE.format(query=range_query))
    return filter_clauses


def get_where_clauses(vars, onto_dict):
    where_clauses = []
    for node2_a in vars:
        indirection1 = INDIRECTIONS.get(node2_a, None)
        node1_a = indirection1[0]
        if node1_a:
            indirection2 = INDIRECTIONS.get(node1_a, None)
            if indirection2:
                if indirection2[1] == 'f':
                    node2_b = node1_a
                    node1_b = indirection2[0]
                    node = node2_b
                else:
                    node2_b = indirection2[0]
                    node1_b = node1_a
                    node = node1_b
                props = ''
                for key, value in onto_dict.get(node, {}).items():
                    props = props + ' ' + key + ':' + value
                where_clauses.append('?{node1} {props} ?{node2}.'.format(node1=node1_b, props=props, node2=node2_b))
            props = ''
            for key, value in onto_dict.get(node2_a, {}).items():
                props = props + ' ' + key + ':' + value
            where_clauses.append('?{node1} {props} ?{node2}.'.format(node1=node1_a, props=props, node2=node2_a))
    return list(unique_everseen(where_clauses))


def query_builder(select, filter):
    # Building SELECT and WHERE clause
    movie_vars = [str(key) for key in select.get('movie') if select.get('movie')[key]]
    book_vars = [str(key) for key in select.get('book') if select.get('book')[key]]
    select_clause = ' '.join(map(lambda x: '?' + x, movie_vars) + map(lambda x: '?' + x, book_vars))
    movie_vars_filter = [str(key) for key in filter['movie']]
    book_vars_filter = [str(key) for key in filter['book']]
    movie_vars += movie_vars_filter
    book_vars += book_vars_filter
    where_clauses = []
    where_clauses += get_where_clauses(movie_vars, MOVIE_ONTO_DICT)
    where_clauses += get_where_clauses(book_vars, BOOK_ONTO_DICT)
    if book_vars:
        where_clauses.insert(0, BOOK_CLAUSE)
    if movie_vars:
        where_clauses.insert(0, MOVIE_CLAUSE)
    if movie_vars and book_vars and BOOK_MOVIE_CLAUSE not in where_clauses:
        where_clauses.append(BOOK_MOVIE_CLAUSE)
    where_clauses = ''.join(where_clauses)

    # Building FILTER clause
    filter_clauses = []
    filter_clauses += get_filter_clauses('movie', filter)
    filter_clauses += get_filter_clauses('book', filter)
    filter_clauses = ' '.join(filter_clauses)
    clauses = '.'.join([where_clauses, filter_clauses])
    query = QUERY.format(select_vars=select_clause, clauses=clauses)
    print query
    return query


def query_decorator(func):
    def func_wrapper(*args, **kwargs):
        query = query_builder(kwargs.pop('select'), kwargs.pop('filter'))
        sparql = SPARQLWrapper(sparql_endpoint)
        kwargs.update({'service': sparql,
                       'query': query})
        return func(*args, **kwargs)

    return func_wrapper


@query_decorator
def query_apache_jena(*args, **kwargs):
    try:
        service = kwargs.pop('service')
        query = kwargs.pop('query')
        service.setQuery(query)
        service.setReturnFormat(JSON)
        results = service.query().convert()
        df = convert_to_dataframe(results['head']['vars'], results['results']['bindings'])
        return df.to_html(), INT_OK
    except Exception as e:
        print 'Error in querying Apache Jena', e
    return None, INT_QUERY_FAILURE
