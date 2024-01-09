'''  Name: LAVANYA SASIKALA
     Student ID: 156621211
     Assignment
    This program implements a store stock calculator for a small business. The program takes a csv file as the input which has the 
    current stock details for each item. The program needs to read the csv file and print it in a readble table format. It then asks the user
    for an input which takes the item number to indicate the sale. Each time the user enters the item number, the current stock will 
    decrement by 1. If the item's stock value is zero, and if the user enters the item number to indicate, the sale then use another variable
    to indicate that the sale is lost and increment the variable by 1 each time a hit is made to that item. When the cashier enters 'e' it 
    indicates the end of the day and then 3 tables needs to be printed.
    i) The Total Sales Table: This is simply a table which indicates the total sales, including totals for each item, and a grand total:
    ii) The Lost Sales Table: These are sales that were lost because of missing stock. 
    iii) Restock Report: This report will tell the manager how many of each item will be needed to address the current demand. The restock 
    should also add an additional 20% for each item (rounded to the nearest integer) to account for variation in demand:

'''



import csv
import sys


def read_stock_file(filename):         
    '''This functions reads the csv file and convert the file contents to a list of dictionaries and returns it'''
    stock_list = []                  # Initializing an empty list.
    f = open('stock.csv ','r')       #Opening the csv file in read mode.
    reader = csv.DictReader(f)       # Import the contents of th ecsv file into a list of dictionaries.
    for row in reader:          
        row['Lost Item']=0           # Added two more headers 'Lost Item' and 'Sales'to the csv file for further processing of the contents.
        row['Sales'] = 0
        stock_list.append(row)       # Appending each row of the csv file to the list.
    f.close                          #Closing the file
    return stock_list


def write_stock_file(stock_list):

    '''This function converts a list of dictionaries into the contents of a csv file. After processing,
    this dictionary has two new headers (Lost_Item & Sales added in the read_stock_file function'''

    filename = 'stock_status.csv'       # The new csv file name
    f=open(filename,'w')                #Opening the file in write mode
    fieldnames = stock_list[0].keys()   # The fieldnames are the keys of the first list
    w = csv.DictWriter(f,fieldnames=fieldnames)  # The fieldnames are written 
    w.writeheader()
    for row in stock_list:                      # The dictionaries are writtn to the csv file
        w.writerow(row)
    
    f.close()


def create_new_csv(input_file_path, output_file_path):

    '''While reading the csv file , 2 headers were additionally added to the csv file.
    The write_stock_file creates the updated csv with the 2 new headers also. But the requirement is to
    update the original csv file. So this function creates the updated csv file with the original headers from the csv file 
    created by the above function write_stock_file.'''
    
    with open(input_file_path, 'r') as infile:     # open the existing CSV (the output of the function write_stock_filr) in read mode
        reader = csv.DictReader(infile)
        
        data = []                                   # A list is initaillized for appending the required file contents. 
        for row in reader:                         # extract the required columns from the existing file
            item = row['Item']
            current_stock = row['Current Stock']
            price_per_item = row['Price per Item']
            previous_sale = row['Sales']                 #The previous sales is now the sales column in the updated csv file.
            data.append({'Item': item, 'Current Stock': current_stock, 'Price per Item': price_per_item, 'Previous Sales': previous_sale})

   
    with open(output_file_path, 'w', newline='') as outfile:      # open the new CSV file for writing
        writer = csv.DictWriter(outfile, fieldnames=['Item', 'Current Stock', 'Price per Item', 'Previous Sales'])

        
        writer.writeheader()                            # writing the headers to the new file
         
        for row in data:                                 # writing the extracted data to the new file
            writer.writerow(row)

      

   


