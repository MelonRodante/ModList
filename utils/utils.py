import sys


class Utils:

    @staticmethod
    def print_exception(method, exception):
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line_number = exception_traceback.tb_lineno

        print(method + str(exception) + ' [' + str(line_number) + ']')
