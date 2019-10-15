from pyAitu.utils.strings import CONTACT_TYPE, FIRST_NAME, LAST_NAME, PHONE_NUMBER


class Contact():
    def __init__(self, first_name: str = None, last_name: str = None, phone_number: str = None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.contact_type = "InputUnregisteredContact"

    def to_dict(self):
        return {
            CONTACT_TYPE: self.contact_type,
            FIRST_NAME: self.first_name,
            LAST_NAME: self.last_name,
            PHONE_NUMBER: self.phone_number
        }
