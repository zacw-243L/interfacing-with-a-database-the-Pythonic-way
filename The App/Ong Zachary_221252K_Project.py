#imports
import os, re, time, hashlib, difflib, keyboard, random, mysql.connector, tabulate, subprocess, pandas as pd
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

mysqldump_path = 'C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysqldump.exe'
mysql_path = 'C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe'


def RS():
    # Reads a text file
    with open("secrets.txt", "rb") as file:
        SK = file.readline().strip()
        SCP = file.readline().strip()
    return SK, SCP


def DP(SK, SCP):
    # Decrypts content of text file
    CS = Fernet(SK)
    DP = CS.decrypt(SCP).decode()
    return DP


def SS(NP):
    # Used to reset password, generates an encrypts new password then writes to text file
    NK = Fernet.generate_key() # new key
    CS = Fernet(NK)
    CP = CS.encrypt(NP.encode())
    with open("secrets.txt", "wb") as file:
        file.write(NK + b"\n" + CP)


SK, SCP = RS() # 1
ogpassword = DP(SK, SCP) #2
Hero = False # easter egg


def hashedpassword(ogpassword):
    # function for hashing
    # Salt for hashing password
    salt = os.urandom(16)

    # Hash the password with salt
    hashedpassword = hashlib.pbkdf2_hmac('sha256', ogpassword.encode('utf-8'), salt, 100)

    # Store the salt and hashed password securely
    storedsalt = salt.hex()
    storedhashedpassword = hashedpassword.hex()

    return storedsalt, storedhashedpassword # encrypts the password


storedsalt, storedhashedpassword = hashedpassword(ogpassword)


def connect_to_db(username, inputpassword):
    # When connecting to the database, hash the input password with the stored salt
    if inputpassword == ogpassword:
        # Convert the stored salt back to bytes
        salt = bytes.fromhex(storedsalt)
        # Hash the input password with the stored salt
        inputhashedpassword = hashlib.pbkdf2_hmac('sha256', inputpassword.encode('utf-8'), salt, 100)
        # Compare the hashed input password with the stored hashed password
        if inputhashedpassword.hex() == storedhashedpassword:
            connection = mysql.connector.connect(host="localhost", user="root", password="!password", database="ongzachary_221252k_project") # do something to obfuscate this line
            cursor = connection.cursor(buffered=True)
            cursor.execute("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''))") # enables GROUPBY
            print("\n200 OK: Connected to the database\n")
            return connection, cursor
        else:
            print("")
            return None, None
    else:
        print("")
        return None, None


def Readquery(cursor, sql_select_query, tuple1):
    start_time = time.time()
    cursor.execute(sql_select_query, tuple1)
    ReturnedRows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(ReturnedRows, columns=columns)
    table = tabulate.tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False)
    print(table)
    print("\nNo of Record Fetched:" + str(cursor.rowcount))
    print("--- %s seconds ---" % (time.time() - start_time))
    return ReturnedRows, str(cursor.rowcount)


def Readqueryint(cursor, sqlquery, tuple3):
    start_time = time.time()
    cursor.execute(sqlquery, tuple3)
    ReturnedRows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(ReturnedRows, columns=columns)
    df = df.map(lambda x: '{:,.2f}'.format(x))  # format values to integers
    table = tabulate.tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False)
    print(table)
    print("\nNo of Record Fetched:" + str(cursor.rowcount))
    print("--- %s seconds ---" % (time.time() - start_time))
    return ReturnedRows, str(cursor.rowcount)


def NONTABLEREADQuery(cursor, SQLQUERY, tuple2):
    cursor.execute(SQLQUERY, tuple2)
    ReturnedRow = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(ReturnedRow, columns=columns)
    return df, str(cursor.rowcount)


def ADDONLYSQL(cursor, ADDSQL, tuple4):
    cursor.execute(ADDSQL, tuple4)

def printrandomline(username):
    # blurb randomiser
    lines = [
        '\nSigh when are you going to do something\n',
        '\nSo what is next?\n',
        '\nPlaning your next move?\n',
        f"\n{username} have you done at least something today?\n",
        f"\nwhat ever are you going to do next {username} ?\n",
        "\ni am dying to know your next move\n"
    ]
    a = print(random.choice(lines))
    return a


def upload_to_backup():
    # create or update(overwrite) backup file
    output_file = 'Ong Zachary_221252K_Project.sql'
    print(f'\nUploading to Backup: {output_file}')
    with open(output_file, 'w') as f:
        subprocess.Popen([
            mysqldump_path,
            '-u', 'root',
            '-p!password',
            '--databases',
            'ongzachary_221252k_project',
            '--add-drop-database'
        ], stdout=f, stderr=subprocess.DEVNULL)
    # takes parameters and sends it to CMD, notice the supress warning flag


def restore_from_backup():
    # Restore from backup
    backup_file = 'Ong Zachary_221252K_Project.sql'
    print(f'\nRestoring from Backup: {backup_file}')
    with open(backup_file, 'r') as f:
        subprocess.Popen([
            mysql_path,
            '-u', 'root',
            '-p!password'
        ], stdin=f, stderr=subprocess.DEVNULL)
    # takes parameters and sends it to CMD, notice the supress warning flag


def BUP(username, connection, cursor):
    while True:
        BMM = '''
        --- Backup ---

        1)Upload to Backup
        2)Restore from Backup
        '''
        print(BMM)
        BUaction = str(input("Choose an action (1 or 2) or type 'exit' to quit: "))
        if BUaction == '1':
            # dose 2 action create file and exit this menu
            upload_to_backup()
            now = datetime.now()
            print(f'\nBackup created successfully at {now.strftime("%Y-%m-%d %H:%M:%S")}\n')
            ener = input("Press enter to continue")
            SK, SCP = RS()
            ogpassword = DP(SK, SCP)
            login_to_system()
        elif BUaction == '2':
            # dose 2 action restore database and exit this menu
            restore_from_backup()
            now = datetime.now()
            print(f'\nRestored from backup at {now.strftime("%Y-%m-%d %H:%M:%S")}\n')
            ener = input("Press enter to continue")
            SK, SCP = RS()
            ogpassword = DP(SK, SCP)
            login_to_system()
        elif BUaction.lower() == 'exit':
            # its just an exit
            print('\n')
            ener = input("Press enter to continue")
            SK, SCP = RS()
            ogpassword = DP(SK, SCP)
            login_to_system()
        else:
            print('Invalid input. Please choose 1, 2, or type exit.')


