import os
import time
from slackclient import SlackClient
from ibm_term import termSearch

# starterbot's ID as an environment variable
BOT_NAME = os.environ.get('BOT_NAME')
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

# constants
TERM_COMMAND="term"
LIST_COMMAND="list"

## Start up
def get_bot_id():
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        #Retrieve all users to determine bot name
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '"+user['name']+"'is "+user.get('id'))
                return user.get('id')
    else:
        return None

## Handling Slack Input
def handle_command(command, channel):
    """
    Recieves command directed at the bot and determines how to processs it.
    """
    response = "Not sure what you mean. Please use "+LIST_COMMAND+" command to list all commands."
    if command.startswith(TERM_COMMAND):
        ## Get user input
        userInput=command[5:]
        ## response = ibm_term_function(input value)
        response = termSearch(userInput)
    if command.startswith(LIST_COMMAND):
	##List all Commands
        response = "Current Commands are: \n term [arg] - Define a term."
    slack_client.api_call("chat.postMessage",channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
    Parses message, returns none unless message is directed at bot based on the BOT_ID.
    """
    output_list=slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                #return text after the @ mention after stripping whitespace
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading
    BOT_ID=get_bot_id()
    if BOT_ID!=None:
        global AT_BOT
        AT_BOT="<@"+BOT_ID+">"
        if slack_client.rtm_connect():
            print(BOT_NAME+" connected and running!")
            while True:
                command, channel = parse_slack_output (slack_client.rtm_read())
                if command and channel:
                    handle_command(command, channel)
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID.")
    else:
        print("Could not find bot user with name "+BOT_NAME)

