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
    
    @staticmethod
    def create_position_object(code, price, money_invested):
        return {
            "code" : code,
            "value" : price,
            "num_shares" : money_invested / price,
            "total_invested" : money_invested
        }
    @staticmethod
    def update_position_object(share_object, price, money_invested):
        share_object['total_invested'] += money_invested
        share_object['num_shares'] += money_invested / price
        share_object['value'] = share_object['total_invested'] / share_object['num_shares']
    
    def set_stop_loss(self, stop_loss):
        self.stop_loss = stop_loss

    def set_balance(self, balance):
        self.balance = balance
        
    def set_position(self, position):
        self.position = position
    
    def get_balance(self):
        return self.balance

    def get_stop_loss(self):
        return self.stop_loss

    def get_position(self):
        return self.position
    
    def buy(self, code, price, money_invested):
        if self.balance - money_invested < 0:
            raise Exception("Not enough money to buy")

        self.set_balance(self.get_balance() - money_invested)
        
        # if the code is already in the list, try and find it
        share_object = [x for x in self.get_position() if x['code'] == code]
        
        if len(share_object) == 0:
            self.position.append(self.create_position_object(code,price,money_invested))  
        else:
            self.update_position_object(share_object[0], price, money_invested)
        
        
    def sell(self, code, sell_price):
        sell_object = [x for x in self.get_position() if x['code'] == code][0]
        self.set_balance(self.get_balance() + sell_price * sell_object['num_shares'])
        self.position.remove(sell_object)
        
    
    
    
    
    
    
    
    
    
    