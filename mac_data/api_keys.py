from ConfigParser import SafeConfigParser


def get_api_key(key_file, service):
    # type: (file, str) -> str
    """Read the service API key from the config file

    :rtype: str
    :param key_file: the api keys file object
    :param service: the service name
    :return: api_key
    """
    parser = SafeConfigParser()
    parser.readfp(key_file)
    return parser.get(service, 'api_key')
