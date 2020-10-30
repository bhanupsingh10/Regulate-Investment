import csv                                          #importing CSV(comma-seperated-value) files
import datetime                                     #importing python module that module supplies classes for manipulating dates and times
from dateutil.relativedelta import relativedelta    #importing


class BudgetViolation:
    def __init__(self, budget_file, investment_file):                               #Constructor with paths of the two files
        """Initialization"""
        self.budget_file = budget_file
        self.investment_file = investment_file
        self.rule = {'1.00': {}, '2.00': {}, '3.00': {}, '4.00': {}, '5.00': {}}
        self.time = {"Month": 1, "Quarter": 3, "Year": 12}

    def check_violation_investments(self):                                          #Check all violations in the investment.csv
        with open(self.investment_file, 'r') as investments:                        #Opening a file in reading mode
            read_invests = csv.DictReader(investments)                              #Return a reader object which will traverse over lines in the given csvfile
            for invest in read_invests:                                             #Traversing over all the data with help if reader object
                self.check_violation(invest)                                        #Checking violation

    def check_violation(self, invest):                                                                  #Funtion for traversing over the budget rules and find out the invalid investments
        invest_date = datetime.datetime.strptime(invest['Date'], '%d/%m/%Y')                            #strptime creates a datetime object from a string and returns a object of a combination of a date and a time
        with open(self.budget_file, 'r') as budgets:                                                    #Opening budget.csv in read mode
            read_budgets = csv.DictReader(budgets)                                                      # Return a reader object for traversal
            for budget in read_budgets:
                if budget['Sector'] == '' or invest['Sector'] == budget['Sector']:                                      #Comparing the sector
                    if float(invest['Amount']) <= float(budget['Amount']):                                              #Checking the budget amount condition
                        if self.rule[budget['ID']] != {} and invest_date.date() < self.rule[budget['ID']]['to_date']:
                            self.rule[budget['ID']]['Amount'] += float(invest['Amount'])
                            if self.rule[budget['ID']]['Amount'] > float(budget['Amount']):
                                self.rule[budget['ID']]['Amount'] -= float(invest['Amount'])
                                print(int(float(invest['ID'])))                                                         #Printing the ID from the investments list for violation
                                break
                        else:
                            self.rule[budget['ID']]['from_date'] = invest_date.date()
                            self.rule[budget['ID']]['to_date'] = invest_date.date() + relativedelta(
                                months=+ self.time.get(budget['Time Period'], 0))
                            self.rule[budget['ID']]['Amount'] = float(invest['Amount'])
                    else:
                        print(int(float(invest['ID'])))                                                                 #Printing the ID from the investments list for violation
                        break


if __name__ == '__main__':
    budget_file = input()                                           #Taking path of budget.csv file as user input
    investment_file = input()                                       #Taking path of investment.csv file as user input
    budget = BudgetViolation(budget_file, investment_file)          #making object budget and calling the constructor
    budget.check_violation_investments()                            #checking the violations in investment.csv file
