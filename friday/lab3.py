#count from 1 to 5 using a while L
balance=float(input("enter starting balance"))
while balance>0:
    print("current balance")
    choice=input("Deposit(D) or withdraw (W)")
    if choice =="D":
        amount=float(input("enter amount to deposit"))
        balance+=amount

    elif choice=="W":
       amount=float(input("enter amount to withdraw"))
       balance+=amount 

       if balance<0:
           balance=0
           print("balance is 0 account closed")