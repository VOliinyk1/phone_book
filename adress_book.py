from collections import UserDict
from datetime import date, timedelta      
import datetime
class AddressBook(UserDict):                                                              
    def iterator(self, n=1):
        page = []
        for i in range(len(list(self.data.items()))):
                page.append(list(self.data.items())[i])
                if list(self.data.items())[i] == list(self.data.items())[-1]:
                    yield page
                    page = []
                if len(page) == n :
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
            else: f'Contact not founded'
                
    def add_record(self, record):
        if record.get_record_phones():
            self.data[record.name.value] = record
            return f"Record {record.name.value} {record.get_record_phones()} is added"
        else: return "Record is not added"

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
        return str(self.value)
    
    

    @Field.value.setter
    def value(self, new_value):
        self._value = new_value


class Phone(Field):
    def __repr__(self):
        return str(self.value)

    @Field.value.setter
    def value(self, new_value):
        self._value = new_value if 10 <= len(new_value) <= 12 else None



class Birthday(Field):
    def __repr__(self):
        return str(self.value)
    
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, new_value):
        if new_value:
            date_elems = len(new_value)
            if date_elems == 10:
                bday = new_value.split('.')
                birthday = date(int(bday[0]), int(bday[1]), int(bday[2]))
                self._value = birthday
                
            else:
                print('Wrong date format')
                self._value = None

        


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phone = Phone()
        self.phone.value = phone
        self.phones = [self.phone.value] if self.phone.value else []
        self.bday = Birthday() 
        self.bday.value = birthday

    def days_to_birthday(self):
        try:
            bday_date = self.bday.value
            now_date = datetime.datetime.now().date()
            this_year_bday = date(now_date.year,  bday_date.month ,bday_date.day)
            if this_year_bday < now_date:
                next_bday = date(this_year_bday.year + 1, this_year_bday.month, this_year_bday.day)
                return f'To bday: {(next_bday - now_date).days} days'
            else: return f"To bday: {(this_year_bday - now_date).days} days"
        except:
            return 'No bday in contact'

    def get_record_phones(self):
        return [i for i in self.phones]
    
    def __repr__(self) -> str:
        return str(self.get_record_phones()) + str(self.bday)
    
    def add_bday(self, bday_date):
        self.bday = Birthday()
        self.bday.value = bday_date
        
        return f'Bday added' if self.bday.value else f'Bday not added'

    def add_phone(self, phone=''):
        if phone:
            self.phones.append(Phone(phone))
            return f'{self.name} phone {self.get_record_phones()} is added'
        return "Enter phone nuber for adding"
    
    def change_phone(self,old_phone, new_phone):
        for phone in range(len(self.phones)):
            if self.phones[phone] == str(old_phone):
                self.phones[phone] = new_phone
                return f"{self.name.value}'s number is changed to {new_phone}"
        return 'No such number'

    def remove_phone(self, phone):
        for number in self.phones:
            if number == phone:
                self.phones.remove(number)
                return f"{phone} is removed from {self.name.value}"
            return 'No such phone number'



# def generate_n_names(n):
#     return [str(i) for i in list(range(n))]

# def generate_n_numbers(n):
#     return [i for i in list(range(n))]

# names = generate_n_names(10)
# numbers = generate_n_numbers(10)


# book = AddressBook()
# for name, number in zip(names, numbers):
#     name = Name(name)
#     phone = Phone(number)
#     new_record = Record(name, phone)
#     book.add_record(new_record)

# for i in book.iterator(3):
#     print('_______________________________')
#     for key, value in dict(i).items():
#         print(f"name {key} record{value}")
