CONTACTS = {}

def command_parser(command_string: str) -> tuple:
    command_elements = command_string.lower().split(' ')
    command = command_elements[0]
    args = ' '.join(i for i in command_elements[1:])
    return command, args

def split_args(args_string):
    sep_args = args_string.split(' ')
    name = sep_args[0]
    phone = sep_args[1]
    return name, phone

def input_error(func):
    """Handle user's input"""
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Wrong name'
        except ValueError:
            return 'Not found'
        except IndexError:
            return 'type name and number'
        except TypeError:
            return 'Enter name and phone'
    return wrap

def do_command(input):
    new_input = input
    args = ''
    for key in COMMANDS:
        if input.startswith(key):
            new_input = key
            args = input[len(new_input):].strip()
    result = COMMANDS.get(new_input, lambda : 'enter one of available commands' )
    return result(args) if args else result()

@input_error
def hello_handler():
    """Print hello!"""
    return 'hello!'

@input_error
def add_handler(args):
    """Add new contact"""
    name, phone = split_args(args)
    if name not in CONTACTS.keys():
        CONTACTS[name] = phone
        return f'{name} : {phone} is added'
    else: return f'contact {name} already exists!'

@input_error
def change_handler(args):
    """Change contact phone number by name"""
    name, phone = split_args(args)
    if name in CONTACTS:
        CONTACTS[name] = phone
        return f'Contact {name} is changed to {phone}'
    else: return 'No such contact in the phone book'
     
@input_error
def phone_handler(name):
    """Shows phone number by name"""
    if name in CONTACTS.keys():
        return CONTACTS[name]
    else: raise ValueError('Contact is not found')
    
@input_error
def show_all_handler():
    """shows all contacts"""
    return CONTACTS

@input_error
def good_bye_handler():
    """Print Bye"""
    return "Bye!"

COMMANDS = {'hello': hello_handler,
            'show all': show_all_handler,
            'exit': good_bye_handler,
            'add': add_handler,
            'change': change_handler,
            'phone': phone_handler
            }

def main():
    while True:
        user_input = input('Enter command ')
        result = do_command(user_input)
        print(result)
        if result == 'Bye!':
            break 

if __name__ == '__main__':
    main()