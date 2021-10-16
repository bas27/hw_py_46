class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
 
    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def marks_lecturer(self, mentor, course, marks):

        if isinstance(mentor, Lecturer) and course in self.courses_in_progress and course in mentor.courses_attached:
            if course in mentor.marks:
                mentor.marks[course] += [marks]
            else:
                mentor.marks[course] = [marks]
        else:
            return 'Ошибка'
 
    def average_rate(self):
        
        summ = 0
        count = 0
        
        for _, grades in self.grades.items():
            # for grade in grades:
            #     sum += grade
            #     count += 1
            summ += sum(grades)
            count += len(grades)
        
        result = summ / count
        return result

    def __str__(self):
        result = f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {self.average_rate()}\nКурсы в процессе изучения: {', '.join(self.courses_in_progress)}\nЗавершенные курсы: {', '.join(self.finished_courses)}"
        return result
     
class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
        
class Lecturer(Mentor):

    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)
        self.marks = {}

    def average_rate(self):
        
        summ = 0
        count = 0
        
        for _, grades in self.marks.items():
            # for grade in grades:
            #     sum += grade
            #     count += 1
            summ += sum(grades)
            count += len(grades)

        result = summ / count
        return result

    def __str__(self):
        result = f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.average_rate()}'
        return result

    def __lt__(self, other):
        if not isinstance(other, Student):
            print('Not a Student!')
            return
        if self.average_rate() == Student.average_rate(other):
            print('Средние оценки равнозначны')
            return
        else:
            return self.average_rate() < Student.average_rate(other)

    def __gt__(self, other):
        if not isinstance(other, Student):
            print('Not a Student!')
            return

        if self.average_rate() == Student.average_rate(other):
            return 'Средние оценки равнозначны'

        else:
            return self.average_rate() > Student.average_rate(other)        
class Reviewer(Mentor):
    
    def __init__(self, name, surname):
        Mentor.__init__(self, name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        result = f'Имя: {self.name}\nФамилия: {self.surname}'
        return result

best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['Git']
best_student.finished_courses += ['Введение в программирование']

mentor_gy = Lecturer('Tom', 'Soer')
mentor_gy.courses_attached += ['Python']

cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python']

cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 10)

best_student.marks_lecturer(mentor_gy, 'Python', 10)

print(best_student.grades)
print(best_student)
print(mentor_gy.marks)
# print(cool_reviewer)
print(mentor_gy)
# mentor_gy.average_rate()
print(mentor_gy > best_student)