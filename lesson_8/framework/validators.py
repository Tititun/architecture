from .sql import execute


class StudentCourse:
    """Class for interaction between students and courses"""
    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id
        self.max_students_per_course = 10

    def count_enlisted(self):
        """counts how many students are enlisted for the course"""
        statement = "SELECT count(*) AS  total" \
                    " FROM users_courses WHERE course_id = :id"
        params = {'id': self.course_id}
        res, _ = execute(statement, params)
        return int(res[0]['total'])

    def deregister_student(self):
        """unregisters the student from the course"""
        statement = "DELETE FROM users_courses WHERE" \
                    " user_id = :student_id AND course_id = :course_id"
        params = {
            'student_id': self.student_id,
            'course_id': self.course_id
        }
        execute(statement, params)

    def register_student(self):
        """registers the student for the course if it has available
        positions"""
        if self.count_enlisted() >= self.max_students_per_course:
            return False

        statement = "INSERT INTO users_courses VALUES" \
                    " (NULL, :student_id, :course_id)"
        params = {
            'student_id': self.student_id,
            'course_id': self.course_id
        }
        execute(statement, params)
        return True

    def is_enlisted(self):
        """chacks if the student is already enlisted for the course"""
        statement = "SELECT * FROM users_courses  WHERE" \
                    " user_id = :student_id AND course_id = :course_id"
        params = {
            'student_id': self.student_id,
            'course_id': self.course_id
        }
        res, _ = execute(statement, params)
        return len(res)