def print_stock(stock_list,tablenum):

    ''' This function performs the entire printing. It takes the stock_list and an integer as the parameters
      and the type of table to be printed  is determined b the integer tablenum.'''
    

    max_width =50               #   table width is set to 50.

    if(tablenum ==1):           #If the integer tablenum passed as argument is 1, it prints the original csv file in table format.        
        line1 = print(f"{'#':<5}{'Item':<15}{'Current Stock':<15}{'Price per Item':>13}")    # Width of various columns are set.
        print("="*max_width)
        i =1
        for item in stock_list:                  # Each dictionary content of the list is printed.
            print(f"{i:<5} {item['Item']:<15} {item['Current Stock']:^12} $ {item['Price per Item']:<2}")
            i = i+1


    elif(tablenum==2):            # If tablenum is 2, the total sales table of the day needs to be printed.
        max_width = 60

        line1 = print(f"{'#':<5}{'Item':<15}{'Sales':<15}{'Price per Item':>13} {'Total':>8}")    #The table headers are set.
        print("="*max_width)
        i =1
        total = 0
        for item in stock_list:         #Each content of the list dictionary  is printed.
            total_sale_item = float(item['Sales']) * float(item['Price per Item'])           #The total sale value of an item is calculated.
            print(f"{i:<5} {item['Item']:<15} {item['Sales']:<15} $ {item['Price per Item']:^12} ${total_sale_item:^2.2f}")
            total += total_sale_item         #The total sale of the day is calculated
            i = i+1
           
        print(f"\nTotal: { ' ' *45} ${total:^2.2f}" )
    elif(tablenum==3):    
        max_width = 60                          #If tablenum is 3, Lost sale table to be printed.
        line1 = print(f"{'#':<5}{'Item':<15}{'Sales':<15}{'Price per Item':^13} {'Total':<15}")    #Table headers are set.
        print("="*max_width)
        i =1
        total = 0
        for item in stock_list:          #  For each item in the dictionary list

            if item['Lost Item'] !=0:    # If  the item stock is 0, then calculate the lost sale of that item
                total_lostsale_item = float(item['Lost Item']) * float(item['Price per Item'])
                print(f"{i:<5} {item['Item']:<15} {item['Lost Item']:<15} $ {item['Price per Item']:^10} ${total_lostsale_item:^2.2f}")
                total += total_lostsale_item          #Calculating the total lost sale
                i = i+1
            
        print(f"\nTotal: { ' ' *43} ${total:.02f}" )
    else:        
        max_width = 80                                           # Printing the demand table.
        print(f"{'#':<5}{'Item':<15}{'Demand':<10}{'20%':<5}{'Total Demand':<12}{'CurrentStock':^22}{'From Ware House':<20}")
        print("="*max_width)
        i =1
        total = 0
        percent = 0
        demand = 0
        warehousecount=0
        for item in stock_list:                 #For each item in the dictionary list,
            demand = (item['Sales']) + int(item['Lost Item'])   #Demand is the sum of the sales and lost item 
            percent= round(demand*20/100)        # 20% of the demand is calculated.
            total = demand+ percent
            if int(item['Current Stock'])> demand:    # checking if there is sufficient stock to meet the demand, if not....
                warehousecount = 0
            else:
                warehousecount = total - int(item['Current Stock'])    #....needs to be brought from th warehouse.
            
                   #Updating the current stock.
                        
            print(f"{i:<5} {item['Item']:<15} {demand:<5}{percent:>5}  {total:^12} {item['Current Stock']:^15}{warehousecount:^23}")
            item['Current Stock']= int(item['Current Stock']) + warehousecount



        



def update_stock(stock_list,item_choice):

    '''This function takes stocklist and the itemchoice as arguments and
    returns the updated stock list'''
    #print("Current stock is"+ stock_list[item_choice]['Current Stock'])

    if(int(stock_list[item_choice]['Current Stock'])==0):    #Checking if the current stock is 0, if so ...
        stock_list[item_choice]['Lost Item'] = stock_list[item_choice]['Lost Item'] + 1      #...the lost sale is incremented by 1
        #print("error")
        print(f"{stock_list[item_choice]['Item']}is out of stock. Replenish  the stock")      #Printing the message that stock is not available.
    else:
        stock_list[item_choice]['Sales'] += 1             #If the stock is available, the sale is incrementd by 1 and the current stock is decrementd by 1
        stock_list[item_choice]['Current Stock']=   str(int(stock_list[item_choice]['Current Stock']) - 1)   
        
    return stock_list             #Return the updated stock list.
    


if len(sys.argv) == 1:      # If the filename is not provided, print the message foe the usage of the command.
    print("Usage: lab7d.py filename")
else:
    filename = sys.argv[1]        # The filename is the 2nd argument 
    try:

        stocklist = read_stock_file(filename)      # Calling the read_stock_file function
        print_stock(stocklist,1)                   #Calling the print_stock function with argument number 1.
        
        while(True):                                #While loop to continue the provision to choose the item number.
            item_choice = input(f"Select a number (1- {len(stocklist)}) to indicate a sale or e to indicate the end of the day: ")
            
            if (item_choice.lower() =='e'):        # If the user choice is the letter e, it indicates the end of sale
                break
    
            elif (int(item_choice) > len(stocklist) or int(item_choice) < 1 ):         # If the user choice a number greater than the length of stocklist
                print("Enter a valid choice.")                                        #Print invalid message
            else:
                item_choice = int(item_choice)-1                                     #If the choice is valid, call the function update_stock
                new_list = update_stock (stocklist,int(item_choice))
        print(f"{'Total Sales':^50}\n ") 
        print_stock(new_list,2)                              #Calling the function print_stock with parameter 2 for printing the total sales list table
        print(f"{'Lost Sales':^50} \n ") 
        print_stock(new_list,3)                                #Calling the function print_stock with parameter 3 for printing the restock table
        print(f"{'Restock':^50} \n ") 
        print_stock(new_list,4)                                 #Calling the function print_stock with parameter 4 for printing the demand table
        write_stock_file(new_list)
    
        latest = "stock.csv"
        create_new_csv("stock_status.csv", latest)              #Creating new csv file....updating the original csv file by calling the function create_new_csv
    except FileNotFoundError:
        print("ERROR:%s not found." %filename)
    