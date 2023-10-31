import json
import os
from datetime import datetime
import requests

# There is literally no error checking anywhere here...
# I wrote this kinda quickly...

countikstub = "https://countik.com/api/userinfo"

def getuserdata(userid, sec_uid):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    }
    countikurl = countikstub + "?sec_user_id=" + sec_uid
    response = requests.get(url=f'{countikurl}',
                             headers=headers)
    userobject = json.loads(response.text)
    thetimestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    return userobject

def loadusers():
    f = open('compare.json')
    users = json.load(f)
    return users

def procuser(userobj):
    userobject = getuserdata(userobj["userid"], userobj["sec_uid"])
    useroutput = {}
    useroutput["name"] = userobj["name"]
    useroutput["followerCount"] = userobject["followerCount"]
    return useroutput

def getuserstats():
    users = loadusers()
    result1 = procuser(users[0])
    result2 = procuser(users[1])
    diff1 = int(result1["followerCount"]) - int(result2["followerCount"])
    comment1 = ""
    comment2 = ""
    if diff1 > 0:
        comment1 = f'({diff1} more than {result2["name"]})'

    diff2 = int(result2["followerCount"]) - int(result1["followerCount"])
    if diff2 > 0:
        comment2 = f'({diff2} more than {result1["name"]})'
    slackmsg = f'{result1["name"]} {result1["followerCount"]} {comment1}\n'
    slackmsg += f'{result2["name"]} {result2["followerCount"]} {comment2}'
    return slackmsg

def main():
    slackmsg = getuserstats()
    slack_key = os.getenv("slack_key")
    slack_webhook_stub = "https://hooks.slack.com/services/"
    slack_webhook_url = slack_webhook_stub + slack_key
    result = requests.post(
        slack_webhook_url,
        data='{"text": "' + slackmsg + '"}')
    print(slackmsg)


if __name__ == '__main__':
    main()
