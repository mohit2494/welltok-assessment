from database import DBHelper
from calculator import calculate_cost
import logging
import argparse

# logging
LOG = "./campaign.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
logging.getLogger("").addHandler(console)
logger = logging.getLogger(__name__)

channel_id_list = []

def check_positive(value):
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                "%s is negative/zero value. Please provide a positive value" % value)
    except:
        raise argparse.ArgumentTypeError(
            "%s is an alphanumeric/text value. Please provide an int value" % value)
    return ivalue


def check_channels_and_store_ids(value):
    if any([not('0' <= ch <= '9' or 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or ch in (' ', '|')) for ch in value]):
        raise argparse.ArgumentTypeError(
            "special characters not allowed in channel codes except for |")
    channel_list = value.strip().split('|')
    channel_list = list(filter(lambda k: k.strip() != "", channel_list))
    if not channel_list:
        raise argparse.ArgumentTypeError('No channels provided in argument')
    for channel in channel_list:
        channel_id = dbhelper.get_channel_id_by_code(
            code=channel.lower().strip())
        channel_id_list.append(channel_id)
        if not channel_id:
            raise argparse.ArgumentTypeError(
                "channel %s not found in configuration." % channel)
try:
    dbhelper = DBHelper()
    if dbhelper.init_failed:
        raise Exception(
            'Unable to connect to database. Please contact welltoktools@gmail.com')
    if not dbhelper.check_tables_exist():
        dbhelper.reload()

    parser = argparse.ArgumentParser()
    parser.add_argument("--size", help="helps specify audience size for cost calculation",
                        type=check_positive, required=True)
    parser.add_argument("--channels", help="helps specify the channels pipe separated. Eg: SMS|DM|EM for sms, direct mail and email",
                        type=check_channels_and_store_ids, required=True)
    parser.add_argument("--showbreakup", help="flag for showing how the total cost was calculated",
                        dest='showbreakup', action="store_true")
    args = parser.parse_args()

    cost = calculate_cost(dbhelper, args.size, channel_id_list, args.showbreakup)
    print("Total Campaign Cost : $" + str(round(cost,2)))
except Exception as e:
    logger.error(e)