def validate_len(name, leng):
    try:
        assert len(name) <= leng
    except AssertionError:
        print(f"{name} must be less than {leng} characters!")
        return None
    else:
        return name


def validate_type(name, dtype):
    try:
        assert type(name) == dtype
    except AssertionError:
        print(f"{name} must be of type {dtype}")
        return None
    else:
        return dtype
