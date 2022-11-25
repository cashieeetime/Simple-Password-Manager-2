from asyncore import read

##############################################
# DEBUGGING FUNCTIONS
##############################################

def default_fp ():
    '''default file for debugging purposes; can also be used by the user for their own file'''
    fp = "example_password_format.txt"
    return fp

##############################################
# FILE FUNCTIONS
##############################################

def initialize_file ():
    '''repeatedly prompts for a file until one is successfully opened'''
    while True:
        fp = input("Enter a file name. \n-> ")
        try:
            file = open(fp, "r")
            return fp
        except FileNotFoundError:
            print("\n    Error: File not found.")
            continue 

def read_file (fp):
    '''opens file for reading'''
    file = open(fp, "r")
    return file

def append_file (fp):
    '''opens file for appending'''
    file = open(fp, "a")
    return file

def write_file(fp):
    '''opens file for writing'''
    file = open(fp, "w")
    return file

def create_file():
    fp = str(input("What would you like your file to be called?\n-> "))
    if ".txt" in fp:
        open(fp, "x")
        return fp
    else:
        fp += ".txt"
        open(fp, "x")
        return fp

def unknown_input():
    print("I didn't understand that.\n")

##############################################
# INITIALIZE DICTIONARY
##############################################

def build_dict (fp):
    '''Reads the file and splits lines, then calls a function to form the dictionary'''
    file = read_file(fp)

    data_dict = {}
    for line in file:   
        line = line.strip().replace(" ", "")
        linelist = line.split("|")
        data_dict[linelist[0]] = (linelist[1], linelist[2], linelist[3])
    file.close()
    return data_dict

##############################################
# TEXT FORMAT FUNCTIONS
##############################################

def character_count (data_dict):
    '''loops through the file to find the keyword with the largest number of characters per  category, then returns those number'''
    w = 0     #len for websites
    e = 0     #len for emails
    u = 0     #len for usernames
    p = 0     #len for passwords

    for key in data_dict:
        w_len = len(key)
        e_len = len(data_dict[key][0])
        u_len = len(data_dict[key][1])
        p_len = len(data_dict[key][2])

        if w_len > w:
            w = w_len
        if e_len > e:
            e = e_len
        if u_len > u:
            u = u_len
        if p_len > p:
            p = p_len 

    return w, e, u, p

def pretty_print (output, data_dict):
    w, e, u, p = character_count(data_dict)

    '''takes output from a function and formats the result for printing'''
    print("    {:{w}s} | {:{e}s} | {:{u}s} | {:{p}s}".format("Website", "Email", "Username", "Password", w = w, e = e, u = u, p = p))
    print("    {:{w}s}   {:{e}s}   {:{u}s}   {:{p}s}".format("-------", "-----", "--------", "--------", w = w, e = e, u = u, p = p))

    for key in output:
        print("    {:{w}s} | {:{e}s} | {:{u}s} | {:{p}s}".format(key, output[key][0], output[key][1], output[key][2], w = w, e = e, u = u, p = p))

##############################################
# PROGRAM ACTION FUNCTIONS
##############################################

def print_all (data_dict):
    '''sorts dictionary keys and stores it oin a new variable to return'''
    output = {}
    for key in sorted((data_dict)):
        keylist = [data_dict[key][0], data_dict[key][1], data_dict[key][2]]
        output[key] = keylist
    pretty_print(output, data_dict)

def print_sites (data_dict):
    '''prints out the dictionary keys in alphabetical order'''
    print("    Website\n    -------")
    for key in sorted(data_dict):
        print("   ", key)
    print()

def p_lookup (data_dict):
    '''takes a website name as an argument, and searches the dictionary for that key; if unable to find key, function suggests related websites'''
    answer = input("What website would you like to search for?\n-> ")
    output = {}
    alt_output = {}
    for key in sorted(data_dict):
        if answer.lower() == key.lower():
            linelist = [data_dict[key][0], data_dict[key][1], data_dict[key][2]]
            output[key] = linelist

        if key.lower().startswith(answer.lower()):
            linelist = [data_dict[key][0], data_dict[key][1], data_dict[key][2]]
            alt_output[key] = linelist

    if output != {}:
        pretty_print(output, data_dict)
    else:
        print("\nWe couldn't find any websites with that name. Do any of these similar websties match what you are looking for?\n")
        pretty_print(alt_output, data_dict)

