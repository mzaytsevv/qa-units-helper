import os
import sys
import csv

from jira import JIRA

jira_url = "https://gigster-network.atlassian.net/"

incoming_header_field_to_nest = {
    'Issue Type': ['issuetype', 'name'],
    'Project key': ['project', 'key'],
    #'Priority': ['priority', 'name'],
}

incoming_header_field_not_nest = {
    'Summary': 'summary',
    'Description': 'description',
    'Custom field (TestRail Link)': 'customfield_10063',
}

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


def validate_e2e_file(data):
    if len(data) > 0:
        return True
    return False


def e2e_tickets(data):
    tickets = []
    for line in data:
        line_json = {}
        num_column = 0
        links = []
        for incoming_header in headers:
            if incoming_header in incoming_header_field_to_nest:
                outgoing_header = incoming_header_field_to_nest[incoming_header][0]
                nested_key = incoming_header_field_to_nest[incoming_header][1]
                outgoing_value = line[num_column]
                line_json[outgoing_header] = {nested_key: outgoing_value}
            elif incoming_header in incoming_header_field_not_nest:
                outgoing_header = incoming_header_field_not_nest[incoming_header]
                outgoing_value = line[num_column]
                line_json[outgoing_header] = outgoing_value
            elif incoming_header == "Outward issue link (Tests)":
                outgoing_value = line[num_column]
                print(f" outgoing_value: {outgoing_value}, num_column= {num_column}")
                if outgoing_value != "":
                    links.append(outgoing_value)
            num_column = num_column + 1
        line_with_links = [line_json, links]
        tickets.append(line_with_links)
    return tickets


def create_tickets_and_links(tickets_with_links):
    for ticket_with_links in tickets_with_links:
        try:
            ticket = ticket_with_links[0]
            #issue_created = jira.create_issue(fields=ticket)
            #print(f"{issue_created.key}")
            print(f"============== new ticket")
            try:
                tickets_to_link = ticket_with_links[1]
                for ticket_to_link in tickets_to_link:
                    ticket_to_link = ticket_to_link.strip()
                    #issue_link = jira.create_issue_link(type='tests', inwardIssue=issue_created.key,
                    #                                    outwardIssue=ticket_to_link)
                    print(f"\t'tests' -> {ticket_to_link}")
            except Exception as e:
                print(f"Error while linking the issue '{issue_created.key}' to '{ticket_to_link}'. \n\tException: {e}")
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
                    if validate_e2e_file(headers):
                        print("Got E2E CSV")
                        ticket_json_with_links = e2e_tickets(data)
                        create_tickets_and_links(ticket_json_with_links)
                    else:
                        print("CSV has not E2E format")
                else:
                    print(f"Empty file: {csv_file_name}")
        except Exception as e:
            print(f"Csv file reading error. Provide the path to it as an argument. Exception: {e}")
