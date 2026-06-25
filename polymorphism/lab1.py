class Transaction:
    def transact(self):
        print("transaction")

    def details(self,name,amount=0):
        print(name,amount)


class Deposit(Transaction):
    def transact(self):
        print("employee deposited 50k")

class withdrawal(Transaction):
    def transact(self):
        print("employee withdrew 20k")

class transfer(Transaction):
    def transact(self):
        print("employee transacted 10k")

d=Deposit()
w=withdrawal()
t=transfer()

d.details("helen")
d.transact()
w.transact()
t.details("helen",1000)
t.transact()
        