def add_entry (fp, data_dict):
    '''add an entry to the original file'''
    file = append_file(fp)

    print("We will now ask you to input the necessary login information. Type \"n/a\" for any fields you'd like to leave blank.\n")
    website = input("What is the name of the website? \n-> ")
    email = input("\nWhat is the email address? \n-> ")
    username = input("\nWhat is the username? \n-> ")
    password = input("\nWhat is the password? \n-> ")

    linelist = [email, username, password]
    data_dict[website] = linelist
    file.write("\n" + website + " | " + email + " | " + username + " | " + password)
    file.close()
    print("\nYour data has been sucessfully saved to your file.")

def edit_entry(fp, data_dict):
    '''edit an already existing entry in the file'''
    file = write_file(fp)
    print("We will now ask you to input the necessary login information. Type \"n/a\" for any fields you'd like to leave blank.\n")

    while True:
        website = input("What is the name of the website you need to edit? \n-> ")
        try:
            linelist = data_dict[website]
            break
        except KeyError:
            print("We couldn't find that website within our data.\n")
            continue

    while True:
        answer = input("What would you like to edit?\n    1. Email Address\n    2. Username\n    3. Password\n-> ")

        if answer.strip() == "1":
            email = input("\nWhat is the new email address? \n-> ")
            data_dict[website][0] = email
            break
        elif answer.strip() == "2":
            username = input("\nWhat is the username? \n-> ")
            data_dict[website][1] = username
            break
        elif answer.lower() == "3":
            password = input("\nWhat is the password? \n-> ")
            data_dict[website][2] = password
            break
        else:
            unknown_input()
            continue

    for key in data_dict:    
        file.write(key + " | " + data_dict[key][0] + " | " + data_dict[key][1] + " | " + data_dict[key][2] + "\n")
    file.close()
    print("\nYour data has been sucessfully saved to your file.")
            
##############################################
# PROGRAM PARTS
##############################################

def intro():
    '''program intro to determine what file to use'''
    print("\nHello. Welcome to the password manager.")

    while True:
        answer = input("\nTo get started, we need the name of the file that is holding your data. Would you like to:\n    1. Provide the name of an already exisiting text file with your data\n    2. Create a new text file to store your data\n    3. Use the default file name stored in the program\n-> ")
        print()

        if answer.strip() == "1":
            fp = initialize_file()
            return fp
        elif answer.strip() == "2":
            fp = create_file()
            return fp
        elif answer.lower() == "3":
            fp = default_fp()
            return fp
        else:
            unknown_input()
            continue

def main_program(fp):
    '''main program and it's functions'''
    while True:
        data_dict = build_dict(fp) 
        answer = input("What would you like to do today?\n    1. View a complete, alphabetized list of websites, emails and passwords.\n    2. View an alphabetized list of just the websites.\n    3. Look up login information for a specific website.\n    4. Add and save a new entry to your data.\n    5. Edit an already existing entry in the database.\n-> ")
        print()

        if answer.strip() == "1":
            print_all(data_dict)
            break   
        elif answer.strip() == "2":
            print_sites(data_dict)
            break  
        elif answer.strip() == "3":
            p_lookup(data_dict)
            break
        elif answer.strip() == "4":
            add_entry(fp, data_dict)
            break
        elif answer.strip() == "5":
            edit_entry(fp, data_dict)
            break
        else:
            unknown_input()
            continue

def cont_question():
    '''question to ask the user if they'd like to coontinue or not'''
    while True:
        answer = input("\nWould you like to start over? (yes/no)\n-> ")
        
        if answer.lower() == "no":
            print("\nThank you for using the password manager. We will now close the program.\n")
            return False
        elif answer.lower() == "yes":
            print()
            return True
        else:
            unknown_input()
            continue

##############################################
# MAIN
##############################################

def main():
    cont = True
    fp = intro()
    print()
    while cont == True:
        main_program(fp)
        cont = cont_question()

main()