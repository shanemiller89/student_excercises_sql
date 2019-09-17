import sqlite3

class Cohort():

    def __init__(self, cohort):
        self.cohort_name = cohort

    def __repr__(self):
        return f'\nCohort: {self.cohort_name}'

class Student(Cohort):

    def __init__(self, first, last, handle, cohort):
        Cohort.__init__(self, cohort)
        self.first_name = first
        self.last_name = last
        self.slack_handle = handle

    def __repr__(self):
        return f'\nStudent:{self.first_name} {self.last_name} \n Cohort:{self.cohort_name}'

class Instructor(Cohort):

    def __init__(self, first, last, handle, speciality, cohort):
        Cohort.__init__(self, cohort)
        self.first_name = first
        self.last_name = last
        self.slack_handle = handle
        self.speciality = speciality

    def __repr__(self):
        return f'\nInstructor:{self.first_name} {self.last_name} \n Speciality: {self.speciality} \n Cohort:{self.cohort_name}'

class Excercises():

    def __init__(self, name, language):
        self.excercise_name = name
        self.excercise_language = language
        
    def __repr__(self):
        return f'\nExercise:{self.excercise_name} \n Language:{self.excercise_language}'


class StudentExerciseReports():

    """Methods for reports on the Student Exercises database"""

    def __init__(self):
        self.db_path = "/home/shanemiller89/workspace/SQL/student_excercises/studentexcercises.db"

    # def create_student(self, cursor, row):
    #     return Student(row[1], row[2], row[3], row[5])

    def all_cohorts(self):

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Cohort(row[1])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT c.cohortId, c.cohortName
            FROM Cohorts c
            ORDER BY c.cohortId
            """)

            all_cohorts = db_cursor.fetchall()

            [print(c) for c in all_cohorts]
        

    def all_students(self):

        """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            #row_factory needs to be BEFORE db_cursor
            conn.row_factory = lambda cursor, row: Student(row[1], row[2], row[3], row[5])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select s.studentId,
                s.firstName,
                s.lastName,
                s.slackHandle,
                s.cohortId,
                c.cohortName
            from Students s
            join Cohorts c on s.cohortId = c.cohortId
            order by s.cohortId
            """)

            all_students = db_cursor.fetchall()

            [print(s) for s in all_students]

            # print(all_students)
            # for student in all_students:
                # print(student)

    def all_instructors(self):

        """Retrieve all students with the cohort name"""

        with sqlite3.connect(self.db_path) as conn:
            #row_factory needs to be BEFORE db_cursor
            conn.row_factory = lambda cursor, row: Instructor(row[1], row[2], row[3], row[4], row[6])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select i.instructorId, i.firstName, i.lastName, i.slackHandle, i.speciality, i.cohortId, c.cohortName
            from Instructors i
            join Cohorts c on i.cohortId = c.cohortId
            order by i.cohortId
            """)

            all_instructors = db_cursor.fetchall()

            [print(i) for i in all_instructors]

    def all_excercises(self):
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Excercises(row[1], row[2])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT e.excerciseId, e.excerciseName, e.excerciseLanguage
            FROM Excercises e
            ORDER BY e.excerciseId
            """)

            all_excercises = db_cursor.fetchall()

            [print(e) for e in all_excercises] 

    def all_javascript(self):

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Excercises(row[1], row[2])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT e.excerciseId, e.excerciseName, e.excerciseLanguage
            FROM Excercises e
            WHERE e.excerciseLanguage='Javascript'
            ORDER BY e.excerciseId;
            """)

            all_javascript = db_cursor.fetchall()

            [print(e) for e in all_javascript] 

    def all_python(self):
            
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Excercises(row[1], row[2])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT e.excerciseId, e.excerciseName, e.excerciseLanguage
            FROM Excercises e
            WHERE e.excerciseLanguage='Python'
            ORDER BY e.excerciseId;
            """)

            all_python = db_cursor.fetchall()

            [print(e) for e in all_python] 
        
    def all_csharp(self):
            
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = lambda cursor, row: Excercises(row[1], row[2])
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT e.excerciseId, e.excerciseName, e.excerciseLanguage
            FROM Excercises e
            WHERE e.excerciseLanguage='C#'
            ORDER BY e.excerciseId;
            """)

            all_csharp = db_cursor.fetchall()

            [print(e) for e in all_csharp] 

    def student_assignments(self):

        assignments = {}
        
        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()
        
        db_cursor.execute("""
        Select s.firstName, s.lastName, e.excerciseName
        FROM StudentExcercises se
        JOIN Students s ON se.studentId = s.studentId
        JOIN Excercises e ON se.excerciseId = e.excerciseId
        """)

        dataset = db_cursor.fetchall()

        for row in dataset:
            student_name = f'{row[0]} {row[1]}'
            excercise_name = row[2]
            if student_name not in assignments:
                assignments[student_name] = [excercise_name]
            else:
                assignments[student_name].append(excercise_name)

        for student, excercises in assignments.items():

            print(student)
            for excercise in excercises:
                print(f' \t* {excercise}')

    def instructor_assignments(self):
            
        assignments = {}

        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()
        
        db_cursor.execute("""
        Select i.firstName, i.lastName, e.excerciseName
        from StudentExcercises se
        JOIN Instructors i ON se.instructorId = i.instructorId
        JOIN Excercises e ON se.excerciseId = e.excerciseId
        GROUP BY e.excerciseName;
        """)

        dataset = db_cursor.fetchall()

        for row in dataset:
            instructor_name = f'{row[0]} {row[1]}'
            excercise_name = row[2]
            if instructor_name not in assignments:
                assignments[instructor_name] = [excercise_name]
            else:
                assignments[instructor_name].append(excercise_name)

        for instructor, excercises in assignments.items():

            print(instructor)
            for excercise in excercises:
                print(f' \t* {excercise}')

    def excercise_assignments(self):

        assignments = {}
        
        with sqlite3.connect(self.db_path) as conn:
            db_cursor = conn.cursor()
        
        db_cursor.execute("""
        Select s.firstName, s.lastName, e.excerciseName
        FROM StudentExcercises se
        JOIN Students s ON se.studentId = s.studentId
        JOIN Excercises e ON se.excerciseId = e.excerciseId
        """)

        dataset = db_cursor.fetchall()

        for row in dataset:
            student_name = f'{row[0]} {row[1]}'
            excercise_name = row[2]
            if excercise_name not in assignments:
                assignments[excercise_name] = [student_name]
            else:
                assignments[excercise_name].append(student_name)

        for excercise, students in assignments.items():

            print(excercise)
            for student in students:
                print(f' \t* {student}')

reports = StudentExerciseReports()

def build_menu():
    print("\n1. View Cohorts")
    print("2. View Instructors")
    print("3. View Students")
    print("4. View Excercises")
    print("5. View Javascript Excercises")
    print("6. View Python Excercises")
    print("7. View C# Excercises")
    print("8. View Student Assignments")
    print("9. View Instructor Assignments")
    print("10. Excercise Overview \n")
    menu_options()


def menu_options():
    userinput = input("Select an Option: ")
    if (userinput == "1"):
        reports.all_cohorts()
        build_menu()
    if (userinput == "2"):
        reports.all_instructors()
        build_menu()
    if (userinput == "3"):
        reports.all_students()
        build_menu()
    if (userinput == "4"):
        reports.all_excercises()
        build_menu()
    if (userinput == "5"):
        reports.all_javascript()
        build_menu()
    if (userinput == "6"):
        reports.all_python()
        build_menu()
    if (userinput == "7"):
        reports.all_csharp()
        build_menu()
    if (userinput == "8"):
        reports.student_assignments()
        build_menu()
    if (userinput == "9"):
        reports.instructor_assignments()
        build_menu()
    if (userinput == "10"):
        reports.excercise_assignments()
        build_menu()
    
build_menu()