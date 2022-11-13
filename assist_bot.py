CONTACTS = {}

def command_parser(command_string: str) -> tuple:
    """Takes string entered by user and parse it to command,[args] format"""
    if command_string.lower() in('','.','bye','good bye','exit','close'):
        return ('exit',[])
    
    if command_string.lower().startswith('show all'):
        return('show all', [])
    
    command_elements = command_string.lower().split()
    
    return (command_elements[0], command_elements[1:]) if command_string else ''

def question_answer_loop(command=[]):
    """Takes input from user parse it and compile relative functions"""
    while 'exit' not in command:
        command_string = input('Enter command: ')
        command, args = command_parser(command_string) 
        do_command = COMMANDS.get(command)
        
        try:
            do_command(args)
        except: print('There no such command!')
        
        continue

def input_error(func):
    """Handle user's input"""
    
    def inner(*args: list):
        if func.__name__ in ('add_handler', 'change_handler'):
            try:
                contact_name = args[0][0]
                phone_number = ''.join(args[0][1:])
                func(contact_name, phone_number)
            except: print('This command require contact name and phone number')
        
        elif func.__name__ == 'phone_handler':
            try:
                contact_name = args[0][0]
                func(contact_name)
            except: print('This command require contact name')
        else:
            try:
                func()
            except: print('There no such a command!')
    return inner

@input_error
def hello_handler():
    """Print hello!"""
    print('hello!')

@input_error
def add_handler(contact_name, phone_number):
    """Add new contact"""
    if contact_name not in CONTACTS.keys():
        CONTACTS[contact_name] = phone_number
    else: print(f"Contact {contact_name} is already exists in phone book")
    
    print(CONTACTS)

@input_error
def change_handler(contact_name, phone_number):
    """Change contact phone number by name"""
    if contact_name in CONTACTS.keys():
        CONTACTS[contact_name] = phone_number
    else: print("Ther's no such contact in phonebook")
    
    print(CONTACTS)
    
@input_error
def phone_handler(contact_name):
    """Shows phone number by name"""
    if contact_name in CONTACTS:
        print(CONTACTS[contact_name])
    else: print("Ther's no such contact in phonebook")

@input_error
def show_all_handler():
    """shows all contacts"""
    print(CONTACTS)

@input_error
def good_bye_handler():
    """Print Bye"""
    print("Bye!")

COMMANDS = {'hello': hello_handler,
            'show all': show_all_handler,
            'exit': good_bye_handler,
            'add': add_handler,
            'change': change_handler,
            'phone': phone_handler
            }

def main():
    question_answer_loop()

if __name__ == '__main__':
    main()