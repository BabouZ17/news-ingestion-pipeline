class NewsFetcherException(Exception):
    pass


class NewsFetcherFetchingException(NewsFetcherException):
    pass


class NewsFetcherParsingException(NewsFetcherException):
    pass
