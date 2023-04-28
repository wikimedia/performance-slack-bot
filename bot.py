import subprocess
import slack
import os
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
from pathlib import Path
from dotenv import load_dotenv
import json
import threading
import logging


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
api_key = os.environ['API_KEY']
host = os.environ['HOST']
addCommand = [
    "sitespeed.io",
    "--api.hostname",
    host,
    "--api.key",
    api_key,
    "--api.location",
    "wmfcloud",
    "--api.port",
    "443",
    "--api.json",
    "true",
    "--api.testType",
    "emulatedMobile",
    "--api.action",
    "add"
]

getCommand = [
    "sitespeed.io",
    "--api.hostname",
    host,
    "--api.key",
    api_key,
    "--api.location",
    "wmfcloud",
    "--api.port",
    "443",
    "--api.json",
    "true",
    "--api.action",
    "get",
    "--api.id",
]
logging.basicConfig(
    filename='output.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def run_command(command):
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def send_test(user_id):
    test_stdout = run_command(addCommand).stdout
    test_stderr = run_command(addCommand).stderr

    if test_stderr:
        logging.error(f'Error: {test_stderr}')

    if test_stdout:
        result = test_stdout
        getCommand.append(result)

    # check if the Job is completed
    while True:
        get_stdout = run_command(getCommand).stdout
        get_stderr = run_command(getCommand).stderr

        if get_stderr:
            logging.error(f'Error: {get_stderr}')

        result_json = json.loads(get_stdout)

        if result_json.get('status') == 'completed':
            test_result_url = result_json.get('result')
            break

    # send test result back to the user
    message = {
        'channel': user_id,
        'text': test_result_url
    }

    client.chat_postMessage(**message)


@app.route('/performance-bot', methods=['POST'])
def performance_bot():
    data = request.form
    print(data)
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    param = data.get('text')
    params = param.split()

    for i in params:
        addCommand.append(i)

    threading.Thread(target=send_test,
                     args=(user_id,)).start()

    # notify user test is running
    response_message = {
            'response_type': 'in_channel',
            'text': f'''You requested for:{data.get('text')}, your test is running'''}

    client.chat_postMessage(
        channel=channel_id, **response_message)
    return response_message, 200


if __name__ == "__main__":
    app.run(debug=True)
