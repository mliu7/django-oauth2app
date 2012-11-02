from __future__ import unicode_literals


"""OAuth 2.0 Django Models"""


import time
from hashlib import sha512
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from oauth2app.consts import CLIENT_KEY_LENGTH, CLIENT_SECRET_LENGTH
from oauth2app.consts import ACCESS_TOKEN_LENGTH, REFRESH_TOKEN_LENGTH
from oauth2app.consts import ACCESS_TOKEN_EXPIRATION, MAC_KEY_LENGTH, REFRESHABLE
from oauth2app.consts import CODE_KEY_LENGTH, CODE_EXPIRATION
from oauth2app.forms import CustomURLFormField
from oauth2app.validators import CustomURLValidator
from south.modelsinspector import add_introspection_rules

from trackable_object.models import TrackableObject


add_introspection_rules([], ["^oauth2app\.models\.CustomURLField"])


class TimestampGenerator(object):
    """Callable Timestamp Generator that returns a UNIX time integer.
    
    **Kwargs:**
    
    * *seconds:* A integer indicating how many seconds in the future the
      timestamp should be. *Default 0*
    
    *Returns int*
    """
    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds


class KeyGenerator(object):
    """Callable Key Generator that returns a random keystring.
    
    **Args:**
    
    * *length:* A integer indicating how long the key should be.
    
    *Returns str*
    """
    def __init__(self, length):
        self.length = length
    
    def __call__(self):
        return sha512(uuid4().hex).hexdigest()[0:self.length]


class CustomURLField(models.URLField):
    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 200)
        models.CharField.__init__(self, verbose_name, name, **kwargs)
        self.validators.append(CustomURLValidator())

    def formfield(self, **kwargs):
        # As with CharField, this will cause URL validation to be performed
        # twice.
        defaults = {
            'form_class': CustomURLFormField,
        }
        defaults.update(kwargs)
        return super(models.URLField, self).formfield(**defaults)


class Client(TrackableObject):
    """Stores client authentication data.
    
    **Args:**
    
    * *name:* A string representing the client name.
    * *user:* A django.contrib.auth.models.User object representing the client
       owner.
    
    **Kwargs:**
    
    * *description:* A string representing the client description. 
      *Default None*
    * *key:* A string representing the client key. *Default 30 character 
      random string*    
    * *secret:* A string representing the client secret. *Default 30 character
      random string*
    * *redirect_uri:* A string representing the client redirect_uri. 
      *Default None*
      
    """
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User)
    description = models.TextField(null=True, blank=True)    
    website = models.URLField(blank=True, max_length=256, verify_exists=False)
    key = models.CharField(
        max_length=CLIENT_KEY_LENGTH, 
        default=KeyGenerator(CLIENT_KEY_LENGTH),
        db_index=True)
    secret = models.CharField(
        max_length=CLIENT_SECRET_LENGTH, 
        default=KeyGenerator(CLIENT_SECRET_LENGTH))
    redirect_uri = CustomURLField(null=True, blank=True, verbose_name="Redirect URI",
                                  help_text=("This is a full URL on your domain that Leaguevine will "
                                             "redirect to after a user logs in using one of the two User "
                                             "Login OAuth 2 flows. If you intend for users to log into your app, "
                                             "this field is required."))

    # Printing
    def __unicode__(self):
        return self.name

    # URLs
    def get_url_kwargs(self):
        return {'app_id': self.id}

    @models.permalink
    def get_absolute_url(self):
        return ('app_detail', (), self.get_url_kwargs())

    @models.permalink
    def get_absolute_edit_url(self):
        return ('app_edit', (), self.get_url_kwargs())

    @models.permalink
    def get_absolute_remove_url(self):
        return ('app_remove', (), self.get_url_kwargs())


class AccessRange(models.Model):
    """Stores access range data, also known as scope.
    
    **Args:**
    
    * *key:* A string representing the access range scope. Used in access 
      token requests.
    
    **Kwargs:**
    
    * *description:* A string representing the access range description. 
      *Default None*   
    
    """
    key = models.CharField(unique=True, max_length=255, db_index=True) 
    description = models.TextField(blank=True)


class AccessToken(models.Model):
    """Stores access token data.

    **Args:**
    
    * *client:* A oauth2app.models.Client object
    * *user:* A django.contrib.auth.models.User object    
    
    **Kwargs:**
    
    * *token:* A string representing the access key token. *Default 10 
      character random string*
    * *refresh_token:* A string representing the access key token. *Default 10 
      character random string*
    * *mac_key:* A string representing the MAC key. *Default None*
    * *expire:* A positive integer timestamp representing the access token's 
      expiration time.
    * *scope:* A list of oauth2app.models.AccessRange objects. *Default None* 
    * *refreshable:* A boolean that indicates whether this access token is
      refreshable. *Default False*   
         
    """
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    token = models.CharField(
        unique=True,
        max_length=ACCESS_TOKEN_LENGTH, 
        default=KeyGenerator(ACCESS_TOKEN_LENGTH),
        db_index=True)
    refresh_token = models.CharField(
        unique=True, 
        blank=True, 
        null=True, 
        max_length=REFRESH_TOKEN_LENGTH, 
        default=KeyGenerator(REFRESH_TOKEN_LENGTH),
        db_index=True)
    mac_key = models.CharField(
        unique=True, 
        blank=True, 
        null=True, 
        max_length=MAC_KEY_LENGTH, 
        default=None)
    issue = models.PositiveIntegerField(
        editable=False, 
        default=TimestampGenerator())
    expire = models.PositiveIntegerField(
        default=TimestampGenerator(ACCESS_TOKEN_EXPIRATION))
    scope = models.ManyToManyField(AccessRange)
    refreshable = models.BooleanField(default=REFRESHABLE)


class Code(models.Model):
    """Stores authorization code data.
    
    **Args:**
    
    * *client:* A oauth2app.models.Client object
    * *user:* A django.contrib.auth.models.User object
    
    **Kwargs:**
    
    * *key:* A string representing the authorization code. *Default 30 
      character random string*
    * *expire:* A positive integer timestamp representing the access token's 
      expiration time.
    * *redirect_uri:* A string representing the redirect_uri provided by the 
      requesting client when the code was issued. *Default None*
    * *scope:* A list of oauth2app.models.AccessRange objects. *Default None* 
    
    """
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    key = models.CharField(
        unique=True, 
        max_length=CODE_KEY_LENGTH, 
        default=KeyGenerator(CODE_KEY_LENGTH),
        db_index=True)
    issue = models.PositiveIntegerField(
        editable=False, 
        default=TimestampGenerator())
    expire = models.PositiveIntegerField(
        default=TimestampGenerator(CODE_EXPIRATION))
    redirect_uri = models.URLField(null=True, blank=True)
    scope = models.ManyToManyField(AccessRange)
    

class MACNonce(models.Model):
    """Stores Nonce strings for use with MAC Authentication.

    **Args:**
    
    * *access_token:* A oauth2app.models.AccessToken object
    * *nonce:* A unique nonce string.
    
    """
    access_token = models.ForeignKey(AccessToken)
    nonce = models.CharField(max_length=30, db_index=True)
