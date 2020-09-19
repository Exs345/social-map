from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

TOKEN_URL = 'https://consent.swisscom.com/o/oauth2/token'

client_id = 'uFdtRJaDao6ATC2kW4WPLCkm2Ywb3Cjg'
client_secret = '98wsTlX4ou7n1CrD'

# See https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html#backend-application-flow.
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

# Fetch an access token.
oauth.fetch_token(token_url=TOKEN_URL, client_id=client_id, client_secret=client_secret)
print(oauth.access_token)

# Use the access token to query an endpoint.
resp = oauth.get(
    'https://api.swisscom.com/layer/heatmaps/standard/grids/postal-code-areas/8050',
    headers={'scs-version': '2'})
print(resp.json())