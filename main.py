from merge_data import MergeData
from dotenv import load_dotenv
import os

load_dotenv()


def main(userId, pwd, gCred):
    google_token_file = 'google_calendar/creds/g_calendar_token.json'
    google_token_file = gCred

    merge_data = MergeData(google_token_file, userId, pwd)
    merge_data.run()


if __name__ == '__main__':
    main('111', '222')