import logging
import collections
logger = logging.getLogger(__name__)


class ConfigValidator(object):

    def __init__(self):
        pass

    def empty(self, k):
        return not k or str(k).strip() == ""

    def valid_int(self, k):
        return all(['0' <= ch <= '9' for ch in str(k).strip()])

    def valid_float(self, k):
        return all(['0' <= ch <= '9' or ch == "." for ch in str(k).strip()])

    def valid_str(self, k):
        try:
            strk = str(k).strip()
            return all([ch.isalnum() or ch == " " for ch in strk])
        except:
            return False

    def validate_text_value(self, id, key, val, tablename):
        if key not in val:
            raise Exception('missing '+key+' key in ' +
                            tablename+' data for ID:'+str(id))
        keyval = val[key]
        if self.empty(keyval) or not self.valid_str(keyval):
            raise Exception(
                "invalid float value for "+key+" in "+tablename+" data for ID "+str(id))

    def validate_int_value(self, id, key, val, tablename):
        if key not in val:
            raise Exception('missing '+key+' key in ' +
                            tablename+' data for ID:'+str(id))
        keyval = val[key]
        if self.empty(keyval) or not self.valid_int(keyval):
            raise Exception(
                "invalid float value for "+key+" in "+tablename+" data for ID "+str(id))

    def validate_float_value(self, id, key, val, tablename):
        if key not in val:
            raise Exception('missing '+key+' key in ' +
                            tablename+' data for ID:'+str(id))
        keyval = val[key]
        if self.empty(keyval) or not self.valid_float(keyval):
            raise Exception(
                "invalid float value for "+key+" in "+tablename+" data for ID "+str(id))

    def check_missing_or_overlapping_intervals(self, range_data):

        def overlap(k): return (
            min(k[0][1], k[1][1]) - max(k[0][0], k[1][0])) >= 0

        def missing(k):
            return (k[1][0]-k[0][1]) > 1

        intervals = []
        for key, val in range_data.items():
            start, end = int(val['from']), int(val['to'])
            intervals.append((start, end))
        intervals.sort()

        for interval1, interval2 in zip(intervals, intervals[1:]):
            if overlap((interval1, interval2)) or missing((interval1, interval2)):
                logger.debug('Found overlapping/missing range ' +
                             str(interval1)+' and '+str(interval2))
                raise Exception('Found overlapping/missing range ' +
                                str(interval1)+' and '+str(interval2))

    def validate_range(self, range_data):
        count = 0
        for k, val in range_data.items():
            if self.empty(k) or not self.valid_int(k):
                raise Exception(
                    'Empty or Invalid ID in range data. Range Object Position : %s' % int(count+1))
            k = int(k)
            self.validate_int_value(k, 'from', val, 'range')
            self.validate_int_value(k, 'to', val, 'range')
            count += 1
        self.check_missing_or_overlapping_intervals(range_data)

    def validate_channels(self, channel_data):
        count = 0
        for k, val in channel_data.items():
            if self.empty(k) or not self.valid_int(k):
                raise Exception(
                    'Empty or Invalid ID in channel data. Channel Object Position : %s' % int(count+1))
            k = int(k)
            count += 1
            self.validate_text_value(k, 'name', val, 'channels')
            self.validate_text_value(k, 'code', val, 'channels')

    def validate_base_fee(self, base_fee_data):
        count = 0
        for k, val in base_fee_data.items():
            if self.empty(k) or not self.valid_int(k):
                raise Exception(
                    'Empty or Invalid ID in base_fee data. Base_fee Object Position : %s' % int(count+1))
            k = int(k)
            self.validate_int_value(k, 'channel_id', val, 'base_fee')
            self.validate_float_value(k, 'price', val, 'base_fee')
            count += 1

    def validate_trans_fee(self, trans_fee_data):
        count = 0
        for k, val in trans_fee_data.items():
            if self.empty(k) or not self.valid_int(k):
                raise Exception(
                    'Empty or Invalid ID in trans_fee data, trans_fee Object Position : %s' % int(count+1))
            k = int(k)
            self.validate_int_value(k, 'range_id', val, 'trans_fee')
            self.validate_int_value(k, 'channel_id', val, 'trans_fee')
            self.validate_float_value(k, 'price', val, 'trans_fee')
            count+=1