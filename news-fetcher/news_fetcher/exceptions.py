class NewsFetcherException(Exception):
    pass


class NewsFetcherFetchingException(NewsFetcherException):
    pass


class NewsFetcherConsumerException(NewsFetcherException):
    pass
