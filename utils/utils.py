import sys


class Utils:

    @staticmethod
    def print_exception(method, exception):
        try:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_number = exception_traceback.tb_lineno

            print(method + ': ' + str(exception.__cause__) + ' [' + str(line_number) + ']')

        except Exception as e:
            Utils.print_exception('UTILS print_exception', e)

    @staticmethod
    def query_exec(q, method):
        try:
            result = q.exec()
            if not result:
                print('QUERY ' + method + ': ' + q.lastError().text())
            return result

        except Exception as e:
            Utils.print_exception('UTILS query_exec', e)