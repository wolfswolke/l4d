import string


class FirehoseRecordIdGenerator:
    def __init__(self, last_record_id=None):
        self.charset = string.ascii_lowercase + string.digits
        self.last_record_id = last_record_id if last_record_id else "00000000-0000-0000-0000-000000000000"

    def setup(self, last_record_id):
        self.last_record_id = last_record_id

    def __increment_record_id__(self, record_id):
        record_id = list(record_id.replace('-', ''))
        for i in range(len(record_id) - 1, -1, -1):
            if record_id[i] == 'z':
                record_id[i] = '0'
            elif record_id[i] == '9':
                record_id[i] = 'a'
                break
            else:
                record_id[i] = chr(ord(record_id[i]) + 1)
                break

        new_record_id = ''.join(record_id)
        new_record_id = f"{new_record_id[:8]}-{new_record_id[8:12]}-{new_record_id[12:16]}-{new_record_id[16:20]}-{new_record_id[20:]}"
        return new_record_id

    def generate(self):
        self.last_record_id = self.__increment_record_id__(self.last_record_id)
        return self.last_record_id


firehose_generator = FirehoseRecordIdGenerator()
