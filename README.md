# qa-units-helper
This is the util for mass creation of QA units. Will be especially helpful for ETTs creation in the case we don't have
them created automatically.

**Input:** CSV file with unit data. Each row == new ticket. ETT and WTT template has strict structure that has to be exactly
the same as in the example template files

**Output:** the list of JIRA tickets keys created

**Prerequisites:** requires 2 env vars to be set before running the script:
 - `JIRA_EMAIL` - the email of the JIRA user tickets will be created from. Use your own
 - `JIRA_API_TOKEN` - the auth token of that user. Create it here https://id.atlassian.com/manage-profile/security/api-tokens

**How to set env vars:**
Linux \ Mac: 
```
export JIRA_EMAIL=maxim.zaytsev@gigster.com
```
Windows: 
```
set JIRA_EMAIL=maxim.zaytsev@gigster.com
```
Note: it is set only in the current terminal session 

**How to run: **
```
python create_wu.py path_to_csv_file
```

Example: 
```
python create_wu.py ./qa_wu_import_template_ett.csv
```


**The full list of actions:**
 - [one time] create a token in https://id.atlassian.com/manage-profile/security/api-tokens and save it
 - [one time] clone the repo to a folder on your machine
 - open the console (For Linux or Mac use the default is fine, for Windows use some latest consoles like Powershel)
 - set 2 env vars
 - prepare \ edit the csv by cloning this template https://docs.google.com/spreadsheets/d/1gixHXOhBbZlO_67xAp-yYglPhX5zPjLdL_zAwul93Jw/edit#gid=0
 - run the script
