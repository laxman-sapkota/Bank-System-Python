from admin import Admin
from customer import Customer
from account import Account
import json

customers_list = []
admins_list = []

	
class BankSystem(object):                               
    def __init__(self):                                                         #These are used to define customer, admin, and bank data loded from json file
        self.customers_list = []
        self.admins_list = []
        self.load_bank_data()

    def getFloat(self,prompt):
        while True:
            try:
                myFloat = float (input(prompt))
                return myFloat
            except ValueError:
                Print('Not a number!')
                

    #Customer List, Personal Information, Account Numbers
    def load_bank_data(self):
        with open ("data.json", "r", encoding="utf-8") as bank:                        #Data backed up using utf-8
            data = json.load(bank)
    

        for c in data['customer']:

            customer = Customer(c["Name"], c["password"], c["address"])
            account = Account(c["balance"], c["uid"], self)
            customer.open_account(account)
            self.customers_list.append(customer)

        for c in data['admin']:
            admin= Admin(c["Name"], c["password"],True, c["address"])                  #This creates an instance
            self.admins_list.append(admin)

    def customer_login(self, name, password):
        #If Customer login is incorrect
        found_customer = self.search_customers_by_name(name)
        if found_customer == None:
            return("\n The customer has not been found!\n")                    #This message is displayed when username is wrong
        else:
            if (found_customer.check_password(password) == True):
                self.run_customer_options(found_customer)
            else:
                return("you have input a wrong password")                      #This message is displayed when password is wrong
    
        
    def search_customers_by_name(self, customer_name):
        #Searching customers via name
        found_customer = None
        for a in self.customers_list:
            name = a.get_name()
            if name == customer_name:
                found_customer = a
                break
        if found_customer == None:
            print("\nThe customer %s does not exist! Try again...\n" %customer_name)
        return found_customer


    def main_menu(self):
        #print the options you have
        print()
        print()
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("Welcome to the Python Bank System")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Admin login")
        print ("2) Customer login")
        print ("3) Quit Python Bank System")
        print (" ")
        option = int(input ("Choose your option: "))
        return option

    def run_main_option(self):
        loop = 1         
        while loop == 1:
            choice = self.main_menu()
            if choice == 1: #Input Admin Login
                name = input ("\nPlease input admin name: ")
                password = input ("\nPlease input admin password: ")
                msg = self.admin_login(name, password)
                print(msg)
            elif choice == 2: #Input Customer Login
                name = input ("\nPlease input customer name: ")
                password = input ("\nPlease input customer password: ")
                msg = self.customer_login(name, password)
                print(msg)
            elif choice == 3:
                loop = 0
        print ("Thank-You for stopping by the bank!")

    def customer_menu(self, customer_name):
        #print the options you have
         print (" ")
         print ("Welcome %s : Your transaction options are:" %customer_name)
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Account operations")
         print ("2) profile settings")
         print ("3) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option

    def run_customer_options(self, customer):
          #Customer account/profile options can be chosen here          
        account = customer.get_account()            
        loop = 1
        while loop == 1:
            choice = self.customer_menu(customer.get_name())
            if choice == 1:
                account.run_account_options()#runs account options
            elif choice == 2:
                customer.run_profile_options()#runs profile options
            elif choice == 3:#Exits account/profile options
                loop = 0
        print ("Exit account operations")

                
    def admin_login(self, name, password):
        #If Admin login is incorrect
        found_admin = self.search_admin_by_name(name)
        if found_admin == None:
            return("\n The admin has not been found!\n")                                #This message is displayed when username is wrong
        else:
            if (found_admin.check_password(password) == True):
                self.run_admin_options(found_admin)
            else:
                return("you have input a wrong password")                               #This message is displayed when password is wrong

    def search_admin_by_name(self, admin_name):
        #Search an admin
        found_admin = None
        for a in self.admins_list:
            name = a.get_name()#Searches admin within the admin list
            if name == admin_name:
                found_admin = a
                break
        if found_admin == None:
            print("\nThe admin %s does not exist! Try again...\n" %admin_name)#Incorrect input will result with this message
        return found_admin



    def admin_menu(self, admin_name):
        #print the options you have
         print (" ")
         print ("Welcome Admin %s : Avilable options are:" %admin_name)
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Transfer money")
         print ("2) Customer account operations")
         print ("3) Customer profile settings")
         print ("4) Admin profile settings")
         print ("5) Delete customer")
         print ("6) Print all customers detail")
         print ("7) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option


    def run_admin_options(self, admin):
                                
        loop = 1
        while loop == 1:
            choice = self.admin_menu(admin.get_name())
            if choice == 1:
                sender_name =input("\nWho's account are we transferring the money from?")
                sender = self.search_customers_by_name(sender_name)
                if sender!= None:
                    account = sender.get_account()
                    customer_name =input ("\nPlease enter recipient name:")
                    recipient = self.search_customers_by_name(customer_name)
                    if recipient != None:
                        trans_amount = self.getFloat("\nHow much would you like to transfer?")
                        if trans_amount > account.get_balance():
                            print("Request amount has been denied")
                            response= input("Press Y to retry transfer. Press any other key to exit")
						
                        else:
                            recipient_account = recipient.get_account()
                            (recipient_account).deposit(trans_amount, recipient_account)
                            account.withdraw(trans_amount,account)
                            print ('£%d Transfer was successful. Your balance now is %.2f' %(trans_amount,account.get_balance()))
                            break

                        
            elif choice == 2:
                #Choice 2 allows you to search customer from customer list
                customer_name = input("\nPlease input customer name :\n")
                customer = self.search_customers_by_name(customer_name)
                if customer != None:
                    account = customer.get_account()
                    if account != None:
                        account.run_account_options()
            elif choice == 3:
                #Search customers, then runs profile options
                customer_name = input("\nPlease input customer name :\n")
                customer = self.search_customers_by_name(customer_name)
                if customer != None:
                    customer.run_profile_options()
            elif choice == 4:
                #profile options for admin
                admin.run_profile_options()
            elif choice == 5:
                #Removes a specified customer, only if Admin has full rights
                if admin.has_full_admin_right() == True:
                    customer_name = input("\nPlease input customer name you want to delete :\n")
                    customer_account = self.search_customers_by_name(customer_name)
                    if customer_account != None:
                        self.customers_list.remove(customer_account)
                        print("\nCustomer has been removed from the system")

                        
                else:#If Admin does not have full rights
                    print("\nOnly administrators with full admin rights can remove a customer from the bank system!\n")
            elif choice == 6:
                #prints all accounts details for every customer
                self.print_all_accounts_details()

            elif choice == 7:
                loop = 0
        print ("Exit account operations")


    def print_all_accounts_details(self):
            # list related operation - move to main.py
            i = 0
            for c in self.customers_list:
                i+=1
                print('\n %d. ' %i, end = ' ')
                c.print_details()
                print("------------------------")

        



app = BankSystem()
app.run_main_option()
