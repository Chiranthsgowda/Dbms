"""
student_module.py - Student management module for College Event Participation Tracker
"""

from db_connection import db
import re


class StudentModule:
    """Class to handle student-related operations"""

    @staticmethod
    def validate_usn(usn):
        """Validate USN format (e.g., 1MS21CS001)"""
        pattern = r'^\d[A-Z]{2}\d{2}[A-Z]{2}\d{3}$'
        return bool(re.match(pattern, usn))

    @staticmethod
    def validate_year(year):
        """Validate student year"""
        try:
            year = int(year)
            return 1 <= year <= 5
        except ValueError:
            return False

    def add_student(self, usn, name, department, year):
        """Add a new student to the database"""
        # Validate inputs
        if not usn or not name or not department or not year:
            return False, "All fields are required"
        
        # Validate USN format
        if not self.validate_usn(usn):
            return False, "Invalid USN format. Expected format: 1MS21CS001"
        
        # Validate year
        if not self.validate_year(year):
            return False, "Year must be between 1 and 5"
        
        # Check if USN already exists
        existing = db.fetch_one("SELECT usn FROM students WHERE usn = %s", (usn,))
        if existing:
            return False, f"Student with USN {usn} already exists"
        
        # Insert new student
        query = """
        INSERT INTO students (usn, name, department, year) 
        VALUES (%s, %s, %s, %s)
        """
        success = db.execute_query(query, (usn, name, department, int(year)))
        
        if success:
            return True, f"Student {name} ({usn}) added successfully"
        else:
            return False, "Failed to add student"

    def get_all_students(self):
        """Get all students with their participation count"""
        query = """
        SELECT s.usn, s.name, s.department, s.year, 
               COUNT(p.id) AS participation_count
        FROM students s
        LEFT JOIN participation p ON s.usn = p.usn
        GROUP BY s.usn, s.name, s.department, s.year
        ORDER BY s.department, s.year, s.name
        """
        return db.fetch_all(query)

    def get_student_by_usn(self, usn):
        """Get student details by USN"""
        query = "SELECT * FROM students WHERE usn = %s"
        return db.fetch_one(query, (usn,))

    def update_student(self, usn, name, department, year):
        """Update student information"""
        # Validate inputs
        if not usn or not name or not department or not year:
            return False, "All fields are required"
        
        # Validate year
        if not self.validate_year(year):
            return False, "Year must be between 1 and 5"
        
        # Check if student exists
        existing = self.get_student_by_usn(usn)
        if not existing:
            return False, f"Student with USN {usn} not found"
        
        # Update student
        query = """
        UPDATE students 
        SET name = %s, department = %s, year = %s 
        WHERE usn = %s
        """
        success = db.execute_query(query, (name, department, int(year), usn))
        
        if success:
            return True, f"Student {name} ({usn}) updated successfully"
        else:
            return False, "Failed to update student"

    def delete_student(self, usn):
        """Delete a student record"""
        # Check if student exists
        existing = self.get_student_by_usn(usn)
        if not existing:
            return False, f"Student with USN {usn} not found"
        
        # Delete student (participation records will be deleted due to CASCADE)
        query = "DELETE FROM students WHERE usn = %s"
        success = db.execute_query(query, (usn,))
        
        if success:
            return True, f"Student with USN {usn} deleted successfully"
        else:
            return False, "Failed to delete student"

    def search_students(self, search_term):
        """Search students by name, USN, or department"""
        query = """
        SELECT * FROM students 
        WHERE usn LIKE %s OR name LIKE %s OR department LIKE %s
        ORDER BY department, year, name
        """
        search_param = f"%{search_term}%"
        return db.fetch_all(query, (search_param, search_param, search_param))

    def get_student_events(self, usn):
        """Get all events a student has participated in"""
        query = """
        SELECT e.event_id, e.name, e.event_type, e.department, 
               e.event_date, p.performance
        FROM events e
        JOIN participation p ON e.event_id = p.event_id
        WHERE p.usn = %s
        ORDER BY e.event_date DESC
        """
        return db.fetch_all(query, (usn,))


# For testing the module
if __name__ == "__main__":
    student_module = StudentModule()
    
    # Example operations for testing
    # Add a student
    result, message = student_module.add_student("1MS21CS100", "Test Student", "Computer Science", 3)
    print(message)
    
    # Get all students
    students = student_module.get_all_students()
    print(f"Total students: {len(students)}")
    
    # Get student by USN
    student = student_module.get_student_by_usn("1MS21CS100")
    if student:
        print(f"Found student: {student['name']}")
    
    # Update student
    result, message = student_module.update_student("1MS21CS100", "Updated Name", "Computer Science", 4)
    print(message)
    
    # Delete student
    result, message = student_module.delete_student("1MS21CS100")
    print(message)
