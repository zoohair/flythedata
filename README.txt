# Installation, Requirements, etc.

In a nutshell:
- Requires python3 to run the code
- For visualization requires plotly/Dash 

## Installing python and dependencies

Python can be messy especially if you need to manage different versions (2.7, 3+, etc.)
Some people recommend virtualenv or anaconda. I'll just assume that this is something
you already have, know how to do, or can google. The gist is that you need:
- python3
- pip3 (package installer for python libraries/tools)
- the packages listed in requirements.txt

If you're on Mac, easiest thing to do is to get Homebrew then do:
```
brew install python3 
pip3 install -r requirements.txt
```

# Running

To run the server, just launch the ./run.py script.
To view the site, go to http://localhost:3000

# Deploying

It is possible to deploy this to heroku. see ./deploy.sh