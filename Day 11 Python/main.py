def salary(hours_worked, hour_rate):
    return hours_worked * hour_rate
employee_list = []
def add_employee(id, name):
    new_employee = {'id': id, 'name': name}
    employee_list.append(new_employee)
    return new_employee

print(salary(4, 5))
print(add_employee(1, "loke"))
print(add_employee(13, "rohit"))
print(employee_list)

class Employee:

    def __init__(self, name, hours_worked, hour_rate):
        self.name = name
        self.hours_worked = hours_worked
        self.hour_rate = hour_rate
    
    def salary(self):
        return self.hours_worked * self.hour_rate
class Employer:
    def __init__(self):
        self.employees = []
    
    def add_employee(self, employee):
        self.employees.append(employee)
    
    def calculate_total_pay(self):
        total_pay = 0
        for employee in self.employees:
            total_pay+= employee.salary()
        return total_pay

employer = Employer()
emp1 = Employee("lokesh",10,20)
emp2 = Employee("ram",16, 25)
employer.add_employee(emp1)
employer.add_employee(emp2)

print(employer.calculate_total_pay())
# try to display all employees


