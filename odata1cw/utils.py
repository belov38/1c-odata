def make_url_part(name, value, value_type):
    if value == None:
        return ''
    if type(value) != value_type:
        raise ValueError('{}={} must be {}'.format(
            name, value, value_type))
    result = "&${}={}".format(name, value)
    return result
