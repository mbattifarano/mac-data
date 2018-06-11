from mac_data import api_keys


def test_get_api_key(file_object):
    expected_api_key = "the_api_key"
    s = '\n'.join([
        "[the_service_name]",
        "api_key = %s" % expected_api_key
    ])
    file_object.write(s)
    file_object.seek(0)
    actual_api_key = api_keys.get_api_key(file_object, "the_service_name")
    assert actual_api_key == expected_api_key
