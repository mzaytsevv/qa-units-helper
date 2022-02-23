import os
import sys
import csv

from jira import JIRA

jira_url = "https://gigster-network.atlassian.net/"


def get_jira():
    jira_email = os.getenv("JIRA_EMAIL")
    if jira_email is None:
        print("JIRA_EMAIL env var is not set")
    jira_api_token = os.getenv("JIRA_API_TOKEN")
    if jira_api_token is None:
        print("JIRA_API_TOKEN env var is not set")
    try:
        jira = JIRA(jira_url, basic_auth=(jira_email, jira_api_token))
        return jira
    except Exception:
        print(f"Couldn't build JIRA client\n")
    return None


def validate_ett_file(data):
    if len(data) > 0:
        headers = data[0]
        if len(headers) > 0:
            if headers[0] != "Assignee":
                print("1st column has to be Assignee")
                return False
            if headers[1] != "Issue Type":
                print("2nd column has to be Issue Type")
                return False
            if headers[2] != "Summary":
                print("3rd column has to be Summary")
                return False
            if headers[3] != "Description":
                print("4th column has to be Description")
                return False
            if headers[4] != "Test Execution Link":
                print("5th column has to be Test Execution Link")
                return False
            if headers[5] != "Auto Execution Result":
                print("6th column has to be Auto Execution Result")
                return False
            if headers[6] != "Manual Execution Result":
                print("7th column has to be Auto Manual Execution Result")
                return False
            if headers[7] != "Project Key":
                print("8th column has to be Project Key")
                return False
    return True


def validate_ett_file(data):
    if len(data) > 0:
        if len(headers) > 0:
            if headers[0] != "Assignee":
                return False
            if headers[1] != "Issue Type":
                return False
            if headers[2] != "Summary":
                return False
            if headers[3] != "Description":
                return False
            if headers[4] != "Test Execution Link":
                return False
            if headers[5] != "Auto Execution Result":
                return False
            if headers[6] != "Manual Execution Result":
                return False
            if headers[7] != "Project Key":
                return False
    return True


def validate_wtt_file(data):
    if len(data) > 0:
        if len(headers) > 0:
            if headers[0] != "Assignee":
                return False
            if headers[1] != "Issue Type":
                return False
            if headers[2] != "Summary":
                return False
            if headers[3] != "Description":
                return False
            if headers[4] != "E2E Link":
                return False
            if headers[5] != "TestRail Link":
                return False
            if headers[6] != "Project Key":
                return False
    return True


def ett_tickets(data):
    tickets = []
    for line in data:
        tickets.append({
            'assignee': {'id': line[0]},
            'issuetype': {'name': line[1]},
            'summary': line[2],
            'description': line[3],
            'customfield_10064': line[4],
            'customfield_10073': {'value': line[5]},
            'customfield_10074': {'value': line[6]},
            'project': {'key': line[7]}
        })
    return tickets


def wtt_tickets(data):
    tickets = []
    for line in data:
        tickets.append({
            'assignee': {'id': line[0]},
            'issuetype': {'name': line[1]},
            'summary': line[2],
            'description': line[3],
            'customfield_10062': line[4],
            'customfield_10063': line[5],
            'project': {'key': line[6]}
        })
    return tickets


def create_tickets(tickets):
    for ticket in tickets:
        try:
            issue_created = jira.create_issue(fields=ticket)
            print(f"{issue_created.key}")
        except Exception as e:
            print(f"Error while creating the issue: {ticket}. Exception: {e}")


if __name__ == "__main__":
    jira = get_jira()
    if jira:
        data = []
        tickets = []
        try:
            argv = sys.argv[1:]
            csv_file_name = argv[0]
            with open(csv_file_name, newline='\n') as f:
                reader = csv.reader(f)
                csv = list(reader)
                headers = csv[0]
                data = csv[1:]
                if len(data) > 0:
                    if validate_ett_file(headers):
                        print("Got ETT CSV")
                        create_tickets(ett_tickets(data))
                    elif validate_wtt_file(headers):
                        print("Got WTT CSV")
                        create_tickets(wtt_tickets(data))
                    else:
                        print("CSV has neither ETT nor WTT format")
                else:
                    print(f"Empty file: {csv_file_name}")
        except Exception as e:
            print(f"Csv file reading error. Provide the path to it as an argument. Exception: {e}")
