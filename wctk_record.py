from datetime import datetime

class WCRecord:
    def __init__(self, version="None", last_mod=-1, other_record=None):
        if other_record:
            self.version = other_record.version
            self.last_modified = other_record.last_modified
        else:
            self.version = version
            self.last_modified = last_mod
            if self.last_modified == -1:
                self.last_modified = datetime.now().timestamp()

    def set_datetime_as_last_modified(self, new_last_modified_datetime):
        self.last_modified = new_last_modified_datetime

    def is_higher_version_than(self, other_record):
        self_pieces = self.version.split(".")
        other_pieces = other_record.version.split(".")
        compare_length = min(len(self_pieces), len(other_pieces))
        for index in range(0, compare_length):
            if self_pieces[index] > other_pieces[index]:
                return True
        return False

    def has_newer_modifications_than(self, other_record):
        return self.last_modified > other_record.last_modified

    def is_newer_than(self, other_record):
        return self.is_higher_version_than(other_record) or self.has_newer_modifications_than(other_record)

    def is_equal_to(self,other_record):
        return self.version == other_record.version and self.last_modified == other_record.last_modified

    def has_same_version_as(self, other_record):
        return self.version == other_record.version



