import json

class Account:

        def __init__(self, balance, account_no, MainClass):
                self.balance = float(balance)
                self.account_no = account_no
                self.mainClass = MainClass

        def deposit(self, amount, account):
                account.balance+=amount

                with open("data.json", "r") as jsonFile:
                        data = json.load(jsonFile)

                customer = data["customer"][account.account_no-1]
                customer["balance"] = account.balance

                with open("data.json", "w") as jsonFile:
                        json.dump(data, jsonFile)

        def withdraw(self, amount, account):

                account.balance-=amount

                with open("data.json", "r") as jsonFile:
                        data = json.load(jsonFile)

                customer = data["customer"][account.account_no-1]
                customer["balance"] = account.balance

                with open("data.json", "w") as jsonFile:
                        json.dump(data, jsonFile)

                

        def transfer(self, amount, customer):
                self.withdraw(amount, self)
                account = customer.get_account()
                account.deposit(amount, account)
                print("You have transfered " + str(amount) + " to " + customer.name)
                       
        def print_balance(self):
                print("Your account balance is %.2f" %self.balance)

        def get_balance(self):
                return self.balance

        def get_account_no(self):
                return self.account_no

        def account_menu(self):
                #print the options you have
                 print (" ")
                 print ("Your Transaction Options Are:")
                 print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                 print ("1) Deposit money")
                 print ("2) Withdraw money")
                 print ("3) Check balance")
                 print ("4) Transfer money")
                 print ("5) Back")
                 print (" ")
                 option = int(input ("Choose your option: "))
                 return option

        def run_account_options(self):
                loop = 1
                while loop == 1:
                        choice = self.account_menu()
                        if choice == 1:
                                amount=float(input("::\nPlease enter amount to be deposited\n: "))
                                deposit = self.deposit(amount, self)
                                self.print_balance()
                        elif choice == 2:
                                amount=float(input("::\nPlease enter amount to be withdrawn\n: "))
                                withdraw = self.withdraw(amount, self)
                                self.print_balance()
                        elif choice == 3:
                                balance = self.print_balance()
                        elif choice == 4:
                                user=input("::\nPlease enter a name you wish to transfer to\n: ")
                                amount=float(input("::\nPlease enter amount to transfer\n: "))
                                customer = self.mainClass.search_customers_by_name(user)
                                transfer = self.transfer(amount, customer)
                                self.print_balance()
                        elif choice == 5:
                                loop = 0
                print ("Exit account operations")


