from merge_data.moodle_scraper.moodle import Moodle

def getherData(userId:str, pwd:str) -> dict:
    '''Get all data from moodle and process it

    Args:
        userId (string): user id of moodle
        pwd (string): password of moodle

    Returns:
        dict: all assessments from moodle
    '''
    moodle = Moodle(userId, pwd)

    moodle_data = moodle.get_data()
    moodle_data = moodle.data_process(moodle_data)

    return moodle_data