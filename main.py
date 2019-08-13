import requests
import json
import csv

import pymysql
import re
import os.path


def main():
    print("========== Starting ==========")
    cfg = read_config()
    db = pymysql.connect(cfg["SQL Server IP"], cfg["SQL username"], cfg["SQL Password"], "curse_analytics")
    cursor = db.cursor()
    r = get(cfg, "https://authors.curseforge.com/dashboard/projects?filter-games=&filter-project-status=4")
    text = r.text
    for group in re.findall("<a.*href=\"/dashboard/project/(.*)\"><span>Download</span></a>", text):
        print(group)
        got = get(cfg, "https://authors.curseforge.com/dashboard/project/" + group)
        for row in csv.DictReader(got.text.splitlines(), delimiter=','):
            cursor.execute("select statDate, projectId from stats where statDate=STR_TO_DATE(\"{}\", '%Y-%m-%d') and projectId={}".format(row["Date"], row["Project ID"]))
            if cursor.rowcount == 0:
                cursor.execute("insert into stats values(STR_TO_DATE(\"{}\", '%Y-%m-%d'), {}, \"{}\",{},{},{},{},{},{})".format(row["Date"], row["Project ID"], row["Name"], row["Points"], row["Historical Download"], row["Daily Download"], row["Daily Unique Download"], row["Daily Twitch App Download"], row["Daily Curse Forge Download"]))
                db.commit()
    print("============ Done ============")


def read_config():
    if not os.path.isfile("config.json"):
        print("=== Generating Config File ===")
        with open('config.json', 'w') as f:
            json.dump({"SQL Server IP": "127.0.0.1", "SQL username": "username", "SQL Password": "password", "Cobalt Session": "session"}, f)
            print(" Please edit config and retry ")
            exit(0)
    with open('config.json') as config_file:
        return json.load(config_file)


def get(cfg, url):
    return requests.get(url, headers={
        "referer": "https://authors.curseforge.com/store/transactions",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }, cookies={
        "CobaltSession": cfg["Cobalt Session"],
    })


if __name__ == '__main__':
    main()
