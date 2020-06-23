# Contributing to GameReqsAPI

Welcome!<br>
Everyone is welcome to contribute to this project, whether you just want to have a go at API development, you have
something to add to the scraper, or you simply like Python and Flask.

##Getting started

If you're new to Git and Github, this is a [good place to start](https://guides.github.com/activities/hello-world/).

In order to contribute, you should fork this repo by clicking the 
**Fork button** <img src="https://user-images.githubusercontent.com/17777237/54873012-40fa5b00-4dd6-11e9-98e0-cc436426c720.png" height="14"/>
in the top right corner. Then, clone with `git clone` the fork to get a local copy.

When you have a fork and start working on an issue, remember to [keep your fork synced with the upstream
repository](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).

After you've cloned locally your fork, you can start to contribute. If you want to make an important change,
you're encouraged to create a new branch. Keep tabs on [the issues section](https://github.com/Plutone11011/GameReqsAPI/issues)
for things to work on, or feel free to open new issues yourself if you think there is something that needs to be fixed or improved.

##The environment

Once you have a local copy, there are a few steps before you can test the API.<br>
You need to first create a `.flaskenv` file inside the project directory (same level as api package)
where you're going to define 2 environment variables, which will be automatically set
once you install python-dotenv.
Thus, the file must contain the following variables:
```
FLASK_ENV=development
FLASK_APP=api/__init__.py
```
Then, you need to [create a virtualenv](https://docs.python.org/3/library/venv.html). <br>
After you've created it, you need to activate it. <br>
On Linux, the command is usually `source venv/bin/activate` <br>
On Windows, it's usually `venv\Scripts\activate.bat` <br>
However, do refer again to the link for virtual environment creation for special cases.

Once you're set with virtualenv, you need to finally install dependencies with `pip install -r requirements.txt`.
This will also install python-dotenv.

To run the flask server and start testing the API, use `flask run`. <br>
There are 2 other CLI commands:
* `flask init-db` creates the database file, should not be used unless you end up with the 
.sqlite file removed. The file is already tracked by git however, so it shouldn't be a problem.
* `flask init-scraper` starts scraping steam for data, parses it and inserts it in the database. Again, since sqlite is already
 populated, it shouldn't be used unless you empty the database somehow. Do remember that, in case, the scraper does take
 a few hours to scrape every app page in steam (about 100K).
 
 ## Making changes
 When you're sure you resolved an issue, [make a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
 I'll be sure to review it.