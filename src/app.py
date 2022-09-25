import os
import praw
import res


client_id = "TABHEXnT9tFNKe05iyUpSA"
redirect_uri = "termux-reddit-client://auth"
scopes = "edit,identity,read,save,submit,vote,wikiread"
token_url_raw = "https://www.reddit.com/api/v1/authorize.compact?duration=permanent&client_id=" + client_id + \
                "&response_type=code&state={state}&redirect_uri="+redirect_uri+"&scope="+scopes

user_agent = "android:Termux Client for Reddit:1.0.0 (by /u/tsanderdev)"

token = res.auth_data()
if token is not None:
    reddit = praw.Reddit(redirect_uri=redirect_uri, user_agent=user_agent, client_secret="", client_id=client_id, refresh_token=token)
else:
    reddit = praw.Reddit(redirect_uri=redirect_uri, user_agent=user_agent, client_secret="", client_id=client_id)


def token_url(state: str):
    return token_url_raw.format(state=state)


def gen_state():
    res = ""
    allowed = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while len(res) < 100:
        rand = os.urandom(1)[0]
        res += allowed[rand % len(allowed)]
    return res



