from ConfigParser import SafeConfigParser


def get_api_key(key_file, service):
    parser = SafeConfigParser()
    parser.readfp(key_file)
    return parser.get(service, 'api_key')
