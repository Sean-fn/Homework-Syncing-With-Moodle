from merge_data import MergeData
from dotenv import load_dotenv
import os

load_dotenv()


def main(userId, pwd, gCred):
    merge_data = MergeData(gCred, userId, pwd)
    merge_data.run()


if __name__ == '__main__':
    main('111', '222')