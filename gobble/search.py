"""Search for users and package inside the ElasticSearch database"""


from gobble.api import search_packages, handle

SEARCH_KEYS = ['q', 'size', 'title', 'author', 'description',
               'regionCode', 'countryCode', 'cityCode']


def search(query, user=None, size=None):
    """Query the ElasticSearch database.

    You can search a package by `title`, `author`, `description`, `regionCode`,
    `countryCode` or`cityCode`. You can match all these fields at once with the
    magic `q` key.

    If authentication-token was provided, then private packages from the
    authenticated user will also be included. Otherwise, only public packages
    will be returned. You can limit the size of your results with the `size`
    parameter.

    :param query: a `dict` of key value pairs
    :param user: an authenticated user
    :param size: the number of results returned

    :type query: "class:`dict`
    :rtype user: :class:`gobble.user.User'
    :rtype size: :class:`int'

    :return: a dictionary with the results
    :rtype: :class: `dict`
    """
    _validate(query)

    if size:
        query.update(size=size)

    quoted_query = _sanitize(query)

    if user:
        quoted_query.update(jwt=user.token)

    response = search_packages(params=quoted_query)
    return handle(response)


def _sanitize(query):
    keys = ['package.' + str(k) for k in query.keys()]
    values = ['"' + str(v) + '"' for v in query.values()]
    return dict(zip(keys, values))


def _validate(query):
    for key in query.keys():
        if key not in SEARCH_KEYS:
            msg = 'Invalid search key "{key}" for package'
            raise ValueError(msg.format(key=key))
