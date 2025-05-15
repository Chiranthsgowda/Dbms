"""
participation_module.py - Participation management module for College Event Participation Tracker
"""

from db_connection import db
from student_module import StudentModule
from event_module import EventModule


class ParticipationModule:
    """Class to handle participation-related operations"""
    
    def __init__(self):
        self.student_module = StudentModule()
        self.event_module = EventModule()
    
    def register_participation(self, usn, event_id, performance="Participant"):
        """Register a student's participation in an event"""
        # Validate inputs
        if not usn or not event_id:
            return False, "Student USN and Event ID are required"
        
        # Validate performance value
        valid_performances = ["Winner", "Runner-up", "Participant"]
        if performance not in valid_performances:
            return False, f"Performance must be one of: {', '.join(valid_performances)}"
        
        # Check if student exists
        student = self.student_module.get_student_by_usn(usn)
        if not student:
            return False, f"Student with USN {usn} not found"
        
        # Check if event exists
        event = self.event_module.get_event_by_id(event_id)
        if not event:
            return False, f"Event with ID {event_id} not found"
        
        # Check if participation already exists
        existing = self.get_participation(usn, event_id)
        if existing:
            # Update existing participation
            query = """
            UPDATE participation 
            SET performance = %s 
            WHERE usn = %s AND event_id = %s
            """
            success = db.execute_query(query, (performance, usn, event_id))
            
            if success:
                return True, f"Updated {student['name']}'s participation in {event['name']}"
            else:
                return False, "Failed to update participation"
        
        # Insert new participation
        query = """
        INSERT INTO participation (usn, event_id, performance) 
        VALUES (%s, %s, %s)
        """
        success = db.execute_query(query, (usn, event_id, performance))
        
        if success:
            return True, f"Registered {student['name']} for {event['name']}"
        else:
            return False, "Failed to register participation"

    def get_participation(self, usn, event_id):
        """Get a specific participation record"""
        query = """
        SELECT id, usn, event_id, performance 
        FROM participation 
        WHERE usn = %s AND event_id = %s
        """
        return db.fetch_one(query, (usn, event_id))

    def delete_participation(self, usn, event_id):
        """Remove a student's participation from an event"""
        # Check if participation exists
        existing = self.get_participation(usn, event_id)
        if not existing:
            return False, f"No participation record found for this student and event"
        
        # Delete participation
        query = """
        DELETE FROM participation 
        WHERE usn = %s AND event_id = %s
        """
        success = db.execute_query(query, (usn, event_id))
        
        if success:
            student = self.student_module.get_student_by_usn(usn)
            event = self.event_module.get_event_by_id(event_id)
            return True, f"Removed {student['name']} from {event['name']}"
        else:
            return False, "Failed to remove participation"

    def get_all_participations(self):
        """Get all participation records with student and event details"""
        query = """
        SELECT p.id, p.usn, s.name as student_name, s.department,
               p.event_id, e.name as event_name, e.event_type, 
               e.event_date, p.performance
        FROM participation p
        JOIN students s ON p.usn = s.usn
        JOIN events e ON p.event_id = e.event_id
        ORDER BY e.event_date DESC, s.name
        """
        return db.fetch_all(query)

    def update_performance(self, usn, event_id, performance):
        """Update a student's performance in an event"""
        # Validate performance value
        valid_performances = ["Winner", "Runner-up", "Participant"]
        if performance not in valid_performances:
            return False, f"Performance must be one of: {', '.join(valid_performances)}"
        
        # Check if participation exists
        existing = self.get_participation(usn, event_id)
        if not existing:
            return False, f"No participation record found for this student and event"
        
        # Update performance
        query = """
        UPDATE participation 
        SET performance = %s 
        WHERE usn = %s AND event_id = %s
        """
        success = db.execute_query(query, (performance, usn, event_id))
        
        if success:
            student = self.student_module.get_student_by_usn(usn)
            event = self.event_module.get_event_by_id(event_id)
            return True, f"Updated {student['name']}'s performance in {event['name']} to {performance}"
        else:
            return False, "Failed to update performance"

    def get_event_winners(self, event_id):
        """Get winners and runners-up for an event"""
        query = """
        SELECT s.usn, s.name, s.department, s.year, p.performance
        FROM students s
        JOIN participation p ON s.usn = p.usn
        WHERE p.event_id = %s AND p.performance IN ('Winner', 'Runner-up')
        ORDER BY 
            CASE 
                WHEN p.performance = 'Winner' THEN 1
                WHEN p.performance = 'Runner-up' THEN 2
                ELSE 3
            END
        """
        return db.fetch_all(query, (event_id,))

    def get_student_achievements(self, usn):
        """Get a student's achievements (wins and runner-ups)"""
        query = """
        SELECT e.event_id, e.name, e.event_type, e.department, 
               e.event_date, p.performance
        FROM events e
        JOIN participation p ON e.event_id = p.event_id
        WHERE p.usn = %s AND p.performance IN ('Winner', 'Runner-up')
        ORDER BY e.event_date DESC
        """
        return db.fetch_all(query, (usn,))


# For testing the module
if __name__ == "__main__":
    participation_module = ParticipationModule()
    
    # Example operations for testing
    # Register participation
    result, message = participation_module.register_participation("1MS21CS001", 1, "Participant")
    print(message)
    
    # Update performance
    result, message = participation_module.update_performance("1MS21CS001", 1, "Winner")
    print(message)
    
    # Get all participations
    participations = participation_module.get_all_participations()
    print(f"Total participations: {len(participations)}")
    
    # Get student achievements
    achievements = participation_module.get_student_achievements("1MS21CS001")
    print(f"Student achievements: {len(achievements)}")
    
    # Delete participation
    result, message = participation_module.delete_participation("1MS21CS001", 1)
    print(message)
