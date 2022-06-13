from .sql import execute


class StudentCourse:
    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def count_enlisted(self):
        statement = "SELECT count(*) AS  total" \
                    " FROM users_courses WHERE course_id = :id"
        params = {'id': self.course_id}
        res, _ = execute(statement, params)
        return int(res[0]['total'])

    def deregister_student(self):
        statement = "DELETE FROM users_courses WHERE" \
                    " user_id = :student_id AND course_id = :course_id"
        params = {
            'student_id': self.student_id,
            'course_id': self.course_id
        }
        execute(statement, params)

    def register_student(self):
        if self.count_enlisted() >= 10:
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
        statement = "SELECT * FROM users_courses  WHERE" \
                    " user_id = :student_id AND course_id = :course_id"
        params = {
            'student_id': self.student_id,
            'course_id': self.course_id
        }
        res, _ = execute(statement, params)
        return len(res)