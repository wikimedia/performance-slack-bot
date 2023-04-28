import unittest
from slackbot.bot import app
from unittest.mock import patch


class TestPerformanceBot(unittest.TestCase):
    @patch('slackbot.bot.client.chat_postMessage')
    def setUp(self, mock_chat_post_message):
        self.app = app.test_client()

    # @patch.dict('os.environ', {'SLACK_TOKEN': 'xoxb-2155697888-5163828972065-HDqQWUuOweImEE1taClKl7hj',
    #                            'SIGNING_SECRET': 'ab1cac0b86e804508c7b7786433d768f'})
    @patch('slackbot.bot.process_test')
    @patch('slackbot.bot.client.chat_postMessage')
    def test_performance_bot_with_valid_data(self, mock_chat_post_message, mock_process_test):
        mock_chat_post_message.return_value = {'ok': True}

        data = {
            "channel_id": "CIO98432",
            "text": "https://www.example.com",
            "user_id": 1,

        }

        expected_result = {
            "response_type": "in_channel",
            "text": "You requested for:https://www.example.com, your test is running"
        }

        response = self.app.post('/performance-bot', data=data)
        self.assertEqual(response.status_code, 200)
        mock_process_test.assert_called_once()
        mock_chat_post_message.assert_called_once_with(
            channel='CIO98432',
            response_type='in_channel',
            text=expected_result['text'].strip()  # Strip whitespace characters
        )


if __name__ == "__main__":
    unittest.main()
