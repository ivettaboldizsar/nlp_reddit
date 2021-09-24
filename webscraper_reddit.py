import requests
import pandas as pd
from datetime import datetime


def redditData():
    def df_from_response(res):
        # initializing dataframe
        df = pd.DataFrame()

        # loop through each post from response and append to df
        for post in res.json()['data']['children']:
            df = df.append({
                'subreddit': post['data']['subreddit'],
                'title': post['data']['title'],
                'selftext': post['data']['selftext'],
                'upvote_ratio': post['data']['upvote_ratio'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'score': post['data']['score'],
                'link_flair_css_class': post['data']['link_flair_css_class'],
                'created_utc': datetime.fromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'id': post['data']['id'],
                'kind': post['kind']
            }, ignore_index=True)

        return df

    # --------------------------------------------------------------------------------------------------------------
    auth = requests.auth.HTTPBasicAuth('GA0Tj0doJn7lLQ', 'BuCHHjX9xWI6wtfCyPSZey3odrzpiA')

    # username and password
    data = {'grant_type': 'password',
            'username': '',
            'password': ''}
    headers = {'User-Agent': 'MyAppBot01'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    # add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # while the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    # -------------------------------------------------------------------------------------------------------------
    # WallStreetBets
    # -------------------------------------------------------------------------------------------------------------
    # initialize parameters
    data_wsb = pd.DataFrame()
    params = {'limit': '100'}
    # --------------------------------------------------------------------------------------------------------------
    try:
        for i in range(10):
            # make request
            res = requests.get("https://oauth.reddit.com/r/wallstreetbets/new",
                               headers=headers,
                               params=params)
            print(i)
            # get dataframe from response
            new_df = df_from_response(res)
            row = new_df.head()
            # create fullname
            fullname = row['kind'] + '_' + row['id']
            # add/update fullname in params
            params['after'] = fullname

            # append new_df to data
            data_wsb = data_wsb.append(new_df, ignore_index=True)
    except:
        print("Limit number has been reached")
    # -------------------------------------------------------------------------------------------------------------
    # StockMarket
    # --------------------------------------------------------------------------------------------------------------
    # initialize parameters
    data_sm = pd.DataFrame()
    params = {'limit': '100'}
    # --------------------------------------------------------------------------------------------------------------
    try:
        for i in range(10):
            # make request
            res = requests.get("https://oauth.reddit.com/r/StockMarket/new",
                               headers=headers,
                               params=params)
            print(i)
            # get dataframe from response
            new_df = df_from_response(res)
            row = new_df.head()
            # create fullname
            fullname = row['kind'] + '_' + row['id']
            # add/update fullname in params
            params['after'] = fullname

            # append new_df to data
            data_sm = data_sm.append(new_df, ignore_index=True)
    except:
        print("Limit number has been reached")

    # return results
    return data_wsb, data_sm


def save(date):
    data_wsb, data_sm = redditData()
    data_wsb.to_csv('C:/Users/LENOVO/Documents/Python/RedditData/reddit_wallstreetbets'+date+'.csv', header=True, index=False)
    data_sm.to_csv('C:/Users/LENOVO/Documents/Python/RedditData/reddit_stockmarket'+date+'.csv', header=True, index=False)
    print('Data Saved')


save(str(datetime.today().date()))
