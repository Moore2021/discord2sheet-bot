"""Ask if required role needs to be created or edited"""
x=input("Would you like to edit/create a required role? y or n:    ")
if x=='y' or x=='yes':
    try:
        """Ask for required role"""
        y=input("What is your required role? (press enter for default)")
        with open('./configurations/requiredrole.txt', 'w') as requiredrole_file:
            requiredrole_file.write(y)
    except SyntaxError:
        y = None
        with open('./configurations/requiredrole.txt', 'w') as requiredrole_file:
            requiredrole_file.write(y)

"""Ask if authorized users needs to be created or edited"""
x=input("Would you like to edit/create authorized users? y or n:    ")
if x=='y' or x=='yes':
    try:
        """Ask for authorized users"""
        y=input("Who are your authorized user(s)? (press enter for default)")
        with open('./configurations/authorizedusers.txt', 'w') as authorizedusers_file:
            authorizedusers_file.write(y)
    except SystemError:
        y = None
        with open('./configurations/authorizedusers.txt', 'w') as authorizedusers_file:
            authorizedusers_file.write(y)