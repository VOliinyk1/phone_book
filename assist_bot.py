from adress_book import *

CONTACTS = AddressBook()

def command_parser(command_string: str):
    command_elements = command_string.lower().split(' ')
    command = command_elements[0]
    args = ' '.join(i for i in command_elements[1:])
    return command, args

def split_args(args_string):
    sep_args = args_string.split(' ')
    if len(sep_args) > 1:
        name = sep_args[0]
        phone = sep_args[1]
        bday = ''.join(sep_args[2:])
        return name, phone, bday
    else:
        name = sep_args[0] 
        return name
    

def input_error(func):
    """Handle user's input"""
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Wrong key'
        except ValueError:
            return 'Wrong value'
        except IndexError:
            return 'Wrong index'
        except TypeError:
            return 'Wrong type'
    return wrap

def do_command(input):
    new_input = input
    args = ''
    for key in COMMANDS:
        if input.startswith(key):
            new_input = key
            break
    args = input[len(new_input):].strip()
        
    result = COMMANDS.get(new_input, lambda : 'enter one of available commands' )
    return result(args) if args else result()

@input_error
def hello_handler():
    """Print hello!"""
    return 'hello!'

@input_error
def add_phone(args):
    """Add new contact"""
    name, phone,_ = split_args(args)
    if name:
        return CONTACTS[name].add_phone(phone)
    else: return f'Enter name'

@input_error
def change_number(args):
    """Change number"""
    old_phone, new_phone,_  = split_args(args)
    for _, record in CONTACTS.items():
        if old_phone in record.get_record_phones():
            return record.change_phone(old_phone, new_phone)
    return 'no such phone number'

@input_error
def remove_phone(args):
    """Remove record from book"""
    phone = split_args(args)
    for record in CONTACTS.values():
        if phone in record.get_record_phones():
            return record.remove_phone(phone)
    


@input_error
def add_new_record(args):
    """add new record"""
    name, phone,_ = split_args(args)
    if name not in CONTACTS.keys():
        record = Record(name=name, phone=phone)
        return CONTACTS.add_record(record)
    else: return(f'record {name} is already exists')

@input_error
def search_records(name, phone=''):
    if name.isdigit():
        phone = name
    if phone:
        for contact, record in CONTACTS.items():
            if phone in record.get_record_phones():
                return CONTACTS.search_contact(contact, record.phones)
    elif name:
        for contact, record in CONTACTS.items():
            if name == record.name.value:
                return CONTACTS.search_contact(contact, record.phones)
    else: f'Contact not founded'



@input_error
def show_all_handler():
    """shows all contacts"""
    return CONTACTS

@input_error
def good_bye_handler():
    """Print Bye"""
    return "Bye!"

@input_error
def iter_records(args):
    page_size = split_args(args)
    
    
    for i in CONTACTS.iterator(int(page_size)):
        print('_______________________________')
        for key, value in dict(i).items():
            print(f"name: {key} record:{value}")
            continue
    return '___________END____________'

@input_error
def add_bday(args):
    name,bday_date, _ = split_args(args)
    return CONTACTS[name].add_bday(bday_date) if name in CONTACTS else 'No such name'

@input_error
def days_to_bday(args):
    name = split_args(args)
    return CONTACTS[name].days_to_birthday()



COMMANDS = {'bday_count' : days_to_bday,
            'add' : add_new_record,
            'bday': add_bday,
            'n_records' : iter_records,
            'hello': hello_handler,
            'show all': show_all_handler,
            'exit': good_bye_handler,
            'new_record' : add_new_record,
            'new_phone': add_phone,
            'change_phone': change_number,
            'remove' : remove_phone,
            'add' : add_new_record,
            'search' : search_records,
            
            
            }

def main():
    print('''COMMANDS:
            bday_count' : days_to_bday,\n
            'add' : add new record to the book, Format: name* phone number*\n
            'bday': add bday date to contact. Format: name YYYY.MM.DD,\n
            'n_records' : show n records per page. Format: n_records n* \n
            'hello': hello,\n
            'show all': show all contacts,\n
            'exit': good bye,\n
            'new_record' : add new record,\n
            'new_phone': add phone to contact. Format: name* phone number*\n
            'change_phone': change number of a contact. Format: name* new_number*\n
            'remove' : remove phone,\n
            'search' : search records''')
    while True:
        user_input = input('Enter command ')
        result = do_command(user_input)
        print(result)
        if result == 'Bye!':
            break 

if __name__ == '__main__':
    main()