import sqlite3

###FUNCTIONS###
# Function that adds a book with 4 fields into table 'books'
def add_book(): 

    # While loop  + try/except that requires user to enter values again if they are not valid
    while True:
        try:
            
            # Create variables that represent each field value, obtained from user input
            id = int(input('Enter the ID of this book: ')) # ID
            title = input('Enter the title of this book: ') # Title
            author = input('Enter the author of this book: ') # Author
            qty = int(input ('Enter the quantity of these book(s): ')) # quantity

            # Insert values into books with the above variables
            cursor.execute('''
            INSERT INTO books VALUES(?,?,?,?)''', (id, title, author, qty))
            print('Entry added') 
            db.commit() # Commit to database
            break # Break out of while loop

        # Stay in while loop if error occurs, print error message
        except:
            print('Error, make sure:\n-ID and quantity are integers\n-ID is unique')


# Function that allows user to update any of the 4 fields of a book item
def update_book(): 

    # Get a list of all current ids
    db.row_factory = lambda cursor, row: row[0]
    c=db.cursor()
    ids = c.execute('SELECT id FROM books').fetchall()

    # While loop + try/except that requires user to enter ID again if it is not valid
    while True:
        try:

            # Ask user to input ID number of the book to be updated
            id = int(input('Enter the ID of the book you wish to update: '))
            if id in ids: # If id exists in database, break
                break
            else: # If ID does not exist, raise error
                raise KeyError
        except: # If error occurs from the user entering a string/non-existent ID, loop back to while loop
            print('Please enter a valid ID. ')

    # After a valid ID is given, create while loop and ask user to choose field to update
    while True:
        choice = input('Would you like to update the ID, title, author, or quantity?: ').lower()

        # ID
        if choice == 'id':
            while True: # Create sub-while loop + try/except for when invalid ID is entered
                try:
                    new_id = int(input('Enter new ID: ')) # Ask user for new ID
                    if new_id not in ids: # If new ID not in database, update
                        cursor.execute('''
                        UPDATE books SET id = ? WHERE id = ?''',
                        (new_id,id))
                        break # Break out of sub-while loop
                    else:
                        raise KeyError # Raise error if ID already present
                except:
                    print('Please enter a valid new ID. ') # Print error message if error occurs
            break # Break out of while loop

        # Title
        elif choice == 'title':
            new_title = input('Enter new title: ') # Ask user for new title
            cursor.execute(''' 
            UPDATE books SET title = ? WHERE id = ?''',
            (new_title,id)) # Update title
            break # Break out of while loop

        # Author 
        elif choice == 'author':
            new_author = input('Enter new author: ') # Ask user for new author
            cursor.execute('''
            UPDATE books SET author = ? WHERE id = ?''',
            (new_author,id)) # Update author
            break # Break out of while loop
            
        #Quantity
        elif choice == 'quantity':
            while True: # Create sub-while loop + try/except for when invalid quantity is entered
                try:
                    new_quantity = int(input('Enter new quantity: ')) # Ask user for new quantity
                    cursor.execute('''
                    UPDATE books SET qty = ? WHERE id = ?''',
                    (new_quantity,id)) # Update quantity
                    break
                except: # If error occurs, print error message and ask user to enter valid quantity
                    print('Please enter a valid quantity. ') 
            break # Break out of while loop

        # ID, title, author, and quantity not entered. Ask user to enter 1 of those options
        else:
            print('Please choose ID, title, author, or quantity:')          
    db.commit() # Commit to database
    print('Updated')


# Function that deletes a book
def delete_book():

    # Get a list of all current ids
    db.row_factory = lambda cursor, row: row[0]
    c=db.cursor()
    ids = c.execute('SELECT id FROM books').fetchall()
    # Create while loop + try/except for invalid IDs
    while True:
        try:
            id = int(input('Enter the ID of the book to be deleted: ')) # Ask user to enter ID

            # Check if ID exists
            if id in ids:
                cursor.execute('''
                DELETE FROM books WHERE id = ?''', (id,)) # Delete row if ID exists
                db.commit() # Commit to database
                print('Book deleted')
                break # Break out of while loop

            # Raise error if ID does not exist
            else: 
                raise KeyError
            
        # If error occurs, let loop start again and print error message    
        except:
            print('Please enter a valid ID. ')


# Function that searches for a book
def search_book():

    # Get a list of all current ids
    db.row_factory = lambda cursor, row: row[0]
    c=db.cursor()
    ids = c.execute('SELECT id FROM books').fetchall()

    # Create while loop + try/except for invalid IDs
    while True:
        try:
            id = int(input('Search for a book using its ID: ')) # Ask user to enter ID

            # Check if ID exists
            if id in ids:
                cursor.execute('''
                SELECT * FROM books where id = ?''', (id,)) # Select row if ID exists
                book = cursor.fetchone() # Fetch row
                print(f'Here is the book:\n{book}') # Print row
                break  # Break out of while loop

            # Raise error if ID does not exist
            else: 
                raise KeyError   

        # If error occurs, let loop start again and print error message            
        except:
            print('Book not found, please try again. ')


# Function that views whole 'books' table
def view_bookstore():
    cursor.execute('''SELECT * FROM books''')
    table = cursor.fetchall() # Fetch whole table
    print(f'Whole bookstore:\n{table}') # Print table



###MAIN CODE###
db = sqlite3.connect('ebookstore.db') # Create database
cursor=db.cursor() # Get cursor object

# Create table with name 'books'
cursor.execute('''
CREATE TABLE IF NOT EXISTS books(
id INTEGER PRIMARY KEY, title TEXT, author TEXT, 
qty INTEGER)''')
db.commit()

# Create variables to store the initial books in database
id1, id2, id3, id4, id5 = (3001, 3002, 3003, 3004, 3005)
t1, t2, t3, t4, t5 = ('A Tale of Two Cities',
                      "Harry Potter and the Philosopher's Stone",
                      'The Lion, the Witch and the Wardrobe',
                      'The Lord of the Rings',
                      'Alice in Wonderland')
a1, a2, a3, a4, a5 = ('Charles Dickens',
                      'J.K. Rowling',
                      'C.S. Lewis',
                      'J.R.R Tolkien',
                      'Lewis Carroll')
qty1, qty2, qty3, qty4, qty5 = (30, 40, 25, 37, 12)

# Create a list of tuples to enter values
books = [(id1, t1, a1, qty1),
         (id2, t2, a2, qty2),
         (id3, t3, a3, qty3),
         (id4, t4, a4, qty4),
         (id5, t5, a5, qty5),]

# Use try/except to add preliminary books, if already added, except is executed
try:
    # Use executemany to enter book entries into table 
    cursor.executemany('''
    INSERT INTO books VALUES(?,?,?,?)''', books)
    # Confirm it is added and commit changes
    print('Books added')
    db.commit()
except:
    print('Books already added') # Print message to show books already added

while True:
    menu = input('''
Welcome to the ebookstore, select one of the following options below:
e - Enter a book
u - Update a book
d - Delete a book
s - Search for a book
v - View ebookstore)
0 - Exit
''')
    if menu == 'e':
        add_book() # Call function add_book()
        
    elif menu == 'u': 
        update_book() # Call function update_book()

    elif menu == 'd': 
        delete_book() # Call function delete_book()

    elif menu == 's': 
        search_book() # Call function search_book()
    
    elif menu == 'v':
        view_bookstore() # Call function view-bookstore()
        
    elif menu == '0': # Exit program
        print('Goodbye!!!')
        break
    
    else: # Default case
        print("You have made a wrong choice, please try again:") 

db.close() # Close database