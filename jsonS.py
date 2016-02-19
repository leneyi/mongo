import json  
  
# dict to json  
d=dict(name="cui",age=20,score=88)  
print json.dumps(d)  
  
#list to json  
l=["cui",20,88]  
print json.dumps(l) 


#object to json  
class Student(object):  
    """docstring for Student"""
    '''
    def __init__(self):  
        super(Student, self).__init__()  
        self.age=20  
        self.name="cui"  
        self.score=88
    
  
    print json.dumps(Student(),default=lambda obj:obj.__dict__)
    '''
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


s = Student('Bob', 20, 88)
#lambda expression, argument:expression
print json.dumps(s,default=lambda obj:obj.__dict__)

#insert into the collections