def CREATION(username, connection, cursor):
    while True:
        print('This is the menu to add or create certian data.')
        MM2 = '''
        --- Store ---

        S1)Add new store 

        --- Product ---

        P1)Add new product

        --- Customer ---

        C1)Add new customer
        
        --- Order ---
        
        O1)Add new order
        
        --- Exit ---
        
        B1)<---- Back 
        '''
        print(MM2)
        ADDINGaction = str(input("Do at least one of the following actions besides exiting or backtracking."))
        if ADDINGaction == 'S1':
            SQLQUERY = '''SELECT * FROM ongzachary_221252k_project.store;'''
            AUTOSQLQUERY2 = '''SELECT StoreID FROM store ORDER BY StoreID DESC, StoreID DESC LIMIT 1;'''
            NONTABLEREADQuery(cursor, SQLQUERY, ())
            print(f'There are currently {str(cursor.rowcount)} stores globally.\n')
            df, _ = NONTABLEREADQuery(cursor, AUTOSQLQUERY2, ())
            LS = df['StoreID'].iloc[0] if not df.empty else 0
            print(f"The lastest store ID is {LS}\n")
            while True:
                ack = str(input('Are you going to expand our empire? (Y/N)'))
                if ack == 'N':
                    print('It is a shame you cannot contribute to our empire')
                    print('\n')
                    ener = input("Press enter to continue")
                    MP(username, connection, cursor)
                if ack.isdigit():
                    print("Invalid input. Enter Y or N.")
                    continue
                while True:
                    try:
                        store_id = int(input("\nEnter Store ID: "))
                        if store_id == LS + 1:
                            break
                        else:
                            print(f"\nInvalid input. Enter a valid Store ID that is exactly {LS} + 1.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid Store ID.\n")
                store_country = input("Enter Store Country: ")
                store_state = input("Enter Store State: ")
                while True:
                    try:
                        store_square_meters = int(input("Enter Store Square Meters: "))
                        break
                    except ValueError:
                        print("Invalid input. Enter a valid integer.")
                while True:
                    store_open_date = input("Enter store open date (YYYY-MM-DD): ")
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', store_open_date):
                        year, month, day = map(int, store_open_date.split('-'))
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            break
                        else:
                            print("Invalid input. Invalid date. Enter a valid date in YYYY-MM-DD format.")
                    else:
                        print("Invalid input. Enter a valid date in YYYY-MM-DD format.")
                try:
                    params = (store_id, store_country, store_state, store_square_meters, store_open_date)
                    ADDQUERY = '''INSERT INTO store (StoreID, `Store Country`, `Store State`, `Store Square Meters`, `Store Open Date`) VALUES (%s, %s, %s, %s, %s);'''
                    ADDONLYSQL(cursor, ADDQUERY, params)
                    connection.commit()
                    Parameter = store_id
                    SQLQuery = ''' SELECT * FROM ongzachary_221252k_project.store WHERE StoreID = %s ; '''
                    print('\n')
                    Readquery(cursor, SQLQuery, (Parameter,))
                    SQLQUERY = '''SELECT * FROM store;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    print("\nStore added. Empire expanded")
                    print(f'There are now currently {str(cursor.rowcount)} stores globally.\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except mysql.connector.errors.IntegrityError as e:
                    connection.rollback()
                    print("\nFailed to add store: That store already exists. Try again with a different store.")
                    print('\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except Exception as e:
                    connection.rollback()
                    print(f'Failed to add store due to an unexpected error: {e}')
        if ADDINGaction == 'P1':
            categories = ["Audio", "Cameras and camcorders", "Cell phones", "Computers", "Games and Toys", "Home Appliances", "Music, Movies and Audio Books", "TV and Video"]
            brands = ["A. Datum", "Adventure Works", "Contoso", "Fabrikam", "Litware", "Northwind Traders", "Proseware", "Southridge Video", "Tailspin Toys", "The Phone Company", "Wide World Importers"]
            subcategories_dict = {
                "Audio": ["Recording Pen", "MP4&MP3", "Bluetooth Headphones"],
                "Cameras and camcorders": ["Cameras & Camcorders Accessories", "Digital SLR Cameras", "Camcorders","Digital Cameras"],
                "Cell phones": ["Smart phones & PDAs", "Cell phones Accessories", "Touch Screen Phones", "Home & Office Phones"],
                "Computers": ["Laptops", "Desktops", "Printers, Scanners & Fax", "Projectors & Screens", "Computers Accessories", "Monitors"],
                "Games and Toys": ["Download Games", "Boxed Games"],
                "Home Appliances": ["Microwaves", "Air Conditioners", "Fans", "Refrigerators", "Lamps", "Water Heaters", "Coffee Machines", "Washers & Dryers"],
                "Music, Movies and Audio Books": ["Movie DVD"],
                "TV and Video": ["Televisions", "Car Video", "Home Theater System", "VCD & DVD"]
            }
            SQLQUERY = '''SELECT * FROM product ;'''
            AUTOSQLQUERY2='''SELECT ProductID FROM product ORDER BY ProductID DESC, ProductID DESC LIMIT 1;'''
            NONTABLEREADQuery(cursor, SQLQUERY, ())
            print(f'There are currently {str(cursor.rowcount)} products.')
            df, _ = NONTABLEREADQuery(cursor, AUTOSQLQUERY2, ())
            latestP = df['ProductID'].iloc[0] if not df.empty else 0
            print(f"The lastest ProductID is {latestP}\n")
            while True:
                ack = str(input('\nAre you adding more products? (Y/N)'))
                if ack == 'N':
                    print('It is a shame you cannot contribute to our sales')
                    print('\n')
                    ener = input("Press enter to continue")
                    MP(username, connection, cursor)
                if ack.upper() != 'Y':
                    print("Invalid input. Enter Y or N.")
                    continue
                while True:
                    try:
                        a = int(input("\nEnter product ID: "))
                        if a == latestP + 1:
                            break
                        else:
                            print(f"\nInvalid input. Enter a valid product ID that is exactly {latestP} + 1.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid product ID.\n")
                b = input("Enter product name: ")
                while True:
                    c = input('Enter product brand: ')
                    if c in brands:
                        break
                    else:
                        print("Invalid input. Enter one of the brands below:")
                        for i, brand in enumerate(brands, start=1):
                            print(f"{i}) {brand}")
                d = input('Enter product color: ')
                while True:
                    e = input('Enter product category: ')
                    if e in ["Audio", "Cameras and camcorders", "Cell phones", "Computers", "Games and Toys", "Home Appliances", "Music, Movies and Audio Books", "TV and Video"]:
                        break
                    else:
                        print("Invalid input. Enter one of the categories below:")
                        for i, category in enumerate(categories, start=1):
                            print(f"{i}) {category}")
                while True:
                    f = input('Enter product subcategory: ')
                    if f in subcategories_dict[e]:
                        break
                    else:
                        print(f"Invalid subcategory. Valid subcategories for {e} are:")
                        for i, subcategory in enumerate(subcategories_dict[e], start=1):
                            print(f"{i}) {subcategory}")
                while True:
                    user_input = input('Enter product unit cost: ')
                    if user_input == '':
                        print("\nBlank input is not allowed. Please enter a valid cost.\n")
                        continue
                    try:
                        g = float(user_input)
                        if len(str(g).split('.')[1]) > 2:
                            print("\nPlease enter a value with no more than 2 decimal places.\n")
                            continue
                        break
                    except ValueError:
                        print("\nInvalid input. Please enter a valid cost.\n")

                while True:
                    user_input = input('Enter product unit price: ')
                    if user_input == '':
                        print("\nBlank input is not allowed. Please enter a valid price.\n")
                        continue
                    try:
                        h = float(user_input)
                        if len(str(h).split('.')[1]) > 2:
                            print("\nPlease enter a value with no more than 2 decimal places.\n")
                            continue
                        break
                    except ValueError:
                        print("\nInvalid input. Please enter a valid price.\n")
                try:
                    cursor.execute("START TRANSACTION;")
                    product_query = '''INSERT INTO product (ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Category`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
                    params = (a, b, c, d, e, f, g, h)
                    ADDONLYSQL(cursor, product_query, params)
                    totalsales_params = (a, g, h)
                    totalsales_query = '''INSERT INTO totalsales (ProductID, `Product Unit Cost`, `Product Unit Price`) VALUES (%s, %s, %s);'''
                    ADDONLYSQL(cursor, totalsales_query, totalsales_params)
                    connection.commit()
                    Parameter = a
                    SQLQuery = '''SELECT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Category`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price` FROM product WHERE ProductID = %s ;'''
                    print('\n')
                    Readquery(cursor, SQLQuery, (Parameter,))
                    SQLQUERY = '''SELECT * FROM product ;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    print('\nProduct added successfully.')
                    print(f'There are now currently {str(cursor.rowcount)} products.\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except mysql.connector.errors.IntegrityError as e:
                    connection.rollback()
                    print("\nFailed to add product: That product already exists. Try again with a different product.")
                    print('\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except Exception as e:
                    connection.rollback()
                    print(f'Failed to add product due to an unexpected error: {e}')
        if ADDINGaction == 'C1':
            SQLQUERY = '''SELECT * FROM customer;'''
            AUTOSQLQUERY2 = '''SELECT CustID FROM customer ORDER BY CustID DESC, CustID DESC LIMIT 1;'''
            NONTABLEREADQuery(cursor, SQLQUERY, ())
            print(f'There are currently {str(cursor.rowcount)} customers.')
            df, _ = NONTABLEREADQuery(cursor, AUTOSQLQUERY2, ())
            latestcust = df['CustID'].iloc[0] if not df.empty else 0
            print(f"The lastest customer ID is {latestcust}\n")
            while True:
                ack = str(input('\nDo we have a new customer? (Y/N)'))
                if ack == 'N':
                    print('It is a shame you cannot expand our customer base')
                    print('\n')
                    ener = input("Press enter to continue")
                    MP(username, connection, cursor)
                if ack.upper() != 'Y':
                    print("Invalid input. Enter Y or N.")
                    continue
                print('--- Customer Info ---')
                while True:
                    try:
                        PA = int(input("\nEnter customer ID: "))
                        if PA == latestcust + 1:
                            break
                        else:
                            print(f"\nInvalid input. Enter a valid customer ID that is exactly {latestcust} + 1.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid customer ID.\n")
                while True:
                    PB = input("Enter customer Name: ")
                    if re.match(r'^[\w\u00C0-\u017F]+ [\w\u00C0-\u017F]+$', PB):
                        break
                    else:
                        print("Invalid input. Enter a valid customer name.")
                while True:
                    PC = input("Enter customer gender (Male/Female): ")
                    if PC in ['Male', 'Female']:
                        break
                    else:
                        print("Invalid input. Enter Male or Female.")
                while True:
                    PD = input("Enter customer birthday (YYYY-MM-DD): ")
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', PD):
                        year, month, day = map(int, PD.split('-'))
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            break
                        else:
                            print("\nInvalid input. Invalid date. Enter a valid date in YYYY-MM-DD format.\n")
                    else:
                        print("\nInvalid input. Enter a valid date in YYYY-MM-DD format.\n")
                print(f"--- Customer's Residence Info ---")
                while True:
                    PE = input("Enter customer continent: ")
                    if PE == "":
                        print("\nInput cannot be blank. Try again.\n")
                    elif PE.isalpha():
                        break
                    else:
                        print("\nInvalid input. Enter a valid customer continent.\n")
                while True:
                    PF = input("Enter customer country: ")
                    if PF == "":
                        print("\nInput cannot be blank. Try again.\n")
                    elif PF.isalpha():
                        break
                    else:
                        print("\nInvalid input. Enter a valid customer country.\n")
                while True:
                    PG = input("Enter customer city: ")
                    if PG == "":
                        print("\nInput cannot be blank. Try again.\n")
                    elif PG.isalpha():
                        break
                    else:
                        print("\nInvalid input. Enter a valid customer city.\n")
                while True:
                    PH = input("Enter customer state: ")
                    if PH == "":
                        print("\nInput cannot be blank. Try again.\n")
                    elif PH.isalpha():
                        break
                    else:
                        print("\nInvalid input. Enter a valid customer state.\n")
                while True:
                    PI = input("Enter customer state code: ")
                    if PI == "":
                        print("\nInput cannot be blank. Try again.\n")
                    elif PI.isalpha():
                        break
                    else:
                        print("\nInvalid input. Enter a valid customer state code.\n")
                while True:
                    PJ = input("Enter customer zip code: ")
                    if PJ == "":
                        print("\nZip code cannot be blank. Try again.\n")
                    else:
                        break
                try:
                    params = (PA, PB, PC, PD, PE, PF, PG, PH, PI, PJ)
                    ADDQUERY = '''INSERT INTO customer (CustID,`Cust Name`,`Cust Gender`,`Cust Birthday`,`Cust Continent`,`Cust Country`,`Cust City`,`Cust State`,`Cust State Code`,`Cust Zip Code`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
                    ADDONLYSQL(cursor, ADDQUERY, params)
                    connection.commit()
                    Parameter = PA
                    SQLQuery = '''SELECT * FROM customer WHERE CustID = %s ;'''
                    print('\n')
                    Readquery(cursor, SQLQuery, (Parameter,))
                    SQLQUERY = '''SELECT * FROM customer;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    print("\nCustomer added. Custoemr base expanded")
                    print(f'There are now currently {str(cursor.rowcount)} customers.\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except mysql.connector.errors.IntegrityError as e:
                    connection.rollback()
                    print("\nFailed to add customer: That customer already exists. Are you trying to commit identity theft? Try again with a different customer.")
                    print('\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except Exception as e:
                    connection.rollback()
                    print(f'Failed to add customer due to an unexpected error: {e}')
        if ADDINGaction == 'O1':
            AUTOSQLQUERY1 = '''SELECT * FROM ongzachary_221252k_project.order;'''
            AUTOSQLQUERY2 ='''SELECT `Order Number`FROM ongzachary_221252k_project.order ORDER BY `Order Date` DESC, `Order Number` DESC LIMIT 1;'''
            NONTABLEREADQuery(cursor, AUTOSQLQUERY1, ())
            print(f'\nThere are currently {str(cursor.rowcount)} orders.')
            df, _ = NONTABLEREADQuery(cursor, AUTOSQLQUERY2, ())
            latestorder = df['Order Number'].iloc[0] if not df.empty else 0
            print(f"The lastest order number is {latestorder}\n")
            while True:
                ack = str(input('\nDo we have a new order? (Y/N)\n'))
                if ack == 'N':
                    print('It is a shame you could not make a sale, perform better next time')
                    print('\n')
                    ener = input("Press enter to continue")
                    MP(username, connection, cursor)
                if ack.upper() != 'Y':
                    print("Invalid input. Enter Y or N.")
                    continue
                print('--- Order Info ---')
                while True:
                    try:
                        A = int(input("\nEnter Order Number: "))
                        if A == latestorder + 1:
                            break
                        else:
                            print(f"\nInvalid input. Enter a valid Order Number that is exactly {latestorder} + 1.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid Order Number.\n")
                while True:
                    B = input("Enter Order Date (YYYY-MM-DD): ")
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', B):
                        year, month, day = map(int, B.split('-'))
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            OD = datetime(year, month, day)
                            break
                        else:
                            print("\nInvalid input. Invalid date. Enter a valid date in YYYY-MM-DD format.\n")
                    else:
                        print("\nInvalid input. Enter a valid date in YYYY-MM-DD format.\n")
                while True:
                    C = input("Enter Delivery Date (YYYY-MM-DD): ")
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', C):
                        year, month, day = map(int, C.split('-'))
                        if 1 <= month <= 12 and 1 <= day <= 31:
                            DD = datetime(year, month, day)
                            if DD < OD:
                                print("\nInvalid input. The Delivery Date cannot be before the Order Date. Please enter a valid date.\n")
                            elif DD > OD + timedelta(days=5):
                                print("\nInvalid input. Delivery Date must be no more than 5 days after the Order Date.\n")
                            else:
                                break
                        else:
                            print("\nInvalid input. Invalid date. Enter a valid date in YYYY-MM-DD format.\n")
                    else:
                        print("\nInvalid input. Enter a valid date in YYYY-MM-DD format.\n")
                while True:
                    try:
                        SQLQUERY = '''SELECT * FROM store;'''
                        NONTABLEREADQuery(cursor, SQLQUERY, ())
                        sc = cursor.rowcount
                        print(f'There are currently {sc} stores globally.')
                        D = int(input("\nEnter Store ID: "))
                        if 1 <= D <= sc:
                            break
                        else:
                            print(f"\nInvalid input. Enter a Store ID between 1 and {sc}.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid integer.\n")
                while True:
                    try:
                        SQLQUERY = '''SELECT * FROM customer;'''
                        NONTABLEREADQuery(cursor, SQLQUERY, ())
                        CC = cursor.rowcount
                        print(f'There are currently {CC} customers.')
                        E = int(input("\nEnter customer ID: "))
                        if 1 <= E <= CC:
                            break
                        else:
                            print(f"\nInvalid input. Enter a customer ID between 1 and {CC}.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid integer.\n")
                try:
                    params = (A,B,C,D,E)
                    ORDERSQL = '''INSERT INTO ongzachary_221252k_project.order (`Order Number`, `Order Date`, `Delivery Date`, StoreID, CustID) VALUES (%s, %s, %s, %s, %s);'''
                    ADDONLYSQL(cursor, ORDERSQL, params)
                    connection.commit()
                    Parameter = A
                    SQLQuery = '''SELECT * FROM ongzachary_221252k_project.order WHERE `Order Number` = %s ;'''
                    print('\n')
                    Readquery(cursor, SQLQuery, (Parameter,))
                    SQLQUERY = '''SELECT * FROM ongzachary_221252k_project.order;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    print("\nOrder Created.")
                    print(f'There are now currently {str(cursor.rowcount)} orders.\n')
                    LI = 1
                    print('--- Line Items ---')
                    while True:
                        if LI == 1:
                            ALI = input("\nAdd a line item (Y/N): ").upper()
                            if ALI == 'N':
                                break
                            elif ALI != 'Y':
                                print("Invalid input. Enter Y or N.")
                                continue
                        else:
                            ALI2 = input("\nAdd another line item? (Y/N): ").upper()
                            if ALI2 == 'N':
                                break
                            elif ALI2 != 'Y':
                                print("Invalid input. Enter Y or N.")
                                continue
                        while True:
                            try:
                                SQLQUERY = '''SELECT * FROM product;'''
                                NONTABLEREADQuery(cursor, SQLQUERY, ())
                                PC = cursor.rowcount
                                print(f'\nThere are currently {PC} products.\n')
                                PID = int(input(f"Enter Product ID for Line Item {LI}: "))
                                if 1 <= PID <= PC:
                                    break
                                else:
                                    print(f"\nInvalid input. Enter a product ID between 1 and {PC}.\n")
                            except ValueError:
                                print("\nInvalid input. Enter a valid integer.\n")
                        while True:
                            try:
                                PQ = int(input(f"Enter Purchased Quantity for Line Item {LI}: "))
                                if PQ > 0:
                                    break
                                else:
                                    print("\nInvalid input. Enter a quantity greater than 0.\n")
                            except ValueError:
                                print("\nInvalid input. Enter a valid integer.\n")
                        LIparams = (A, LI, PID, PQ)
                        LINEITEMSQL = '''INSERT INTO ongzachary_221252k_project.lineitem (`Order Number`, `Line Item`, ProductID, `Purchased Quantity`) VALUES (%s, %s, %s, %s);'''
                        try:
                            ADDONLYSQL(cursor, LINEITEMSQL, LIparams)
                            connection.commit()
                            print(f"Line item {LI} added.")
                            LI += 1
                        except Exception as e:
                            connection.rollback()
                            print(f"Failed to add line item due to an unexpected error: {e}")
                    Parameter = A
                    SQLQuery = ''' SELECT `Line Item`, p.ProductID, `Purchased Quantity`, p.`Product Unit Cost`, p.`Product Unit Price` FROM lineitem l JOIN product p ON l.ProductID = p.ProductID WHERE `Order Number` = %s ;'''
                    print(f"\nOrder Number: {Parameter}")
                    Readquery(cursor, SQLQuery, (Parameter,))
                    print('\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except mysql.connector.errors.IntegrityError as e:
                    connection.rollback()
                    print("\nFailed to add order: That order already exists. Are you trying to commit theft or fraud? Try again with a different order.")
                    print('\n')
                    ener = input("Press enter to continue")
                    CREATION(username, connection, cursor)
                except Exception as e:
                    connection.rollback()
                    print(f'Failed to add customer due to an unexpected error: {e}')
        if ADDINGaction == 'B1':
            printrandomline(username)
            time.sleep(1)
            print('backing out ...')
            MP(username, connection, cursor)


def READING(username, connection, cursor):
    while True:
        print('\nThis is the menu to show or view certain data') # maybe to many search functions
        MM3 = '''
    --- Product ---    
        
    P1) Search product based on product ID
    P2) Search product based on Product Name
    P3) Search product based on Product Brand
    P4) Search product based on Product Category
    
    --- Customer ---
    
    C1) Search customer based on customer ID
    C2) Search customer based on customer Name
    C3) Search customer based on country of residence
    C4) Search customers based on birthday month to check eligibility for birthday discount
    
    --- Order ---
    
    O1) View invoice based on Order Number 
    O2) View invoice based on customer ID
    O3) View customer spending data based on orders
    O4) View financial performance of company stores based on orders
    
    --- Sales ---
    
    S1) Check financial performance of product based on product ID
    S2) Check financial performance of product based on product name
    S3) Check financial performance of company to date
    S4) Check yearly financial performance of company
    
    --- Exit ---
    
    B1)<---- Back 
        '''
        print(MM3)
        READINGaction = str(input("Do at least one of the following actions besides exiting or backtracking."))
        if READINGaction == 'P1':
            #enter number product comes out
            while True:
                try:
                    SQLQUERY = '''SELECT * FROM product;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    PC = cursor.rowcount
                    print(f'\nThere are currently {PC} products.\n')
                    Parameter = int(input(f"Enter Product ID: "))
                    if 1 <= Parameter <= PC:
                        break
                    else:
                        print(f"\nInvalid input. Enter a product ID between 1 and {PC}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid integer.\n")
            SQLQuery = '''SELECT * FROM product WHERE ProductID = %s'''
            Readquery(cursor, SQLQuery, (Parameter,))
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'P2':
            Parameter = input("Enter Product Name: ")
            SQLQuery = '''SELECT * FROM product WHERE `Product Name` = %s'''
            Readquery(cursor, SQLQuery, (Parameter,))
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'P3':
            subMM3 = '''
        --- All Brands ---
        
        1) A. Datum
        2) Adventure Works
        3) Contoso
        4) Fabrikam
        5) Litware
        6) Northwind Traders
        7) Proseware
        8) Southridge Video
        9) Tailspin Toys
        10) The Phone Company
        11) Wide World Importers
            
        --- end --- 
            '''
            print(subMM3)
            BRANDINGaction = input("Enter Brand Name: ")
            if BRANDINGaction == '1' or BRANDINGaction == "A. Datum":
                print('A. Datum')
                Parameter = 'A. Datum'
                SQLQuery = """ SELECT DISTINCT ProductID,`Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '2' or BRANDINGaction == "Adventure Works":
                print('Adventure Works')
                Parameter = 'Adventure Works'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '3' or BRANDINGaction == "Contoso":
                print('Contoso')
                Parameter = 'Contoso'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '4' or BRANDINGaction == "Fabrikam":
                print('Fabrikam')
                Parameter = 'Fabrikam'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '5' or BRANDINGaction == "Litware":
                print('Litware')
                Parameter = 'Litware'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '6' or BRANDINGaction == "Northwind Traders":
                print('Northwind Traders')
                Parameter = 'Northwind Traders'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '7' or BRANDINGaction == "Proseware":
                print('Proseware')
                Parameter = 'Proseware'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '8' or BRANDINGaction == "Southridge Video":
                print('Southridge Video')
                Parameter = 'Southridge Video'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '9' or BRANDINGaction == "Tailspin Toys":
                print('Tailspin Toys')
                Parameter = 'Tailspin Toys'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '10' or BRANDINGaction == "The Phone Company":
                print('The Phone Company')
                Parameter = 'The Phone Company'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            elif BRANDINGaction == '11' or BRANDINGaction == "Wide World Importers":
                print('Wide World Importers')
                Parameter = 'Wide World Importers'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Brand` = %s GROUP BY `Product Name`; """
                Readquery(cursor, SQLQuery, (Parameter,))
                print('\n')
                ener = input("Press enter to continue")
            else:
                print("Invalid action. Try again.")
        if READINGaction == 'P4':
            sub1MM3 = '''
            --- All Categories ---

            1) Audio
            2) Cameras and camcorders
            3) Cell phones
            4) Computers
            5) Games and Toys
            6) Home Appliances
            7) Music, Movies and Audio Books
            8) TV and Video
            
            --- end --- 
                '''
            subcat = None  #this is important
            valid_input = False  #also this
            print(sub1MM3)
            catact = input("Enter Product Category: ")
            if catact == '1' or catact == "Audio":
                valid_input = True
                Parameter = 'Audio'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if catact == '2' or catact == "Cameras and camcorders":
                valid_input = True
                Parameter = 'Cameras and camcorders'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if catact == '3' or catact == "Cell phones":
                valid_input = True
                Parameter = 'Cell phones'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if catact == '4' or catact == "Computers":
                valid_input = True
                Parameter = 'Computers'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if catact == '5' or catact == "Games and Toys":
                valid_input = True
                Parameter = 'Games and Toys'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if catact == '6' or catact == "Home Appliances":
                valid_input = True
                Parameter = 'Home Appliances'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if catact == '7' or catact == "Music, Movies and Audio Books":
                valid_input = True
                Parameter = 'Music, Movies and Audio Books'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if catact == '8' or catact == "TV and Video":
                valid_input = True
                Parameter = 'TV and Video'
                SQLQuery = """ SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Category` = %s GROUP BY `Product Name`; """
                print(f"Category: {Parameter}")
                subcat = Readquery(cursor, SQLQuery, (Parameter,))
            if not subcat:
                print("No subcategories found for this category.")
            else:
                if subcat:
                    autoQ = '''
                    SELECT COUNT(DISTINCT `Product Subcategory`) AS TotalSubcategories
                    FROM (
                    SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity 
                    FROM product 
                    WHERE `Product Category` = %s 
                    GROUP BY `Product Name`
                    ) AS subquery;
                    '''
                    df, _ = NONTABLEREADQuery(cursor, autoQ, (Parameter,))
                    TotalSubcats = df['TotalSubcategories'].iloc[0] if not df.empty else 0
                    print(f"{TotalSubcats} subcategories were found for {Parameter} category")
                while True:
                    Subcategory = str(input("\nEnter Subcategory or ('exit' to quit): "))
                    if Subcategory.lower() == 'exit':
                        READING(username, connection, cursor)
                    if Subcategory.isdigit():
                        print("Invalid input. Enter a valid Subcategory.")
                        continue
                    # Query to get line items for the input order number
                    SQLQuerySubcategory = '''SELECT DISTINCT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Unit Cost`, `Product Unit Price`, TotalPurchasedQuantity FROM product WHERE `Product Subcategory` = %s GROUP BY `Product Name`;'''
                    print(f"Subcategory: {Subcategory}")
                    Subs = Readquery(cursor, SQLQuerySubcategory, (Subcategory,))
                    print('\n')
                    ener = input("Press enter to continue")
                    READING(username, connection, cursor)
            if not valid_input:
                print("Invalid input. Enter a number between 1 and 8 or a valid category name.")
                print('\n')
                ener = input("Press enter to continue")
        if READINGaction == 'C1':
            # enter number customer comes out
            while True:
                try:
                    SQLQUERY = '''SELECT * FROM customer;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    CC = cursor.rowcount
                    print(f'There are currently {CC} customers.')
                    Parameter = int(input("\nEnter customer ID: "))
                    if 1 <= Parameter <= CC:
                        break
                    else:
                        print(f"\nInvalid input. Enter a customer ID between 1 and {CC}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid integer.\n")
            SQLQuery = '''SELECT * FROM customer WHERE CustID = %s'''
            Readquery(cursor, SQLQuery, (Parameter,))
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'C2':
            while True:
                Parameter = input("Enter customer Name: ")
                if re.match(r'^[\w\u00C0-\u017F]+ [\w\u00C0-\u017F]+$', Parameter):
                    break
                else:
                    print("Invalid input. Enter a valid customer name.")
            SQLQuery = '''SELECT * FROM customer WHERE `Cust Name` = %s'''
            Readquery(cursor, SQLQuery, (Parameter,))
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'C3':
            while True:
                Parameter = str(input("\nEnter country name: "))
                if Parameter.isdigit():
                    print("Invalid input. Enter a valid country.")
                else:
                    break
            SQLQuery = '''SELECT CustID, `Cust Name`, `Cust Gender`, `Cust City`, `Cust State`, `Cust State Code`, `Cust Zip Code` FROM customer WHERE `Cust Country` = %s ;'''
            print(f"Country: {Parameter}")
            Readquery(cursor, SQLQuery, (Parameter,))
            print(f'\nThere are {str(cursor.rowcount)} customers living in {Parameter}')
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'C4':
            while True:
                Parameter = input("Enter month (in numbers): ")
                if Parameter.isdigit() and 1 <= int(Parameter) <= 12:
                    break
                else:
                    print("Invalid input. Enter a valid month (1-12).")
            SQLQuery = '''SELECT CustID, `Cust Name`, `Cust Gender`, `Cust Birthday` FROM customer WHERE MONTH(`Cust Birthday`) = %s ;'''
            Readquery(cursor, SQLQuery, (Parameter,))
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'O1':
            # enter number order comes out, also dose abit of math
            while True:
                try:
                    AUTOSQLQUERY1 = '''SELECT * FROM ongzachary_221252k_project.order;'''
                    NONTABLEREADQuery(cursor, AUTOSQLQUERY1, ())
                    OC = cursor.rowcount
                    print(f'\nThere are currently {str(cursor.rowcount)} orders.')
                    AUTOORDERSEARCHQUERY = '''SELECT `Order Number` FROM ongzachary_221252k_project.order;'''
                    df, _ = NONTABLEREADQuery(cursor, AUTOORDERSEARCHQUERY, ())
                    min = df['Order Number'].min()
                    max = df['Order Number'].max()
                    print(f"The lastest order number is {max}\n")
                    Parameter = int(input(f"Enter order number: "))
                    if min <= Parameter <= max:
                        break
                    else:
                        print(f"\nInvalid input. Enter a order number between {min} and {max}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid integer.\n")
            SQLQuery = ''' SELECT `Line Item`, p.ProductID, `Purchased Quantity`, p.`Product Unit Cost`, p.`Product Unit Price` FROM lineitem l JOIN product p ON l.ProductID = p.ProductID WHERE `Order Number` = %s ;'''
            print(f"\nOrder Number: {Parameter}")
            df, _ = NONTABLEREADQuery(cursor, SQLQuery, (Parameter,))
            Readquery(cursor, SQLQuery, (Parameter,))
            if not df.empty:
                df['Total Cost'] = df['Purchased Quantity'] * df['Product Unit Price']
                Totalamount = round(df['Total Cost'].sum(), 2)
            else:
                Totalamount = 0
            print(f"\nTotal amount paid by the customer for Order Number {Parameter}: {Totalamount}")
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'O2':
            # its actaully 2 actions, enter number orders tied to customer comes out, enter the list of numbers the customer has a single order comes out
            while True:
                try:
                    SQLQUERY = '''SELECT * FROM customer;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    CC = cursor.rowcount
                    print(f'There are currently {CC} customers.')
                    Parameter = int(input("\nEnter customer ID: "))
                    if 1 <= Parameter <= CC:
                        break
                    else:
                        print(f"\nInvalid input. Enter a customer ID between 1 and {CC}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid integer.\n")
            SQLQueryOrders = '''SELECT `Order Number`, `Order Date`, `Delivery Date` FROM ongzachary_221252k_project.`order` WHERE CustID = %s ; '''
            print(f"Customer {Parameter}'s orders")
            orders, _ = Readquery(cursor, SQLQueryOrders, (Parameter,)) # returns number of orders tied to customer
            # Check if any orders are returned
            if not orders[0]:
                print("No orders found for this customer.")
            else:
                if orders:
                    print(f"{str(cursor.rowcount)} orders where found for customer {Parameter}")
                while True:
                    ordernumber = input("\nEnter Order Number (in numbers) to view line items or ('exit' to quit): ") #enter order number the customer has
                    if ordernumber.lower() == 'exit':
                        break
                    # Validate order number input
                    if not ordernumber.isdigit():
                        print("Invalid input. Enter a valid order number.")
                        continue
                    ordernumber = int(ordernumber)
                    # Query to get line items for the input order number
                    SQLQueryLineItems = '''SELECT l.`Line Item`, p.ProductID, l.`Purchased Quantity`, p.`Product Unit Cost`, p.`Product Unit Price` FROM lineitem l JOIN product p ON l.ProductID = p.ProductID WHERE l.`Order Number` = %s;'''
                    print(f"\nOrder Number: {ordernumber}")
                    line_items = Readquery(cursor, SQLQueryLineItems, (ordernumber,))
                    if not line_items[0]:
                        print(f"No line items found for Order Number: {ordernumber}")
                    else:
                        if line_items:
                            df, _ = NONTABLEREADQuery(cursor, SQLQueryLineItems, (ordernumber,))
                            if not df.empty:
                                df['Total Cost'] = df['Purchased Quantity'] * df['Product Unit Price']
                                Totalamount = round(df['Total Cost'].sum(), 2)
                            else:
                                Totalamount = 0
                            print(f"\nTotal amount paid by the customer for Order Number {ordernumber}: {Totalamount}")
                            print(f"{str(cursor.rowcount)} line items where found for customer {Parameter}\n")
                            ener = input("Press enter to continue")
                    break
        if READINGaction == 'O3':
            print('\nasking for data ...')
            time.sleep(0.5)
            AUTOSQLQUERY ='''SELECT o.CustID, o.`Order Date`, o.`Order Number`, li.`Line Item`, li.ProductID, li.`Purchased Quantity`, p.`Product Unit Cost`, p.`Product Unit Price` FROM ongzachary_221252k_project.order o INNER JOIN lineitem li ON o.`Order Number` = li.`Order Number`INNER JOIN product p ON li.ProductID = p.ProductID;'''
            df, _ = NONTABLEREADQuery(cursor, AUTOSQLQUERY, ())
            print('averaging orders...')
            time.sleep(0.5)
            orders_per_customer = df.groupby('CustID')['Order Number'].nunique()
            average_orders_per_customer = orders_per_customer.mean()
            print('averaging spending...')
            time.sleep(0.5)
            df['Total Spending'] = df['Purchased Quantity'] * df['Product Unit Price']
            total_spending_per_customer = df.groupby('CustID')['Total Spending'].sum()
            average_spending_per_customer = total_spending_per_customer.mean()
            print('calculating popularity...')
            time.sleep(0.5)
            customers_per_product = df.groupby('ProductID')['CustID'].nunique()
            most_customers_product_id = customers_per_product.idxmax()
            most_customers_count = customers_per_product.max()
            total_amount_bought = df.loc[df['ProductID'] == most_customers_product_id, 'Purchased Quantity'].sum()
            print(f"\nThe average number of orders per customer to date is {average_orders_per_customer:.2f}")
            print(f"The average spending per customer to date is {average_spending_per_customer:,.2f}")
            print(f"The most popular product is ProductID {most_customers_product_id} with {most_customers_count} unique customers buying a total amount of {total_amount_bought} ProductID {most_customers_product_id} to date.\n")
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            df = df.dropna(subset=['Order Date'])
            current_year = datetime.now().year
            while True:
                print('filter by year to view more data')
                try:
                    year = int(input(f"\nEnter year (2016-{current_year}): "))
                    if 2016 <= year <= current_year:
                        break
                    else:
                        print(f"\nEnter a year between 2016 and {current_year}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid year.\n")
            df_filtered = df.loc[df['Order Date'].dt.year == year].copy()
            print('\naveraging orders...')
            time.sleep(0.5)
            orders_per_customer_filtered = df_filtered.groupby('CustID')['Order Number'].nunique()
            average_orders_per_customer_filtered = orders_per_customer_filtered.mean()
            print('averaging spending...')
            time.sleep(0.5)
            df_filtered['Total Spending'] = df_filtered['Purchased Quantity'] * df_filtered['Product Unit Price']
            total_spending_per_customer_filtered = df_filtered.groupby('CustID')['Total Spending'].sum()
            average_spending_per_customer_filtered = total_spending_per_customer_filtered.mean()
            print('calculating popularity...')
            time.sleep(0.5)
            customers_per_product = df_filtered.groupby('ProductID')['CustID'].nunique()
            most_customers_product_id = customers_per_product.idxmax()
            most_customers_count = customers_per_product.max()
            total_amount_bought = df_filtered.loc[
            df_filtered['ProductID'] == most_customers_product_id, 'Purchased Quantity'].sum()
            print(f"\nThe average number of orders per customer in {year} is {average_orders_per_customer_filtered:.2f}")
            print(f"The average spending per customer in {year} is {average_spending_per_customer_filtered:,.2f}")
            print(f"The most popular product is ProductID {most_customers_product_id} with {most_customers_count} unique customers buying a total amount of {total_amount_bought} in {year}.\n")
            ener = input("Press enter to continue")
        if READINGaction == 'O4':
            print('\nstarting calculation ...')
            time.sleep(0.5)
            AUTOSQLQUERY = '''SELECT o.StoreID, o.`Order Date`, o.`Order Number`, li.`Line Item`, li.ProductID, li.`Purchased Quantity`, p.`Product Unit Cost`, p.`Product Unit Price` FROM ongzachary_221252k_project.order o INNER JOIN lineitem li ON o.`Order Number` = li.`Order Number` INNER JOIN product p ON li.ProductID = p.ProductID;'''
            df, _ = NONTABLEREADQuery(cursor, AUTOSQLQUERY, ())
            print('summing up sales ...')
            time.sleep(0.5)
            df['Total Sales'] = df['Product Unit Price'] * df['Purchased Quantity']
            store_sales = df.groupby('StoreID')['Total Sales'].sum()
            most_sales_store_id = store_sales.idxmax()
            most_sales_amount = store_sales.max()
            print('making profits ...')
            time.sleep(0.5)
            df['Profit'] = (df['Product Unit Price'] - df['Product Unit Cost']) * df['Purchased Quantity']
            store_profits = df.groupby('StoreID')['Profit'].sum()
            most_profit_store_id = store_profits.idxmax()
            most_profit_amount = store_profits.max()
            print('tallying up orders ...')
            time.sleep(0.5)
            store_orders = df.groupby('StoreID').agg(Order_Count=('Order Number', 'nunique'))
            most_orders_store_id = store_orders['Order_Count'].idxmax()
            most_orders_count = store_orders['Order_Count'].max()
            print(f"\nThe store that made the most sales to date is store {most_sales_store_id} with a total sales amount of {most_sales_amount:,.2f}.")
            print(f"The store that made the most profit to date is store {most_profit_store_id} with a total profit amount of {most_profit_amount:,.2f}.")
            print(f"The store that fulfilled the most orders to date is store {most_orders_store_id} with a total of {most_orders_count} orders.\n")
            subMM = '''
        --- filter ---
            
        1) Store ID
        2) year
            
        --- Exit ---
        
        3) <---- Back     
        
            '''
            print(subMM)
            YN = str(input('\nPcik a filter to view more data'))
            if YN == '1':
                while True:
                    try:
                        SQLQUERY = '''SELECT * FROM ongzachary_221252k_project.store;'''
                        NONTABLEREADQuery(cursor, SQLQUERY, ())
                        SC = cursor.rowcount
                        print(f'\nThere are currently {SC} stores worldwide.\n')
                        Parameter = int(input("Enter Store ID: "))
                        if 1 <= Parameter <= SC:
                            break
                        else:
                            print(f"\nInvalid input. Enter a Store ID between 1 and {SC}.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid integer.\n")
                df_filtered = df.loc[df['StoreID'] == Parameter].copy()
                print('\nsumming up sales ...')
                time.sleep(0.5)
                df_filtered['Total Sales'] =  df_filtered['Product Unit Price'] *  df_filtered['Purchased Quantity']
                sales = df_filtered['Total Sales'].sum()
                print('making profits ...')
                time.sleep(0.5)
                df_filtered['Profit'] = ( df_filtered['Product Unit Price'] -  df_filtered['Product Unit Cost']) *  df_filtered['Purchased Quantity']
                profit = df_filtered['Profit'].sum()
                print('tallying up orders ...')
                time.sleep(0.5)
                orders_fulfilled = df_filtered['Order Number'].nunique()
                print(f"\nTotal sales for store {Parameter}: {sales:,.2f}")
                print(f"Total profit for store {Parameter}: {profit:,.2f}")
                print(f"Number of orders fulfilled for store {Parameter}: {orders_fulfilled}\n")
                ener = input("Press enter to continue")
            elif YN == '2':
                df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
                df = df.dropna(subset=['Order Date'])
                current_year = datetime.now().year
                while True:
                    try:
                        year = int(input(f"\nEnter year (2016-{current_year}): "))
                        if 2016 <= year <= current_year:
                            break
                        else:
                            print(f"\nEnter a year between 2016 and {current_year}.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid year.\n")
                df_filtered = df.loc[df['Order Date'].dt.year == year].copy()
                print('\nsumming up sales ...')
                time.sleep(0.5)
                df_filtered['Total Sales'] = df_filtered['Product Unit Price'] * df_filtered['Purchased Quantity']
                store_sales = df_filtered.groupby('StoreID')['Total Sales'].sum()
                most_sales_store_id = store_sales.idxmax()
                most_sales_amount = store_sales.max()
                print('making profits ...')
                time.sleep(0.5)
                df_filtered['Profit'] = (df_filtered['Product Unit Price'] - df_filtered['Product Unit Cost']) * df_filtered['Purchased Quantity']
                store_profits = df_filtered.groupby('StoreID')['Profit'].sum()
                most_profit_store_id = store_profits.idxmax()
                most_profit_amount = store_profits.max()
                print('tallying up orders ...\n')
                time.sleep(0.5)
                store_orders = df_filtered.groupby('StoreID').agg(Order_Count=('Order Number', 'nunique'))
                most_orders_store_id = store_orders['Order_Count'].idxmax()
                most_orders_count = store_orders['Order_Count'].max()
                print(f"\nThe store that made the most sales in {year} is store {most_sales_store_id} with a total sales amount of ${most_sales_amount:,.2f}.")
                print(f"The store that made the most profit in {year} is store {most_profit_store_id} with a total profit amount of ${most_profit_amount:,.2f}.")
                print(f"The store that fulfilled the most orders in {year} is store {most_orders_store_id} with a total of {most_orders_count} orders.\n")
                ener = input("Press enter to continue")
            elif YN == '3':
                printrandomline(username)
                time.sleep(1)
                print('backing out ...')
                READING(username, connection, cursor)
        if READINGaction == 'S1':
            while True:
                try:
                    Parameter = int(input("Enter product ID: "))
                    break
                except ValueError:
                    print("Invalid input. Enter a valid integer.")
            SQLQuery = ''' SELECT TotalProductUnitCost AS 'Total Product Expense', `TotalProductUnitPrice(Sales)` AS 'Total Product Sales', (`TotalProductUnitPrice(Sales)` - TotalProductUnitCost) AS 'Total Product Profit' FROM totalsales WHERE ProductID = %s ; '''
            print('\ntallying up expense ...')
            time.sleep(0.5)
            print('summing sales ...')
            time.sleep(0.5)
            print('praising profits ...')
            time.sleep(0.5)
            print('performance evaluated.')
            print('\n')
            print(f'Financial Performance of productID: {Parameter}')
            Readquery(cursor, SQLQuery, (Parameter,))
            print('\n')
            print('Performance of product is satisfactory.')
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'S2':
            Parameter = input("Enter Product Name: ")
            SQLQuery = ''' SELECT TotalProductUnitCost AS 'Total Product Expanse', `TotalProductUnitPrice(Sales)` AS 'Total Product Sales', (`TotalProductUnitPrice(Sales)` - TotalProductUnitCost) AS 'Total Product Profit' FROM totalsales JOIN product ON totalsales.ProductID = product.ProductID WHERE `Product Name` = %s ; '''
            print('\ntallying up expense ...')
            time.sleep(0.5)
            print('summing sales ...')
            time.sleep(0.5)
            print('praising profits ...')
            time.sleep(0.5)
            print('performance evaluated.')
            print('\n')
            print(f'Financial Performance of {Parameter}')
            Readquery(cursor, SQLQuery, (Parameter,))
            print('\n')
            print('Performance of product is satisfactory.')
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'S3':
            SQLQuery = ''' SELECT SUM(TotalProductUnitCost) AS 'Total Company Expense to date', SUM(`TotalProductUnitPrice(Sales)`) AS 'Total Company Sales to date', SUM(`TotalProductUnitPrice(Sales)` - TotalProductUnitCost) AS 'Total Company Profit to date' FROM totalsales; '''
            print('\ntallying up company expenses ...')
            time.sleep(0.5)
            print('summing up sales ...')
            time.sleep(0.5)
            print('chasing profits ...')
            time.sleep(0.5)
            print('compnay performance evaluated.')
            print('\n')
            print('Financial Performance of company to date')
            pd.options.display.float_format = '{:,.2f}'.format  # format float values to integers
            Readqueryint(cursor, SQLQuery, ())
            print('\n')
            print('Performance of compnay is satisfactory.')
            print('\n')
            ener = input("Press enter to continue")
        if READINGaction == 'S4':
            print('\nasking for data ...')
            time.sleep(0.5)
            AUTOSQLQUERY = '''SELECT lineitem.`Order Number`, lineitem.`Line Item`, product.ProductID, lineitem.`Purchased Quantity`, product.`Product Unit Cost`, product.`Product Unit Price`, ongzachary_221252k_project.`order`.`Order Date` FROM lineitem JOIN product ON lineitem.ProductID = product.ProductID JOIN ongzachary_221252k_project.`order` ON lineitem.`Order Number` = ongzachary_221252k_project.`order`.`Order Number` WHERE YEAR( ongzachary_221252k_project.`order`.`Order Date`);'''
            df, _  = NONTABLEREADQuery(cursor, AUTOSQLQUERY, ())
            df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
            df = df.dropna(subset=['Order Date'])
            current_year = datetime.now().year
            while True:
                print('filter by year to view more data')
                try:
                    year = int(input(f"\nEnter year (2016-{current_year}): "))
                    if 2016 <= year <= current_year:
                        break
                    else:
                        print(f"\nEnter a year between 2016 and {current_year}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid year.\n")
            df_filtered = df.loc[df['Order Date'].dt.year == year].copy()
            df_filtered['Total Expense for year'] = df_filtered['Purchased Quantity'] * df_filtered['Product Unit Cost']
            df_filtered['Total Sales for year'] = df_filtered['Purchased Quantity'] * df_filtered['Product Unit Price']
            df_filtered['Total Profit for year'] = df_filtered['Total Sales for year'] - df_filtered['Total Expense for year']
            totalexpense = df_filtered['Total Expense for year'].sum()
            totalsales = df_filtered['Total Sales for year'].sum()
            totalprofit = df_filtered['Total Profit for year'].sum()
            unique_orders = df_filtered['Order Number'].nunique()
            averagesales = totalsales / unique_orders
            print(f'\nTotal Expense for year {year}: {totalexpense:.2f}')
            print(f'Total Sales for year {year}: {totalsales:.2f}')
            print(f'Total Profit for year {year}: {totalprofit:.2f}')
            print(f'Total Orders for year {year}: {unique_orders}')
            print(f'Average Sales for year {year}: {averagesales:.2f}\n')
            ener = input("Press enter to continue")
        if READINGaction == 'B1':
            printrandomline(username)
            time.sleep(1)
            print('backing out ...')
            MP(username, connection, cursor)




def UPDATING(username, connection, cursor):
    while True:
        print('\nThis is the menu to update and amend certian data.')
        MM4 = '''
    --- Customer ---

    C1)Update customer's residence based on customer ID
    C2)Update customer's info based on customer ID
    
    --- Product ---
    
    P1)Update product's price based on product ID
    P2)Update all product's total purchase quantity
    P3)Update all product's financial data
    
    --- Exit ---
        
    B1)<---- Back 
        '''
        print(MM4)
        UPaction = str(input("Do at least one of the following actions besides exiting or backtracking."))
        if UPaction == 'C1':
            while True:
                try:
                    SQLQUERY = '''SELECT * FROM customer;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    CC = cursor.rowcount
                    print(f'There are currently {CC} customers.')
                    Parameter = int(input("\nEnter customer ID: "))
                    if 1 <= Parameter <= CC:
                        break
                    else:
                        print(f"\nInvalid input. Enter a customer ID between 1 and {CC}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid integer.\n")
            SQLQuery = '''SELECT * FROM customer WHERE CustID = %s'''
            CUSTSEARCH = Readquery(cursor, SQLQuery, (Parameter,))
            if not CUSTSEARCH:
                print(f"No customer found for customer ID: {Parameter}")
            else:
                if CUSTSEARCH:
                    UPDATE = str(input(f"\nDo you really want to update customer {Parameter}'s residence info ? (Y/N)"))
                    if UPDATE == 'Y':
                        print(f"--- Updating Customer's Residence Info ---")
                        while True:
                            AA = input("Enter customer continent: ").strip()
                            if AA == "":
                                AA = None
                                print('\ninfo remains the same\n')
                                break
                            elif AA.isalpha():  # Check if the input contains only alphabetic characters
                                break
                            else:
                                print("\nInvalid input. Enter a valid customer continent (or blank to leave it unchanged).\n")
                        while True:
                            BB = input("Enter customer country: ").strip()
                            if BB == "":
                                BB = None
                                print('\ninfo remains the same\n')
                                break
                            elif BB.isalpha():  # Check if the input contains only alphabetic characters
                                break
                            else:
                                print("\nInvalid input. Enter a valid customer country (or blank or blank to leave it unchanged).\n")
                        while True:
                            CC = input("Enter customer city: ")
                            if CC == "":
                                CC = None
                                print('\ninfo remains the same\n')
                                break
                            elif CC.isalpha():  # Check if the input contains only alphabetic characters
                                break
                            else:
                                print("\nInvalid input. Enter a valid customer city (or blank to leave it unchanged).\n")
                        while True:
                            DD = input("Enter customer state: ")
                            if DD == "":
                                DD = None
                                print('\ninfo remains the same\n')
                                break
                            elif DD.isalpha():  # Check if the input contains only alphabetic characters
                                break
                            else:
                                print("\nInvalid input. Enter a valid customer state (or blank to leave it unchanged).\n")
                        while True:
                            EE = input("Enter customer state code: ")
                            if EE == "":
                                EE = None
                                print('\ninfo remains the same\n')
                                break
                            elif EE.isalpha():  # Check if the input contains only alphabetic characters
                                break
                            else:
                                print("\nInvalid input. Enter a valid customer state code (or blank to leave it unchanged).\n")
                        while True:
                            FF = input("Enter customer zip code: ").strip()
                            if FF == "":
                                print("\nInvalid input. Enter a valid customer zip code. Customer at the very least moved house\n")
                            else:
                                break
                        params = (AA, BB, CC, DD, EE, FF, Parameter)
                        UPQUERY = '''
                        UPDATE customer SET
                            `Cust Continent` = COALESCE(%s, `Cust Continent`),
                            `Cust Country` = COALESCE(%s, `Cust Country`),
                            `Cust City` = COALESCE(%s, `Cust City`),
                            `Cust State` = COALESCE(%s, `Cust State`),
                            `Cust State Code` = COALESCE(%s, `Cust State Code`),
                            `Cust Zip Code` = COALESCE(%s, `Cust Zip Code`)
                        WHERE CustID = %s;
                        '''
                        ADDONLYSQL(cursor, UPQUERY, params)
                        connection.commit()
                        SQLQuery = '''SELECT * FROM customer WHERE CustID = %s ;'''
                        print('\n')
                        print("Updated customer's Residence Info")
                        Readquery(cursor, SQLQuery, (Parameter,))
                        print('\n')
                        ener = input("Press enter to continue")
                    if UPDATE == 'N':
                        print("customer's residence info not updated, do they still live where they say they live?")
                        print('\n')
                        ener = input("Press enter to continue")
                        UPDATING(username, connection, cursor)
        if UPaction == 'C2':
            while True:
                try:
                    SQLQUERY = '''SELECT * FROM customer;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    CC = cursor.rowcount
                    print(f'There are currently {CC} customers.')
                    Parameter = int(input("\nEnter customer ID: "))
                    if 1 <= Parameter <= CC:
                        break
                    else:
                        print(f"\nInvalid input. Enter a customer ID between 1 and {CC}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid integer.\n")
            SQLQuery = '''SELECT * FROM customer WHERE CustID = %s'''
            CUSTSEARCH = Readquery(cursor, SQLQuery, (Parameter,))
            if not CUSTSEARCH:
                print(f"No customer found for customer ID: {Parameter}")
            else:
                if CUSTSEARCH:
                    UPDATE = str(input(f"\nDo you really want to update customer {parameter}'s info ? (Y/N)"))
                if UPDATE == 'Y':
                    print(f"--- Updating Customer's Info ---")
                    while True:
                        PB = input("Enter customer Name: ").strip()
                        if PB == "":
                            PB = None
                            print('\ninfo remains the same\n')
                            breakad
                        elif re.match(r'^[a-zA-Z\s]+$', PB):
                            break
                        else:
                            print("\nInvalid input. Enter a valid customer name (or blank to leave it unchanged).\n")
                    while True:
                        PC = input("Enter customer gender (Male/Female): ").strip()
                        if PC == "":
                            PC = None
                            print('\ninfo remains the same\n')
                            break
                        elif PC in ['Male', 'Female']:
                            break
                        else:
                            print("\nInvalid input. Enter a valid customer gender (or blank to leave it unchanged).\n")
                    while True:
                        PD = input("Enter customer birthday (YYYY-MM-DD): ").strip()
                        if PD == "":
                            PD = None
                            print('\ninfo remains the same\n')
                            break
                        elif re.match(r'^\d{4}-\d{2}-\d{2}$', PD):
                            year, month, day = map(int, PD.split('-'))
                            if 1 <= month <= 12 and 1 <= day <= 31:
                                break
                            else:
                                print("\nInvalid input. Invalid date. Enter a valid date in YYYY-MM-DD format.\n")
                        else:
                            print("\nInvalid input. Enter a valid date in YYYY-MM-DD format.\n")
                    params = (PB, PC, PD, Parameter)
                    UPQUERY = '''
                    UPDATE customer SET
                        `Cust Name` = COALESCE(%s, `Cust Name`),
                        `Cust Gender` = COALESCE(%s, `Cust Gender`),
                        `Cust Birthday` = COALESCE(%s, `Cust Birthday`)
                    WHERE CustID = %s;
                    '''
                    ADDONLYSQL(cursor, UPQUERY, params)
                    connection.commit()
                    SQLQuery = '''SELECT * FROM customer WHERE CustID = %s ;'''
                    print('\n')
                    print("Updated Customer's Info")
                    Readquery(cursor, SQLQuery, (Parameter,))
                    print('\n')
                    ener = input("Press enter to continue")
                if UPDATE == 'N':
                    print("Customer's info not updated, are they who they say they are?")
                    print('\n')
                    ener = input("Press enter to continue")
                    UPDATING(username, connection, cursor)
        if UPaction == 'P1':
            while True:
                try:
                    SQLQUERY = '''SELECT * FROM product;'''
                    NONTABLEREADQuery(cursor, SQLQUERY, ())
                    PC = cursor.rowcount
                    print(f'\nThere are currently {PC} products.\n')
                    Parameter = int(input(f"Enter Product ID: "))
                    if 1 <= Parameter <= PC:
                        break
                    else:
                        print(f"\nInvalid input. Enter a product ID between 1 and {PC}.\n")
                except ValueError:
                    print("\nInvalid input. Enter a valid integer.\n")
            SQLQuery = '''SELECT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Category`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price` FROM product WHERE ProductID = %s ;'''
            ProSearch = Readquery(cursor, SQLQuery, (Parameter,))
            if not ProSearch:
                print(f"No product found for ProductID: {Parameter}")
            else:
                if ProSearch:
                    UPDATE = str(input(f"\nDo you really want to update product {Parameter}'s price ? (Y/N)"))
                if UPDATE == 'Y':
                    print(f"--- Updating product's price ---")
                    while True:
                        user_input = input('Enter product unit cost: ')
                        if user_input == '':
                            A1 = None
                            ('\ninfo remains the same\n')
                            break
                        try:
                            A1 = float(user_input)
                            if len(str(A1).split('.')[1]) > 2:
                                print("\nPlease enter a value with no more than 2 decimal places.\n")
                            break
                        except ValueError:
                            print("\nInvalid input. Please enter a valid cost (or blank to leave it unchanged).\n")
                    while True:
                        user_input = input('Enter product unit Price: ')
                        if user_input == '':
                            A2 = None
                            ('\ninfo remains the same\n')
                            break
                        try:
                            A2 = float(user_input)
                            if len(str(A2).split('.')[1]) > 2:
                                print("\nPlease enter a value with no more than 2 decimal places.\n")
                            break
                        except ValueError:
                            print("\nInvalid input. Please enter a valid price (or blank to leave it unchanged).\n")
                    cursor.execute("START TRANSACTION;")
                    params = (A1, A2, Parameter)
                    UPQUERY = '''UPDATE product SET `Product Unit Cost` = COALESCE(%s, `Product Unit Cost`), `Product Unit Price` = COALESCE(%s, `Product Unit Price`) WHERE ProductID = %s;'''
                    ADDONLYSQL(cursor, UPQUERY, params)
                    connection.commit()
                    totalsales_params = (A1, A2, Parameter)
                    totalsales_query = '''UPDATE totalsales SET `Product Unit Cost` = COALESCE(%s, `Product Unit Cost`), `Product Unit Price` = COALESCE(%s, `Product Unit Price`) WHERE ProductID = %s;'''
                    ADDONLYSQL(cursor, totalsales_query, totalsales_params)
                    connection.commit()
                    SQLQuery = '''SELECT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Category`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price` FROM product WHERE ProductID = %s ;'''
                    print('\n')
                    print("Updated product price")
                    Readquery(cursor, SQLQuery, (Parameter,))
                    print('\npray this change keeps our profits margin wide')
                    print('\n')
                    ener = input("Press enter to continue")
                if UPDATE == 'N':
                    print("Are you sure profits can keep up with inflation?")
                    print('\n')
                    ener = input("Press enter to continue")
                    UPDATING(username, connection, cursor)
        if UPaction == 'P2':
            BUQ = "SELECT ProductID, TotalPurchasedQuantity FROM product"
            BU, _ = NONTABLEREADQuery(cursor, BUQ, ())
            print('\nUpdating records...')
            time.sleep(0.5)
            cursor.execute("START TRANSACTION;")
            update_query = """UPDATE product p JOIN (SELECT ProductID, SUM(`Purchased Quantity`) AS TotalPurchasedQuantity FROM lineitem GROUP BY ProductID) l ON p.ProductID = l.ProductID SET p.TotalPurchasedQuantity = l.TotalPurchasedQuantity;"""
            ADDONLYSQL(cursor, update_query, ())
            UPQ = '''UPDATE totalsales ts JOIN (SELECT ProductID, SUM(`Purchased Quantity`) AS TotalPurchasedQuantity FROM lineitem GROUP BY ProductID) l ON ts.ProductID = l.ProductID SET ts.TotalPurchasedQuantity = l.TotalPurchasedQuantity;'''
            ADDONLYSQL(cursor, UPQ, ())
            connection.commit()
            AUQ = "SELECT ProductID, TotalPurchasedQuantity FROM product"
            AU, _ = NONTABLEREADQuery(cursor, AUQ, ())
            print('comparing differences...')
            time.sleep(0.5)
            changes = []
            before_dict = {item['ProductID']: item['TotalPurchasedQuantity'] for item in BU.to_dict('records')}
            for item in AU.to_dict('records'):
                product_id = item['ProductID']
                new_quantity = item['TotalPurchasedQuantity']
                old_quantity = before_dict.get(product_id)
                if old_quantity != new_quantity:
                    changes.append({'ProductID': product_id, 'OldQuantity': old_quantity, 'NewQuantity': new_quantity})
            if changes:
                print('showing change...')
                time.sleep(0.5)
                df_changes = pd.DataFrame(changes)
                table = tabulate.tabulate(df_changes, headers='keys', tablefmt='fancy_grid', showindex=False)
                print('\n')
                print(table)
                print("\nchanges detected, update product's financial data")
                print('\n')
                ener = input("Press enter to continue")
            else:
                print('showing change...')
                time.sleep(0.5)
                print("\nNo changes detected.\n")
                ener = input("Press enter to continue")
        if UPaction == 'P3':
            BUQ = "SELECT * FROM totalsales"
            BU, _ = NONTABLEREADQuery(cursor, BUQ, ())
            print('\nUpdating records...')
            time.sleep(0.5)
            update_query = """UPDATE totalsales SET TotalProductUnitCost = TotalPurchasedQuantity * `Product Unit Cost`, `TotalProductUnitPrice(Sales)` = TotalPurchasedQuantity * `Product Unit Price`"""
            ADDONLYSQL(cursor, update_query, ())
            connection.commit()
            AUQ = "SELECT * FROM totalsales"
            AU, _ = NONTABLEREADQuery(cursor, AUQ, ())
            print('comparing differences...')
            time.sleep(0.5)
            # Calculate the changes
            changes = []
            before_dict = {item['ProductID']: item for item in BU.to_dict('records')}
            for item in AU.to_dict('records'):
                product_id = item['ProductID']
                new_values = item
                old_values = before_dict.get(product_id)
                if old_values:
                    if (old_values['TotalProductUnitCost'] != new_values['TotalProductUnitCost'] or old_values['TotalProductUnitPrice(Sales)'] != new_values['TotalProductUnitPrice(Sales)']):
                        changes.append({'ProductID': product_id, 'OldTotalProductUnitCost': old_values['TotalProductUnitCost'], 'NewTotalProductUnitCost': new_values['TotalProductUnitCost'], 'OldTotalProductUnitPrice': old_values['TotalProductUnitPrice(Sales)'], 'NewTotalProductUnitPrice': new_values['TotalProductUnitPrice(Sales)']})
            if changes:
                print('showing change...')
                time.sleep(0.5)
                df_changes = pd.DataFrame(changes)
                table = tabulate.tabulate(df_changes, headers='keys', tablefmt='fancy_grid', showindex=False)
                print('\n')
                print(table)
                print("\nChanges detected, new data avaliable to view")
                print('\n')
                ener = input("Press enter to continue")
            else:
                print('showing change...')
                time.sleep(0.5)
                print("\nNo changes detected.\n")
                ener = input("Press enter to continue")
        if UPaction == 'B1':
            printrandomline(username)
            time.sleep(1)
            print('backing out ...')
            MP(username, connection, cursor)



def subfunctionA(username, connection, cursor):
    # 3 N's to get kicked out... just continue to press invaild inputs till you understand what you are doing
    max_attempts = 3
    n_count = 0
    while True:
        print('\nThis menu contains dangerous options. Are you sure you know what you are doing?' + "\n" * 11)
        acknowledge = str(input("Proceed? (Y/N): "))
        if acknowledge == 'Y':
            print("\n" * 11)
            return 'Y'
        elif acknowledge == 'N':
            n_count += 1
            if n_count >= max_attempts:
                print("You clearly have no idea what you are doing. Get out.")
                print("Maximum acknowledgement attempts reached. Exiting to main menu.")
                MP(username, connection, cursor)
        else:
            print("Invalid input. Enter 'Y' or 'N'.")
            print('\nThis menu contains dangerous options. Are you sure you know what you are doing?' + "\n" * 11)
            acknowledge = str(input("Proceed? (Y/N): "))


def DELETION(username, connection, cursor):
    # everythig here removes something
    global Hero # easter egg
    while True:
        if subfunctionA(username, connection, cursor) == 'Y':
            print('\nThis is the menu to delete, destroy or remove certian data.')
            MM5 = '''        
    --- Store ---
        
    S1)Remove store based on store ID
    
    --- Product ---
    
    P1)Remove product based on product ID
    
    --- Order ---
    
    O1)Remove order based on order number (Refund)
    
    --- WARNING ---
    
    N1)Delete schema 
                '''
            print(MM5)
            #If i am not wrong everything here needs you do a double take, search what you want to delete then delete
            REMOVEaction = str(input("Do at least one of the following actions besides exiting or backtracking."))
            if REMOVEaction == 'S1':
                while True:
                    try:
                        SQLQUERY = '''SELECT * FROM ongzachary_221252k_project.store;'''
                        NONTABLEREADQuery(cursor, SQLQUERY, ())
                        SC = cursor.rowcount
                        print(f'\nThere are currently {SC} stores worldwide.\n')
                        Parameter = int(input("Enter Store ID: ")) # search
                        if 1 <= Parameter <= SC:
                            break
                        else:
                            print(f"\nInvalid input. Enter a Store ID between 1 and {SC}.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid integer.\n")
                SQLQuery = '''SELECT * FROM ongzachary_221252k_project.store where StoreID = %s ;'''
                StoreSearch = Readquery(cursor, SQLQuery, (Parameter,))
                if not StoreSearch:
                    print(f"No store found for StoreID: {Parameter}")
                else:
                    if StoreSearch:
                        DELETE = str(input("\nDo you really want to remove store? (Y/N)")) # delete
                        if DELETE == 'Y':
                            DELETEQUERY = '''DELETE FROM store WHERE StoreID = %s ;'''
                            # NONTABLEREADQuery(cursor, DELETEQUERY, (Parameter,))
                            ADDONLYSQL(cursor, DELETEQUERY, (Parameter,))
                            connection.commit()
                            print('\nStore deleted may it rest in peace')
                            SQLQUERY = '''SELECT * FROM ongzachary_221252k_project.store;'''
                            NONTABLEREADQuery(cursor, SQLQUERY, ())
                            print(f'There are now currently {str(cursor.rowcount)} stores globally.\n')
                            ener = input("Press enter to continue")
                            MP(username, connection, cursor)
                        if DELETE == 'N':
                            print('Store not deleted, may it still bring use riches')
                            print('\n')
                            ener = input("Press enter to continue")
                            MP(username, connection, cursor)
            if REMOVEaction == 'P1':
                while True:
                    try:
                        SQLQUERY = '''SELECT * FROM product;'''
                        NONTABLEREADQuery(cursor, SQLQUERY, ())
                        PC = cursor.rowcount
                        print(f'\nThere are currently {PC} products.\n')
                        Parameter = int(input(f"Enter Product ID: ")) #same here
                        if 1 <= Parameter <= PC:
                            break
                        else:
                            print(f"\nInvalid input. Enter a product ID between 1 and {PC}.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid integer.\n")
                SQLQuery = '''SELECT ProductID, `Product Name`, `Product Brand`, `Product Color`, `Product Category`, `Product Subcategory`, `Product Unit Cost`, `Product Unit Price` FROM product WHERE ProductID = %s ;'''
                ProSearch = Readquery(cursor, SQLQuery, (Parameter,))
                if not ProSearch:
                    print(f"No product found for ProductID: {Parameter}")
                else:
                    if ProSearch:
                        DELETE = str(input("\nDo you really want to remove product? (Y/N)"))
                        if DELETE == 'Y':
                            cursor.execute("START TRANSACTION;")
                            DSQL = '''DELETE FROM product WHERE ProductID = %s ;'''
                            ADDONLYSQL(cursor, DSQL, (Parameter,))
                            DSQL2 = '''DELETE FROM totalsales WHERE ProductID = %s ;'''
                            ADDONLYSQL(cursor, DSQL2, (Parameter,))
                            connection.commit()
                            print('\nProduct deleted may it rest in peace')
                            SQLQUERY = '''SELECT * FROM product;'''
                            NONTABLEREADQuery(cursor, SQLQUERY, ())
                            print(f'There are now currently {str(cursor.rowcount)} products.\n')
                            ener = input("Press enter to continue")
                            MP(username, connection, cursor)
                        if DELETE == 'N':
                            print('Product not deleted, may it still bring use riches')
                            print('\n')
                            ener = input("Press enter to continue")
                            MP(username, connection, cursor)
            if REMOVEaction == 'O1':
                while True:
                    try:
                        AUTOSQLQUERY1 = '''SELECT * FROM ongzachary_221252k_project.order;'''
                        NONTABLEREADQuery(cursor, AUTOSQLQUERY1, ())
                        OC = cursor.rowcount
                        print(f'\nThere are currently {str(cursor.rowcount)} orders.')
                        AUTOORDERSEARCHQUERY = '''SELECT `Order Number` FROM ongzachary_221252k_project.order;'''
                        df, _ = NONTABLEREADQuery(cursor, AUTOORDERSEARCHQUERY, ())
                        min = df['Order Number'].min()
                        max = df['Order Number'].max()
                        print(f"The lastest order number is {max}\n")
                        Parameter = int(input(f"Enter order number: "))
                        if min <= Parameter <= max:
                            break
                        else:
                            print(f"\nInvalid input. Enter a order number between {min} and {max}.\n")
                    except ValueError:
                        print("\nInvalid input. Enter a valid integer.\n")
                SQLQuery = ''' SELECT `Line Item`, p.ProductID, `Purchased Quantity`, p.`Product Unit Cost`, p.`Product Unit Price` FROM lineitem l JOIN product p ON l.ProductID = p.ProductID WHERE `Order Number` = %s ;'''
                print(f"\nOrder Number: {Parameter}")
                OSearch = Readquery(cursor, SQLQuery, (Parameter,))
                if not OSearch:
                    print(f"No order found for order number: {Parameter}")
                else:
                    if OSearch:
                        DELETE = str(input("\nDo you really want to remove/(refund) order? (Y/N)"))
                        if DELETE == 'Y':
                            print('Such a shame the customer asked for money back')
                            cursor.execute("START TRANSACTION;")
                            DSQL = '''DELETE FROM ongzachary_221252k_project.lineitem WHERE `Order Number` = %s ;'''
                            ADDONLYSQL(cursor, DSQL, (Parameter,))
                            DSQL2 = '''DELETE FROM ongzachary_221252k_project.order WHERE `Order Number` = %s ;'''
                            ADDONLYSQL(cursor, DSQL2, (Parameter,))
                            connection.commit()
                            print('\nOrder deleted / Customer refunded')
                            SQLQUERY = '''SELECT * FROM ongzachary_221252k_project.order;'''
                            NONTABLEREADQuery(cursor, SQLQUERY, ())
                            print(f'There are now currently {str(cursor.rowcount)} orders.\n')
                            ener = input("Press enter to continue")
                            MP(username, connection, cursor)
                        if DELETE == 'N':
                            print('Order not deleted, may it our money never part with us')
                            print('\n')
                            ener = input("Press enter to continue")
                            MP(username, connection, cursor)
            if difflib.SequenceMatcher(None, REMOVEaction, 'NUCLEAR OPTION').ratio() == 1: # Easter Egg
                print('WARNING the following option is irreversible! Are you really sure you want to clear the entire Database?')
                print('To confirm, press "Z" and "P" simultaneously.')
                while True:
                    if keyboard.is_pressed('z+p'):
                        print('NUCLEAR OPTION ARMED!')
                        for i in range(5, 0, -1): # Countdown
                            print(i, '...')
                            time.sleep(1)
                            if keyboard.is_pressed('esc'):
                                print('\nCountdown interrupted!')
                                print(f'Achivement Unlocked: "Hero" of the compnay\n') #Easter Egg
                                Hero = True
                                break
                            if i == 1:
                                print('Database Deleted')
                                print("\n" * 12)
                                now = datetime.now()
                                print("\n469 Disgruntled Employee: Database Deletion Detected\n")
                                print(f"{username} pressed the Nuclear option at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                                print(f"HR will be informed about this action, {username} is fired effective immediately") #its a test
                                print('Logging out ...\n')
                                print("\n" * 12)
                                time.sleep(1)
                                print("\n" * 12)
                                login_to_system()
                    elif keyboard.is_pressed('esc'):
                        print('Nuclear option cancelled. Database NOT Deleted')
                        MP(username, connection, cursor)
                        break # easter egg
            elif difflib.SequenceMatcher(None, REMOVEaction, 'NUCLEAR OPTION').ratio() > 0.8: #spell check
                print('Invalid Nuclear Code. Try Again')
                now = datetime.now()
                print("\n468 Disgruntled Employee: Atemptted Database Deletion\n")
                print(f"{username} attempted to press the Nuclear Option at {now.strftime('%Y-%m-%d %H:%M:%S')}")
                MP(username, connection, cursor)


def MP(username, connection, cursor):
    global ogpassword, storedsalt, storedhashedpassword # import global variable from above
    while True:
        if Hero == False:
            print(f"\nCompany is behind quota. Work harder, {username}")
        if Hero == True:
            print(f"\ncongratulations {username} you saved the company, how did you figure out this easter egg") #Easter Egg
        MM1 = '''
--- Main Menu ---
    
    1) CREATE
    2) READ
    3) UPDATE
    4) DELETE

--- Others ---

    5) RESET or CHANGE PASSWORD
    6) LOGOUT
    7) EXIT
        '''
        print(MM1)
        action = str(input("Do at least one of the following actions besides exiting: CREATE, READ, UPDATE or DELETE"))
        if action.lower() in ['exit', 'e', '7']:
            #Literal Exit
            now = datetime.now()
            print("\n408 Request Timeout: Disconnected from the database")
            print(f"{username} exited program at {now.strftime('%Y-%m-%d %H:%M:%S')}") # captures time
            print("Exiting program. Go back to work slacker")
            connection.close()
            exit(1)
        elif action.lower() in ['logout', 'l', '6']:
            # Logout
            now = datetime.now()
            print("\n408 Request Timeout: Disconnected from the database\n")
            print(f"{username} logged out at {now.strftime('%Y-%m-%d %H:%M:%S')}") # captures time
            print('Logging out ...\n')
            connection.close()
            storedsalt, storedhashedpassword = hashedpassword(ogpassword)
            time.sleep(1)
            login_to_system()
        elif action.lower() in ['reset', 'r', '5']:
            NEWPASSWORDINPUT = str(input('Enter new password: ')) # takes new plain text password
            newsalt, newhashedpassword = hashedpassword(NEWPASSWORDINPUT) # run the new password through the hashing
            SS(NEWPASSWORDINPUT) #encryprt and send password to text file
            storedsalt = newsalt
            storedhashedpassword = newhashedpassword # change variables
            print(f'\npassword has been changed. Logging out {username}.')
            now = datetime.now()
            print("\n408 Request Timeout: Disconnected from the database\n")
            print(f"{username} logged out at {now.strftime('%Y-%m-%d %H:%M:%S')}") # captures time
            print('Logging out ...\n')
            connection.close()
            SK, SCP = RS()
            ogpassword = DP(SK, SCP)
            login_to_system() # login again
        else:
            if action.lower() in ['create', 'c', '1']:
                CREATION(username, connection, cursor) #C
            elif action.lower() in ['read', 'r', '2']:
                READING(username, connection, cursor) #R
            elif action.lower() in ['update', 'u', '3']:
                UPDATING(username, connection, cursor) #U
            elif action.lower() in ['delete', 'd', '4']:
                DELETION(username, connection, cursor) #D
            else:
                print("Invalid action. Try again.") #catch invaild inputs
                print("\n" * 12)


def login_to_system():
    # techincally this is the third function to run, gives 3 attempts for username and password
    max_attempts = 3
    username_attempts = 0
    mm0 = '''
    --- Login menu ---
    '''
    print(mm0)
    while username_attempts < max_attempts:
        username = input("\tEnter username: ").strip()
        if username.lower() == 'esc':
            BUP(username, None, None) # BIOS settings for app (its just backups)
            return
        print("\n" * 12)
        if username == "admin":
            password_attempts = 0
            while password_attempts < max_attempts:
                inputpassword = input("\tEnter password: ")
                print("\n" * 12)
                connection, cursor = connect_to_db(username, inputpassword)
                if cursor is not None:
                    now = datetime.now()
                    print(f"{username} logged on at {now.strftime('%Y-%m-%d %H:%M:%S')}") # captures when user logs on
                    print('Logging in ...\n')
                    MP(username, connection, cursor) # now you are actually in the program
                    return
                else:
                    password_attempts += 1
                    print(f"Invalid password. Attempt {password_attempts}/{max_attempts}")
            print("Maximum password attempts reached. Exiting program.")
            exit(1)
        else:
            username_attempts += 1
            print(f"Invalid username. Attempt {username_attempts}/{max_attempts}")
            if username_attempts >= max_attempts:
                print("Maximum username attempts reached. Exiting program.")
                exit(1)


login_to_system()#3
