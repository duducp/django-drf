class ChallengeProductException(Exception):
    pass


class ChallengeProductTimeoutException(ChallengeProductException):
    pass


class ChallengeProductNotFoundException(ChallengeProductException):
    pass


class ChallengeProductClientException(ChallengeProductException):
    def __init__(
        self,
        message='',
        status_code=None,
        response=None,
        payload=None
    ):
        self.status_code = status_code
        self.response = response
        self.payload = payload
        self.message = message

    def __repr__(self):
        return self.message
