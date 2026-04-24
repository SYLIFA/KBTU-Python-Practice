class Person:
  def __init__(self, fname):
    self.firstname = fname
class Student(Person):
  def __init__(self, fname, year):
    super().__init__(fname)
    self.year = year
x = Student("Mike", 2019)
print(x.year)
