# Archived due to the analytics files no longer being served.

# CurseForge Stats

### What does this do?

What this script does is downloads the analytic CSV files that CurseForge provides on this page https://authors.curseforge.com/dashboard/projects.

The data from those CSV files are then inserted into a MySQL / MariaDB database (See db.sql).

That Data can then be read using Grafana (See grafana-dash.json for a prebuilt dashboard).

### How do I use this?

First install the python requirements:

```
Python3.7 (may work on older versions)

pip install -r requirements.txt
```

The import the SQL database from db.sql.

You're going to need your Curse Cobalt Session, which you can get from your cookies on any CurseForge page (I personally use https://authors.curseforge.com/dashboard/projects as this is where the project data is read from).

Don't share your Cobalt session with anyone!

Edit config.json (If you don't have this file, you can simply run the python file to generate it for you) with your SQL server details and your Cobalt session

(Optional - Import the Grafana dashboard using grafana-dash.json)

Run the program and wait for it to finish

the curse CSV files update daily, but I have no idea at what time, I would suggest setting up a cron job to run the script daily at any time that suits you.
