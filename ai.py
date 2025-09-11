

class Calculate:

    def sum(self, *arg):
        return sum(arg)
    
    def multiplay(self , a: int ,b:int):
        return a * b
    
    def divide(self , a ,b):
        return a/b
    
    def minus(self , a ,b):
        return a-b
    
my_data = Calculate()

sum = my_data.sum(1,2,3,4,5,6)
multiplay = my_data.multiplay(50 , 60)
divide = my_data.divide(100 ,2)
minus = my_data.minus(20 ,50)

print(f"sum of num :{sum} multiplay of num :{multiplay} divide of num :{divide} minus of num :{minus}")

        