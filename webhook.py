import smtplib
import urllib.request
import urllib.parse
import json
import base64
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import userInfo

# The URL root for accessing Google Accounts.
GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'

user = "lincoln.tran@gmail.com"
recievers = ['lincoln.tran@gmail.com']

def sendImage(messageText, image_name, image_data):
   image_data = open("./" + image_name + ".jpg", "rb").read()

   message = MIMEMultipart()
   message['Subject'] = "Unknown person in room"
   message['From'] = "lincoln.tran@gmail.com"
   message['To'] = "lincoln.tran@gmail.com"
   image = MIMEImage(image_data, name=image_name)
   text = MIMEText(messageText, 'plain')
   message.attach(text)
   message.attach(image)

   access_token = RefreshToken(userInfo.client_id, userInfo.client_secret, userInfo.refresh_token)
   auth_string = GenerateOAuth2String(user, access_token['access_token'])

   server = smtplib.SMTP('smtp.gmail.com', 587)
   # server.set_debuglevel(True)
   server.ehlo()
   server.starttls()
   server.docmd('AUTH', 'XOAUTH2 ' + auth_string.decode("utf-8"))
   server.sendmail(user, recievers, message.as_string())
   server.close()

def RefreshToken(client_id, client_secret, refresh_token):
  """Obtains a new token given a refresh token.

  See https://developers.google.com/accounts/docs/OAuth2InstalledApp#refresh

  Args:
    client_id: Client ID obtained by registering your app.
    client_secret: Client secret obtained by registering your app.
    refresh_token: A previously-obtained refresh token.
  Returns:
    The decoded response from the Google Accounts server, as a dict. Expected
    fields include 'access_token', 'expires_in', and 'refresh_token'.
  """
  params = {}
  params['client_id'] = client_id
  params['client_secret'] = client_secret
  params['refresh_token'] = refresh_token
  params['grant_type'] = 'refresh_token'
  request_url = AccountsUrl('o/oauth2/token')

  response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode("utf-8")).read()
  return json.loads(response.decode("utf-8"))

def GenerateOAuth2String(username, access_token, base64_encode=True):
  """Generates an IMAP OAuth2 authentication string.

  See https://developers.google.com/google-apps/gmail/oauth2_overview

  Args:
    username: the username (email address) of the account to authenticate
    access_token: An OAuth2 access token.
    base64_encode: Whether to base64-encode the output.

  Returns:
    The SASL argument for the OAuth2 mechanism.
  """
  auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
  if base64_encode:
    auth_string = base64.b64encode(auth_string.encode("utf-8"))
  return auth_string

def AccountsUrl(command):
  """Generates the Google Accounts URL.

  Args:
    command: The command to execute.

  Returns:
    A URL for the given command.
  """
  return '%s/%s' % (GOOGLE_ACCOUNTS_BASE_URL, command)