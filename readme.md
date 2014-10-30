## Hi!

### Basics

1. `pip install -r requirements.txt`
2. `brew install phantomjs`
3. update the settings in *config_sample.py* then rename the file to *config.py* (make sure you keep this file out of version control since it conatins sensitive information)
4. fire away!

You may need to update you security settings -> https://www.google.com/settings/security/lesssecureapps

### Chron

**Start**

1. Make executable: `chmod +x run.sh`
2. Run: `crontab crontab.txt`

**Is it running?**

1. `crontab -l`

**Stop**

1. `crontab -r`
