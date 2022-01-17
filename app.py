import inspect
def props(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']

class User():
    email = ''
    password = ''
    realName= ''

properties = props(User)
print(properties)