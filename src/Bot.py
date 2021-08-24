'''
constants:
    - stop loss percentage : eg 20%
    - balance : double 
    - 


position = [
    {
        "code" : 'XRP',
        "value" : 2.00,
        "number_of_shares" : 5000.0
    }
]



'''

class Bot:
    def __init__(self, balance=0.0, stop_loss=.2, position=[]):
        self.balance = balance
        self.stop_loss = stop_loss
        self.position = position
        
    def set_stop_loss(self, stop_loss):
        self.stop_loss = stop_loss

    def set_balance(self, balance):
        self.balance = balance
    
    def get_balance(self):
        return self.balance

    def get_stop_loss(self):
        return self.stop_loss

    def get_position(self):
        return self.position
    
    def buy(self, code, price, num_shares):
        if balance - price * num_shares < 0:
            raise Exception("Not enough money to buy")

        self.set_balance(self.get_balance() - (price * num_shares))
        position.append(create_position_object(code,price,num_shares))    

    def sell(self, code, sell_price):
        
        sell_object = [x for x in self.get_position() if x['code'] == code][0]
        self.set_balance(self.get_balance + sell_price * sell_object['num_shares'])
        position.remove(sell_object)
    
    
    
    
    
    
    
    
    
    @staticmethod
    def create_position_object(code, price, num_shares):
        return {
            "code" : code,
            "value" : price,
            "num_shares" : num_shares
        }