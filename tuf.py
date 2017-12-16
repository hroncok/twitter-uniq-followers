import os
import requests

# tracebacks if not set ¯\_(ツ)_/¯
# get it from https://apps.twitter.com/app/new
# or ask @hroncok to run the script
API_KEY = os.environ['API_KEY']
API_SECRET = os.environ['API_SECRET']

ACCOUNTS = ['pyvec', 'napyvo', 'pyladiescz', 'pyconcz']

OAUTH_URL = 'https://api.twitter.com/oauth2/token'
FOLLOWERS_URL = 'https://api.twitter.com/1.1/followers/ids.json'


def twitter_session(api_key=API_KEY, api_secret=API_SECRET):
    """
    From http://naucse.python.cz/lessons/intro/requests/
    """
    session = requests.Session()

    r = session.post(OAUTH_URL, auth=(api_key, api_secret),
                     data={'grant_type': 'client_credentials'})

    bearer_token = r.json()['access_token']

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req

    session.auth = bearer_auth
    return session


def get_followers(session, account, cursor=-1):
    """
    https://developer.twitter.com/en/docs/accounts-and-users/
       follow-search-get-users/api-reference/get-followers-ids
    """
    r = session.get(FOLLOWERS_URL,
                    params={'screen_name': account, 'cursor': cursor})
    r.raise_for_status()
    data = r.json()
    ids = set(data['ids'])
    next_cursor = data['next_cursor']
    if next_cursor:
        ids |= get_followers(session, account, cursor=next_cursor)
    return ids


if __name__ == '__main__':
    session = twitter_session()
    ids = set()
    for account in ACCOUNTS:
        account_ids = get_followers(session, account)
        print(f'{account}: {len(account_ids)} followers')
        ids |= account_ids
    print(f'\ntotal: {len(ids)} uniq followers')
