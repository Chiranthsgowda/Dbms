"""
event_module.py - Event management module for College Event Participation Tracker
"""

from db_connection import db
from datetime import datetime


class EventModule:
    """Class to handle event-related operations"""

    def add_event(self, name, event_type, department, event_date):
        """Add a new event to the database"""
        # Validate inputs
        if not name or not event_type or not department or not event_date:
            return False, "All fields are required"
        
        # Validate date format
        try:
            # Check if the date is in the correct format
            datetime.strptime(event_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        # Insert new event
        query = """
        INSERT INTO events (name, event_type, department, event_date) 
        VALUES (%s, %s, %s, %s)
        """
        success = db.execute_query(query, (name, event_type, department, event_date))
        
        if success:
            return True, f"Event '{name}' added successfully"
        else:
            return False, "Failed to add event"

    def get_all_events(self):
        """Get all events with their participation count"""
        query = """
        SELECT e.event_id, e.name, e.event_type, e.department, 
               e.event_date, COUNT(p.id) AS participant_count
        FROM events e
        LEFT JOIN participation p ON e.event_id = p.event_id
        GROUP BY e.event_id, e.name, e.event_type, e.department, e.event_date
        ORDER BY e.event_date DESC
        """
        return db.fetch_all(query)

    def get_event_by_id(self, event_id):
        """Get event details by ID"""
        query = "SELECT * FROM events WHERE event_id = %s"
        return db.fetch_one(query, (event_id,))

    def update_event(self, event_id, name, event_type, department, event_date):
        """Update event information"""
        # Validate inputs
        if not event_id or not name or not event_type or not department or not event_date:
            return False, "All fields are required"
        
        # Validate date format
        try:
            datetime.strptime(event_date, '%Y-%m-%d')
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        # Check if event exists
        existing = self.get_event_by_id(event_id)
        if not existing:
            return False, f"Event with ID {event_id} not found"
        
        # Update event
        query = """
        UPDATE events 
        SET name = %s, event_type = %s, department = %s, event_date = %s 
        WHERE event_id = %s
        """
        success = db.execute_query(query, (name, event_type, department, event_date, event_id))
        
        if success:
            return True, f"Event '{name}' updated successfully"
        else:
            return False, "Failed to update event"

    def delete_event(self, event_id):
        """Delete an event record"""
        # Check if event exists
        existing = self.get_event_by_id(event_id)
        if not existing:
            return False, f"Event with ID {event_id} not found"
        
        # Delete event (participation records will be deleted due to CASCADE)
        query = "DELETE FROM events WHERE event_id = %s"
        success = db.execute_query(query, (event_id,))
        
        if success:
            return True, f"Event '{existing['name']}' deleted successfully"
        else:
            return False, "Failed to delete event"

    def search_events(self, search_term):
        """Search events by name, type, or department"""
        query = """
        SELECT * FROM events 
        WHERE name LIKE %s OR event_type LIKE %s OR department LIKE %s
        ORDER BY event_date DESC
        """
        search_param = f"%{search_term}%"
        return db.fetch_all(query, (search_param, search_param, search_param))

    def get_upcoming_events(self):
        """Get events that haven't occurred yet"""
        query = """
        SELECT * FROM events 
        WHERE event_date >= CURDATE()
        ORDER BY event_date ASC
        """
        return db.fetch_all(query)
    
    def get_past_events(self):
        """Get events that have already occurred"""
        query = """
        SELECT * FROM events 
        WHERE event_date < CURDATE()
        ORDER BY event_date DESC
        """
        return db.fetch_all(query)

    def get_department_events(self, department):
        """Get events for a specific department"""
        query = """
        SELECT * FROM events 
        WHERE department = %s
        ORDER BY event_date DESC
        """
        return db.fetch_all(query, (department,))
    
    def get_event_participants(self, event_id):
        """Get all participants for an event"""
        query = """
        SELECT s.usn, s.name, s.department, s.year, p.performance
        FROM students s
        JOIN participation p ON s.usn = p.usn
        WHERE p.event_id = %s
        ORDER BY p.performance, s.name
        """
        return db.fetch_all(query, (event_id,))


# For testing the module
if __name__ == "__main__":
    event_module = EventModule()
    
    # Example operations for testing
    # Add an event
    result, message = event_module.add_event("Test Event", "Technical", "Computer Science", "2025-12-25")
    print(message)
    
    # Get all events
    events = event_module.get_all_events()
    print(f"Total events: {len(events)}")
    
    # Get upcoming events
    upcoming = event_module.get_upcoming_events()
    print(f"Upcoming events: {len(upcoming)}")
    
    # Get event by ID
    event = event_module.get_event_by_id(1)
    if event:
        print(f"Found event: {event['name']}")
    
    # Update event
    if event:
        result, message = event_module.update_event(1, event['name'], event['event_type'], 
                                                 event['department'], "2025-12-31")
        print(message)
    
    # Delete the test event (get its ID first)
    test_events = event_module.search_events("Test Event")
    if test_events:
        result, message = event_module.delete_event(test_events[0]['event_id'])
        print(message)
