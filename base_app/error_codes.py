from typing import Union


class ApplicationErrorException(Exception):

    def __init__(self, error_code_message: Union[dict, str], original_exception: Exception = None):
        if type(error_code_message) == dict:
            self.http_message = error_code_message
        elif type(error_code_message) == str:
            self.http_message = {'message': error_code_message}
        super().__init__(error_code_message)
        self.originalException = original_exception

    def __str__(self):
        return super().__str__()
