from merge_data import MergeData
from dotenv import load_dotenv
import os

load_dotenv()


def main(userId, pwd):
    google_token_file = 'google_calendar/creds/g_calendar_token.json'

    merge_data = MergeData(google_token_file, userId, pwd)
    merge_data.getGoogleInfo()
    merge_data.packData()
    merge_data.processingHW()


if __name__ == '__main__':
    userId= os.getenv('MOODLE_ACC')
    pwd = os.getenv('MOODLE_PWD')
    main(userId, pwd)