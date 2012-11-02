from __future__ import unicode_literals

import re

from oauth2app.models import Client, AccessToken, AccessRange
from oauth2app.oauth2_token import TimestampGenerator


absolute_custom_url_re = re.compile(r"^[A-Z_0-9]*://", re.I)

def create_access_token(client_name, user, scope='universal', expiration=None):
    """ Creates an access token for a user using the app specified by client_name 
    
        Args:
            client_name - the name of the client app that you are creating an access token for
            user - the user object you are creating a token for
            scope - the scope of the token
            expiration - the number of seconds the token is good for. If None, the default
                         expiration is used
    """
    client = Client.objects.filter(name=client_name).order_by('id')[0]
    # Use the Client key to generate an access token for the user
    access_range = AccessRange.objects.get(key=scope)
    access_token = AccessToken.objects.create(user=user, client=client)
    access_token.scope.add(access_range)
    if expiration:
        access_token.expire = TimestampGenerator(expiration)()
        access_token.save()
    return access_token
