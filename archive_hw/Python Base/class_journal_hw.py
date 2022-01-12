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


# студенты
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['Git']
best_student.finished_courses += ['Введение в программирование']

stud_ent1 = Student('Din', 'Go', 'gen')
stud_ent1.courses_in_progress += ['Java']
stud_ent1.courses_in_progress += ['Python']
stud_ent1.finished_courses += ['C']

#преподаватели
mentor_gy = Lecturer('Tom', 'Soer')
mentor_gy.courses_attached += ['Python']
mentor_gy.courses_attached += ['C']

cool_mentor = Lecturer('Frans', 'Iosif')
cool_mentor.courses_attached += ['Python']
cool_mentor.courses_attached += ['Java']

# проверяющие
cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python']
cool_reviewer.courses_attached += ['Java']

#Оценки за домашнюю работу студуентам
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 10)

cool_reviewer.rate_hw(stud_ent1, 'Python', 9)
cool_reviewer.rate_hw(stud_ent1, 'Python', 8)
cool_reviewer.rate_hw(stud_ent1, 'Java', 10)

#студенты оценивают преподавателей
best_student.marks_lecturer(mentor_gy, 'Python', 10)
best_student.marks_lecturer(cool_mentor, 'Python', 9)
stud_ent1.marks_lecturer(mentor_gy, 'Python', 6)
stud_ent1.marks_lecturer(cool_mentor, 'Python', 10)

# вычисляем средние оценки по студентам и лекторам
st_list = [best_student, stud_ent1]
lect_list = [mentor_gy, cool_mentor]

def avg_hw_st (lst_students, course):

    tmp = []

    for student in lst_students:
        tmp.extend(student.grades[course])

    result = sum(tmp) / len(tmp)
    return result

def avg_lecturer (lst_lecturers, course):

    tmp = []

    for lecturer in lst_lecturers:
        tmp.extend(lecturer.marks[course])

    result = sum(tmp) / len(tmp)
    return result

print(avg_hw_st(st_list, 'Python'))
print(avg_lecturer(lect_list, 'Python'))

# print(best_student.grades)
# print(stud_ent1.grades)
print()
print(best_student)
print(stud_ent1)
print()
print(mentor_gy.marks)
print(cool_mentor.marks)
print()
print(cool_reviewer)
print(mentor_gy)
print(cool_mentor)
print()
mentor_gy.average_rate()
cool_mentor.average_rate
print()
print(mentor_gy > best_student)