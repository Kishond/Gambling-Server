class User:
    def __init__(self, name, balance=500):
        self.balance = balance
        self.name = name
        self.total_profit = 0

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

    def get_name(self):
        return self.name

    def add_balance(self, balance):
        self.balance += balance
        self.total_profit += balance

    def remove_balance(self, balance):
        self.balance -= balance
        self.total_profit -= balance

    def get_total_profit(self):
        return self.total_profit
