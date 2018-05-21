from mac_data import api_keys


def test_get_api_key(file_object):
    s = '\n'.join([
        "[the_service_name]",
        "api_key = the_api_key"
    ])
    file_object.write(s)
    file_object.seek(0)
    assert api_keys.get_api_key(file_object, "the_service_name") == "the_api_key"
