# TorBreaker
CyberSage is World's 1st AI Security Engineer aka Ethical Hacker which aims to reduce time b/w Vulnerability Detection & Mitigation

## Download Project
```
git clone https://github.com/jatin009v/TorBreaker
```

## Features
- [x] Detects the `Technologies Used` & there `Version` in Target
- [x] Detects `All WAF (Web Application Firewall)`
- [x] Conducts `Rigourous Fingerprinting`
- [x] Conducts `Complete Active & Passive Recon`
- [x] Conducts `Rigourous Web Vulnerability Scanning`
- [x] Finds the Vulnerability in `Code Base` using Deep Learning Model 
- [x] Detects `CVE (Common Vulnerabilities and Exposures) Vulnerabilities`
- [x] `Exploits` the `Vulnerability` for `Reducing False Positive` Result
- [x] `Generates` the `Vulnerability Report`
- [x] `Automatic Code Fixer` for `Mitigating Vulnerability`

## Install Dependencies
```
cd Installer
chmod +x Installer.sh
sudo ./Installer.sh
```

## Install & Run Django Web Application
```
sudo apt install redis-server nginx python3-pip -y
sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo service redis-server status 

cd ../CyberSage
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt 
python3 manage.py runserver
```

## Terminal - 2
```
source venv/bin/activate
celery -A CyberSage.celery worker -l info --pool=eventlet
```

## Database Setup for Production Server
```
sudo -u postgres psql
CREATE DATABASE cybersage_db;
CREATE USER cybersage_admin WITH PASSWORD 'Admin#@123';
ALTER ROLE cybersage_admin SET client_encoding TO 'utf8';
ALTER ROLE cybersage_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE cybersage_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cybersage_db TO cybersage_admin;
\q
```

## Django creds
- Username: admin
- Email: jatingupta009v@gmail.com
- Password: Admin@123

## Rules for Creating Vulnerability Scanning Pipelines
- [X] Pipelines should contain linux commands
- [X] If you want to perform some task on GET parameters, then you can use `get_params.txt` file in the command, backend will automatically adjust the actual `get_params.txt` path dynamically
```
# e.g.
$ cat get_params.txt | grep "file=" > lfi.txt 
``` 
- [X] Similary for POST parameters, use `post_params.txt` in your pipeline cmd, these two files contains the URL containing GET & POST URLs
- [X] Result file should be named as `get_$PIPELINE_NAME_results.txt` e.g. `get_sqli_results.txt` for GET params
- [X] Similary for POST params, the result file name should be `post_$PIPELINE_NAME_results.txt` e.g. `post_sqli_results.txt`
- [X] Result file format which backend is expecting 
```
GET SQLI|http://testphp.vulnweb.com/artists.php?artist=1|Payload|'
```
- [X] Separated By `|` sign 
- [X] First string should be `Vulnerability Name` e.g. `GET SQLI`
- [X] Second string should be `URL` e.g. `http://testphp.vulnweb.com/artists.php?artist=1`
- [X] Third string should be `Payload` as it is 
- [X] Fourth string should be `Actual Payload Value` e.g. `'`

## Resources for creating Pipelines
- [One Liner](https://github.com/0xPugal/One-Liners)
