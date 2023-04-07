from merge_data import MergeData

def main():
    google_token_file = 'google_calendar/creds/g_calendar_token.json'
    moodle_creds_file = 'moodle_scraper/creds/moodle_creds.json'

    merge_data = MergeData(moodle_creds_file, google_token_file)
    merge_data.getGoogleInfo()
    merge_data.packData()
    merge_data.processingHW()


if __name__ == '__main__':
    main()
