def validate_len(name, leng):
    try:
        assert len(name) <= leng
    except AssertionError:
        print(f'{name} must be less than {leng} characters!')
    else:
        return name


def t(x):
    x = 'me'
    print(x)


t('ere')
