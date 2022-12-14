from collections import UserDict
from datetime import date, timedelta
import datetime
import pickle


class AddressBook(UserDict):

    def save_records(self):
        formated_recs = {}
        data_values = tuple(self.data.items())
        for item in data_values:
            formated_recs.update({item[0]: {'name': item[1].name.value,
                                            'phones': item[1].phones,
                                            'bday': str(item[1].bday)}})
        save_file = 'records.bin'

        with open(save_file, 'wb') as fh:
            pickle.dump(formated_recs, fh)

        return f'{len(self.data)} records is saved'

    def initialize_saved_records(self):
        file = 'records.bin'
        with open(file, 'rb') as fh:
            init_data = pickle.load(fh)
        name = Name()
        bday = Birthday()
        phones = []
        for i in init_data.values():
            name = i['name']
            phones = [Phone(phone_num) for phone_num in i['phones']]
            bday = i['bday']
            new_record = Record(name, phones=phones, birthday=bday)
            self.add_record(new_record)
        return (f'{self.data} records is loaded')

    def iterator(self, n=1):
        page = []
        for i in range(len(list(self.data.items()))):
            page.append(list(self.data.items())[i])
            if list(self.data.items())[i] == list(self.data.items())[-1]:
                yield page
                page = []
            if len(page) == n:
                yield page
                page = []

    def search_contact(self, name, phone):
        if name.isdigit():
            phone = name
        if phone:
            for contact, record in self.items():
                if phone in record.get_record_phones():
                    return contact, record.phones
        elif name:
            for contact, record in self.items():
                if name == record.name.value:
                    return contact, record.phones
        else:
            f'Contact not founded'

    def search_matches(self, name, phone):
        matches = {}
        if name.isdigit():
            phone = name
            name = ''

        if phone:
            for contact, record in self.items():
                for rec_phone in record.get_record_phones():
                    if str(phone) in str(rec_phone):
                        matches.update({contact: record.get_record_phones()})
            return matches if matches else 'Matches not founded'

        if name:
            for contact, record in self.items():
                if name in record.name.value:
                    if name not in matches.keys():
                        matches.update({contact: record})
            return matches if matches else 'Matches not found'

        else:
            return 'Matches not found'

    def add_record(self, record):
        if record.get_record_phones():
            self.data.update({record.name.value: record})
            self.save_records()
            return (
                f"Record {record.name} {record.get_record_phones()} is added")
        else:
            return "Record is not added"


class Field:
    def __init__(self, field_value=None):
        self._value = field_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.value = new_value


class Name(Field):
    def __repr__(self):
        return f'name_field: {str(self.value)}'

    @Field.value.setter
    def value(self, new_value):
        self._value = new_value


class Phone(Field):
    def __repr__(self):
        return f'{str(self.value)}'

    @Field.value.setter
    def value(self, new_value):
        self._value = new_value if 10 <= len(str(new_value)) <= 12 else None


class Birthday(Field):
    def __repr__(self):
        return f'bday_field: {str(self.value)}'

    def __str__(self):
        return (str(self.value)).replace('-', '.')

    @property
    def value(self):
        return super().value

    @Field.value.setter
    def value(self, new_value):
        if new_value:
            date_elems = len(str(new_value))
            if date_elems == 10:
                bday = str(new_value).split('.')
                birthday = date(int(bday[0]), int(bday[1]), int(bday[2]))
                self._value = birthday

            else:
                print('Wrong date format')
                self._value = None


class Record:
    def __init__(self, name, phone=None, phones=[], birthday=None):
        self.name = Name(name)
        self.phone = Phone()
        self.phone.value = phone
        self.phones = [self.phone.value] if self.phone.value else phones
        self.bday = Birthday()
        self.bday.value = birthday

    def days_to_birthday(self):
        try:
            bday_date = self.bday.value
            now_date = datetime.datetime.now().date()
            this_year_bday = date(
                now_date.year,  bday_date.month, bday_date.day)
            if this_year_bday < now_date:
                next_bday = date(this_year_bday.year + 1,
                                 this_year_bday.month, this_year_bday.day)
                return f'To bday: {(next_bday - now_date).days} days'
            else:
                return f"To bday: {(this_year_bday - now_date).days} days"
        except:
            return 'No bday in contact'

    def get_record_phones(self):
        return [i for i in self.phones]

    def __repr__(self) -> str:
        return str(self.get_record_phones()) + str(self.bday)

    def add_bday(self, bday_date):
        self.bday = Birthday()
        self.bday.value = bday_date
        AddressBook.save_records()
        return f'Bday added' if self.bday.value else f'Bday not added'

    def add_phone(self, phone=''):
        if phone:
            self.phones.append(Phone(phone))
            AddressBook.save_records()
            return f'{self.name} phone {self.get_record_phones()} is added'
        return "Enter phone nuber for adding"

    def change_phone(self, old_phone, new_phone):
        for phone in range(len(self.phones)):
            if self.phones[phone] == str(old_phone):
                self.phones[phone] = new_phone
                AddressBook.save_records()
                return f"{self.name.value}'s number is changed to {new_phone}"
        return 'No such number'

    def remove_phone(self, phone):
        for number in self.phones:
            if number == phone:
                self.phones.remove(number)
                AddressBook.save_records()
                return f"{phone} is removed from {self.name.value}"
            return 'No such phone number'


def generate_n_names(n):
    return [str(i) for i in list(range(n))]


# def generate_n_numbers(n):
#     return [i for i in list(range(n))]


# names = generate_n_names(2)
# numbers = generate_n_numbers(2)


# book = AddressBook()
# for name, number in zip(names, numbers):

#     new_record = Record(name, str(number)*10, birthday='1990.01.12')
#     book.add_record(new_record)

# book.save_records()
# book = AddressBook()
# book.initialize_saved_records()
# print('________________')
