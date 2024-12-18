from urllib.parse import quote_plus


def reformat_pwd(connection_string):
    end = connection_string.rfind('@')
    start = [pos for pos, char in enumerate(connection_string) if char == ':'][1] + 1
    pwd = connection_string[start:end]
    new_pwd = quote_plus(pwd)
    return connection_string[0:start] + new_pwd + connection_string[end:len(connection_string) ]