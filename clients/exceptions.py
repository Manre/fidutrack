class BaseException(Exception):
    def __init__(self, message: str, additional_info: dict = None):
        super().__init__(message)
        self.additional_info = additional_info


class CouldNotConnectException(BaseException):
    pass


class ClientException(BaseException):
    pass


class ServerException(BaseException):
    pass


class InvalidJSONException(BaseException):
    pass
