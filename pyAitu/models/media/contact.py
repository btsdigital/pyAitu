class Contact():
    def __init__(self, first_name: str = None, last_name: str = None, phone_number: str = None):
        self.firstName = first_name
        self.lastName = last_name
        self.phoneNumber = phone_number
        self.contactType = "InputUnregisteredContact"
