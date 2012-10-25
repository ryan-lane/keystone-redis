
from base64 import b64encode
from base64 import b64decode

def revoked():
    return 'revoked'

def token(token_id):
    return 'token {0}'.format(token_id)

def usertoken(user_id, token_id):
    if token_id == '*':
        return 'usertoken {0} *'.format(b64encode(user_id))
    else:
        return 'usertoken {0} {1}'.format(b64encode(user_id), token_id)

def parse_token(key):
    t, token_b64 = key.split(' ', 1)
    if t != 'token':
        raise ValueError('Expected token key: '+key)
    return b64decode(token_b64)

def parse_usertoken(key):
    t, user_b64, token = key.split(' ', 2)
    if t != 'usertoken':
        raise ValueError('Expected usertoken key: '+key)
    return b64decode(user_b64), token

# vim:et:fdm=marker:sts=4:sw=4:ts=4
