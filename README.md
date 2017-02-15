### Project Euler Streak Maker
> The purpose of this _bot_ is to help me achieve a streak on Github as I get to work on programming problems from [Project Euler](https://projecteuler.net/archives). The solutions repo it updates is [this one.](https://github.com/musale/euler-problems-python)

### Set up
The project is written in `Python`. The executable file is the `run.py`
#### Getting Started
* clone this repo
* run `pip install -r requirements.txt` to get the dependencies.
* create a `.env` file and fill it with your variables for `GITHUB_USERNAME`
  > We need a Github `token` to enable us to make authenticated calls so generate one from [here](https://help.github.com/articles/creating-an-access-token-for-command-line-use/)
* update your `.env` file with your `GITHUB_TOKEN`
    > Next we need to create a repo which will house the Euler problems that this bot will be creating. You can choose to use the same repo but:

  1. You can't have a streak from forks
  2. I don't want your commits (delete the `.git` folder in this after cloning. Push to your own repo now :wink:)
* Create a new repo on Github. Now update your `.env` `GITHUB_REPO` to be this repo
* If you deleted the `.git` folder, initialize this repo now to track your files.
* run `python run.py`
* check the repo you created on Github if it has a new file `001.py`. That's it.

#### Cron?
I created a cron to run this once a day

`streak.sh`
```
#!/bin/bash
cd /projects/project-euler-streak
/usr/bin/python run.py
```
And then I fed it into `crontab -e`

`0 14 * * * /projects/project-euler-streak/streak.sh`

You can pretty much use any scheduling tools you like

### Credits
Coming up with this project, I had some handy libraries and resources online that really made my work easy.
* [Euler Python Library](https://github.com/iKevinY/EulerPy) - helped me get the Euler problems by running the `euler` command. Nifty and handy!
* [Github API V3](https://developer.github.com/v3) - good stuff. More examples please :sob:
* [mdswanson.com](http://mdswanson.com/blog/2011/07/23/digging-around-the-github-api-take-2.html)
* [Levi Botelho's Coding Blog](http://www.levibotelho.com/development/commit-a-file-with-the-github-api)
* [Harlantwood's](https://gist.github.com/harlantwood/2935203) Ruby gist - I actually understood from this. :clap: :clap:
* All you fine people answering questions on SO! Seriously, great stuff!!!
