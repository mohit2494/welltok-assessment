import os
import argparse
from database import DBHelper
import logging

LOG = "./campaign.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)
logger = logging.getLogger(__name__)
logger = logging.getLogger(__name__)

def check_file(file):
    if not os.path.exists("./"+str(file)):
        raise argparse.ArgumentTypeError('File not present in current directory')
    if not str(file).endswith(".json"):
        raise argparse.ArgumentTypeError('Configuration file not a json file')
    return file

parser = argparse.ArgumentParser()
parser.add_argument("--file", help="config json file present in current directory",
                    type=check_file, dest='filename')
args = parser.parse_args()
try:
    comp_path = None
    if args.filename:
        comp_path = "./"+args.filename
    dbhelper = DBHelper(config_file=comp_path)
    if dbhelper.init_failed:
        raise Exception('Unable to connect to database. Please contact tools team at welltoktools@gmail.com')
    dbhelper.reload()
    print("Database reloaded. Try running campaign_cost with new data.")
except Exception as e:
    print(e)
    logger.error('Error reloading database using file:')
    