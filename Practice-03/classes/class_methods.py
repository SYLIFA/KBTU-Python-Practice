class Person:
  def __init__(self, name, age):
    self.name = name
  def myfunc(self):
    print("Hello " + self.name)
p1 = Person("John", 36)
p1.myfunc()
