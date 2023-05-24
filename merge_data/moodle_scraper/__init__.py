from merge_data.moodle_scraper.moodle import Moodle

def getherData(userId, pwd):
    moodle = Moodle(userId, pwd)

    moodle_data = moodle.get_data()
    moodle_data = moodle.data_process(moodle_data)

    return moodle_data