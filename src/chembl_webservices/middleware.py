
import re
from django.db import connection

from django.conf import settings

words_re = re.compile( r'\s+' )

class SqlPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed.  This is only useful for debugging.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response
        super(SqlPrintingMiddleware, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    sql_format_regex = re.compile(r'\b(select|from|where|group|having|order)\b', re.IGNORECASE)
    sql_indent_format_regex = re.compile(r'(,(?!\s:arg)|\bjoin\b|\bor\b|\band\b)', re.IGNORECASE)
    sql_identifiers_format_regex = re.compile(r'IN\s+\(\s*(?:[^\s]+\s*,\s*)+[^\s]+\s*\)', re.IGNORECASE)
    def process_response(self, request, response):
        indentation = 2
        if len(connection.queries) > 0 and settings.DEBUG:
            total_time = 0.0
            for query in connection.queries:
                sql_parts = query['sql'].split("' - PARAMS = ")
                sql_string = sql_parts[0].replace("QUERY = u'", '')
                identifier_matches = SqlPrintingMiddleware.sql_identifiers_format_regex.findall(sql_string)

                for id_match_i in identifier_matches:
                    ids_i = id_match_i.split(',')
                    num_ids = len(ids_i)
                    hidden_ids = 10
                    if num_ids > hidden_ids:
                        sql_string = sql_string.replace(
                            id_match_i,
                            '{0} . . . <<{1} ID\'s hidden>>)'.format('<;>'.join(ids_i[:hidden_ids]), num_ids-hidden_ids)
                        )
                    else:
                        sql_string = sql_string.replace(
                            id_match_i,
                            '<;>'.join(ids_i)
                        )

                sql_string = SqlPrintingMiddleware.sql_format_regex.sub('\n\\1', sql_string)
                sql_string = SqlPrintingMiddleware.sql_indent_format_regex.sub('\\1\n    ', sql_string)
                sql_string = sql_string.replace('<;>', ',')
                print("QUERY TIME: %s secs" % query['time'])
                print('QUERY:' + sql_string + '\n')
                if len(sql_parts) > 1:
                    print('PARAMS:\n' + sql_parts[1] + '\n')
                total_time = total_time + float(query['time'])

            replace_tuple = (" "*indentation, str(total_time))
            print("%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple)

        return response