import logging
import collections
logger = logging.getLogger(__name__)

class ConfigValidator(object):

    def __init__(self):
        pass

    def empty(self, k): return not k or str(k).strip() == ""
    def valid_int(self, k): return all(['0' <= ch <= '9' for ch in str(k)])

    def check_missing_or_overlapping_intervals(self, intervals):
        
        def overlap(k): return (
            min(k[0][1], k[1][1]) - max(k[0][0], k[1][0])) >= 0
        
        def missing(k):
            return (k[1][0]-k[0][1])>1

        for interval1, interval2 in zip(intervals, intervals[1:]):
            if overlap((interval1, interval2)) or missing((interval1, interval2)):
                logger.debug('Found overlapping/missing range '+str(interval1)+' and '+str(interval2))
                raise Exception('Found overlapping/missing range '+str(interval1)+' and '+str(interval2))

    def validate_range(self, range_data):
        count = 0
        for k, val in range_data.items():
            if self.empty(k) or not self.valid_int(k):
                print(self.empty(k), self.valid_int(k))
                raise Exception(
                    'Empty or Invalid ID in range data. Range Object Position : %s' % int(count+1))
            k = int(k)
            if 'from' not in val:
                raise Exception(
                    'missing "from" key in range data for ID: '+str(k))
            from_ = val['from']
            if self.empty(from_) or not self.valid_int(from_):
                raise Exception(
                    "invalid int value for \"from\" key in range data for ID "+str(k))
            if 'to' not in val:
                raise Exception(
                    'missing "to" key in range data for ID: '+str(k))
            to_ = val['to']
            if self.empty(from_) or not self.valid_int(from_):
                raise Exception(
                    "invalid int value for \"to\" key in range data for ID "+str(k))
            count += 1
        intervals = []
        for key, val in range_data.items():
            start, end = int(val['from']), int(val['to'])
            intervals.append((start, end))
        intervals.sort()
        self.check_missing_or_overlapping_intervals(intervals)


    def validate_channels(self, channel_data):
        return True

    def validate_base_fee(self, base_fee_data):
        return True

    def validate_trans_fee(self, trans_fee_data):
        return True
