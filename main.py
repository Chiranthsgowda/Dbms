"""
main.py - Main application file for College Event Participation Tracker
"""

import os
import sys
from datetime import datetime
from db_connection import db
from student_module import StudentModule
from event_module import EventModule
from participation_module import ParticipationModule
from reports import ReportsModule


class CollegeEventTracker:
    """Main application class for College Event Participation Tracker"""
    
    def __init__(self):
        """Initialize application components"""
        self.student_module = StudentModule()
        self.event_module = EventModule()
        self.participation_module = ParticipationModule()
        self.reports_module = ReportsModule()
        
        # Define menu options
        self.main_menu = {
            '1': ('Student Management', self.student_menu),
            '2': ('Event Management', self.event_menu),
            '3': ('Participation Management', self.participation_menu),
            '4': ('Reports', self.reports_menu),
            'q': ('Quit', self.quit_application)
        }
        
        # Welcome message shown at startup
        self.welcome_message = """
        =====================================================
              COLLEGE EVENT PARTICIPATION TRACKER
        =====================================================
        A comprehensive system to track student participation 
        and performance in college events.
        
        Version 1.0.0
        =====================================================
        """
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self, menu_options, title=None):
        """Display a menu with options"""
        self.clear_screen()
        
        if title:
            print(f"\n{title}")
            print("=" * len(title))
        
        for key, (option, _) in menu_options.items():
            print(f"{key}. {option}")
        
        print("\n(Press 'b' to go back to previous menu, 'q' to quit)")
        choice = input("\nEnter your choice: ").lower()
        return choice
    
    def run(self):
        """Run the main application loop"""
        # Display welcome message once at startup
        print(self.welcome_message)
        input("Press Enter to continue...")
        
        while True:
            choice = self.display_menu(self.main_menu, "MAIN MENU")
            
            if choice in self.main_menu:
                _, function = self.main_menu[choice]
                function()
            elif choice == 'b':
                continue  # Stay in main menu
            elif choice == 'q':
                self.quit_application()
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def student_menu(self):
        """Display student management menu"""
        menu = {
            '1': ('Add New Student', self.add_student),
            '2': ('View All Students', self.view_all_students),
            '3': ('Search Students', self.search_students),
            '4': ('Update Student Details', self.update_student),
            '5': ('Delete Student', self.delete_student),
            '6': ('View Student Events', self.view_student_events)
        }
        
        while True:
            choice = self.display_menu(menu, "STUDENT MANAGEMENT")
            
            if choice in menu:
                _, function = menu[choice]
                function()
                input("\nPress Enter to continue...")
            elif choice == 'b':
                break
            elif choice == 'q':
                self.quit_application()
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def add_student(self):
        """Add a new student"""
        print("\nADD NEW STUDENT")
        print("===============")
        
        usn = input("Enter USN (format: 1MS21CS001): ").strip().upper()
        name = input("Enter Student Name: ").strip()
        department = input("Enter Department: ").strip()
        year = input("Enter Year (1-5): ").strip()
        
        success, message = self.student_module.add_student(usn, name, department, year)
        print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
    
    def view_all_students(self):
        """View all students"""
        print("\nALL STUDENTS")
        print("============")
        
        students = self.student_module.get_all_students()
        
        if not students:
            print("No students found in the database.")
            return
        
        # Display students in a tabular format
        print(f"{'USN':<12} {'Name':<25} {'Department':<20} {'Year':<5} {'Participations':<15}")
        print("-" * 80)
        
        for student in students:
            print(f"{student['usn']:<12} {student['name']:<25} {student['department']:<20} {student['year']:<5} {student['participation_count']:<15}")
    
    def search_students(self):
        """Search for students"""
        print("\nSEARCH STUDENTS")
        print("===============")
        
        search_term = input("Enter search term (USN, Name, or Department): ").strip()
        
        if not search_term:
            print("Search term cannot be empty.")
            return
        
        students = self.student_module.search_students(search_term)
        
        if not students:
            print(f"No students found matching '{search_term}'.")
            return
        
        # Display search results
        print(f"\nSearch Results for '{search_term}':")
        print(f"{'USN':<12} {'Name':<25} {'Department':<20} {'Year':<5}")
        print("-" * 65)
        
        for student in students:
            print(f"{student['usn']:<12} {student['name']:<25} {student['department']:<20} {student['year']:<5}")
    
    def update_student(self):
        """Update student details"""
        print("\nUPDATE STUDENT")
        print("==============")
        
        usn = input("Enter USN of student to update: ").strip().upper()
        
        student = self.student_module.get_student_by_usn(usn)
        if not student:
            print(f"No student found with USN: {usn}")
            return
        
        print(f"\nCurrent details for {student['name']}:")
        print(f"USN: {student['usn']}")
        print(f"Name: {student['name']}")
        print(f"Department: {student['department']}")
        print(f"Year: {student['year']}")
        
        print("\nEnter new details (press Enter to keep current value):")
        new_name = input(f"Name [{student['name']}]: ").strip() or student['name']
        new_dept = input(f"Department [{student['department']}]: ").strip() or student['department']
        new_year = input(f"Year [{student['year']}]: ").strip() or str(student['year'])
        
        success, message = self.student_module.update_student(usn, new_name, new_dept, new_year)
        print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
    
    def delete_student(self):
        """Delete a student"""
        print("\nDELETE STUDENT")
        print("==============")
        
        usn = input("Enter USN of student to delete: ").strip().upper()
        
        student = self.student_module.get_student_by_usn(usn)
        if not student:
            print(f"No student found with USN: {usn}")
            return
        
        print(f"\nYou are about to delete: {student['name']} ({student['usn']})")
        confirm = input("Are you sure? This action cannot be undone. (y/n): ").lower()
        
        if confirm == 'y':
            success, message = self.student_module.delete_student(usn)
            print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
        else:
            print("\nDeletion cancelled.")
    
    def view_student_events(self):
        """View events a student has participated in"""
        print("\nVIEW STUDENT EVENTS")
        print("===================")
        
        usn = input("Enter USN: ").strip().upper()
        
        student = self.student_module.get_student_by_usn(usn)
        if not student:
            print(f"No student found with USN: {usn}")
            return
        
        events = self.student_module.get_student_events(usn)
        if not events:
            print(f"{student['name']} has not participated in any events.")
            return
        
        print(f"\nEvents participated by {student['name']}:")
        print(f"{'Event Name':<30} {'Type':<15} {'Department':<20} {'Date':<12} {'Performance':<12}")
        print("-" * 90)
        
        for event in events:
            print(f"{event['name']:<30} {event['event_type']:<15} {event['department']:<20} {event['event_date'].strftime('%Y-%m-%d'):<12} {event['performance']:<12}")
    
    def event_menu(self):
        """Display event management menu"""
        menu = {
            '1': ('Add New Event', self.add_event),
            '2': ('View All Events', self.view_all_events),
            '3': ('Search Events', self.search_events),
            '4': ('Update Event Details', self.update_event),
            '5': ('Delete Event', self.delete_event),
            '6': ('View Event Participants', self.view_event_participants),
            '7': ('View Upcoming Events', self.view_upcoming_events),
            '8': ('View Past Events', self.view_past_events)
        }
        
        while True:
            choice = self.display_menu(menu, "EVENT MANAGEMENT")
            
            if choice in menu:
                _, function = menu[choice]
                function()
                input("\nPress Enter to continue...")
            elif choice == 'b':
                break
            elif choice == 'q':
                self.quit_application()
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def add_event(self):
        """Add a new event"""
        print("\nADD NEW EVENT")
        print("=============")
        
        name = input("Enter Event Name: ").strip()
        event_type = input("Enter Event Type (e.g., Technical, Cultural, Sports): ").strip()
        department = input("Enter Organizing Department: ").strip()
        
        # Date input with validation
        while True:
            date_str = input("Enter Event Date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        success, message = self.event_module.add_event(name, event_type, department, date_str)
        print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
    
    def view_all_events(self):
        """View all events"""
        print("\nALL EVENTS")
        print("==========")
        
        events = self.event_module.get_all_events()
        
        if not events:
            print("No events found in the database.")
            return
        
        # Display events in a tabular format
        print(f"{'ID':<5} {'Event Name':<30} {'Type':<15} {'Department':<20} {'Date':<12} {'Participants':<12}")
        print("-" * 95)
        
        for event in events:
            print(f"{event['event_id']:<5} {event['name']:<30} {event['event_type']:<15} {event['department']:<20} {event['event_date'].strftime('%Y-%m-%d'):<12} {event['participant_count']:<12}")
    
    def search_events(self):
        """Search for events"""
        print("\nSEARCH EVENTS")
        print("=============")
        
        search_term = input("Enter search term (Name, Type, or Department): ").strip()
        
        if not search_term:
            print("Search term cannot be empty.")
            return
        
        events = self.event_module.search_events(search_term)
        
        if not events:
            print(f"No events found matching '{search_term}'.")
            return
        
        # Display search results
        print(f"\nSearch Results for '{search_term}':")
        print(f"{'ID':<5} {'Event Name':<30} {'Type':<15} {'Department':<20} {'Date':<12}")
        print("-" * 85)
        
        for event in events:
            print(f"{event['event_id']:<5} {event['name']:<30} {event['event_type']:<15} {event['department']:<20} {event['event_date'].strftime('%Y-%m-%d'):<12}")
    
    def update_event(self):
        """Update event details"""
        print("\nUPDATE EVENT")
        print("============")
        
        event_id = input("Enter Event ID to update: ").strip()
        
        try:
            event_id = int(event_id)
        except ValueError:
            print("Event ID must be a number.")
            return
        
        event = self.event_module.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID: {event_id}")
            return
        
        print(f"\nCurrent details for '{event['name']}':")
        print(f"ID: {event['event_id']}")
        print(f"Name: {event['name']}")
        print(f"Type: {event['event_type']}")
        print(f"Department: {event['department']}")
        print(f"Date: {event['event_date'].strftime('%Y-%m-%d')}")
        
        print("\nEnter new details (press Enter to keep current value):")
        new_name = input(f"Name [{event['name']}]: ").strip() or event['name']
        new_type = input(f"Type [{event['event_type']}]: ").strip() or event['event_type']
        new_dept = input(f"Department [{event['department']}]: ").strip() or event['department']
        
        # Date input with validation
        while True:
            default_date = event['event_date'].strftime('%Y-%m-%d')
            new_date = input(f"Date [{default_date}]: ").strip() or default_date
            try:
                datetime.strptime(new_date, '%Y-%m-%d')
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        success, message = self.event_module.update_event(event_id, new_name, new_type, new_dept, new_date)
        print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
    
    def delete_event(self):
        """Delete an event"""
        print("\nDELETE EVENT")
        print("============")
        
        event_id = input("Enter Event ID to delete: ").strip()
        
        try:
            event_id = int(event_id)
        except ValueError:
            print("Event ID must be a number.")
            return
        
        event = self.event_module.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID: {event_id}")
            return
        
        print(f"\nYou are about to delete: {event['name']} (ID: {event['event_id']})")
        print("This will also delete all participation records for this event.")
        confirm = input("Are you sure? This action cannot be undone. (y/n): ").lower()
        
        if confirm == 'y':
            success, message = self.event_module.delete_event(event_id)
            print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
        else:
            print("\nDeletion cancelled.")
    
    def view_event_participants(self):
        """View participants for an event"""
        print("\nVIEW EVENT PARTICIPANTS")
        print("=======================")
        
        event_id = input("Enter Event ID: ").strip()
        
        try:
            event_id = int(event_id)
        except ValueError:
            print("Event ID must be a number.")
            return
        
        event = self.event_module.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID: {event_id}")
            return
        
        participants = self.event_module.get_event_participants(event_id)
        if not participants:
            print(f"No participants registered for '{event['name']}'.")
            return
        
        print(f"\nParticipants for '{event['name']}' on {event['event_date'].strftime('%Y-%m-%d')}:")
        print(f"{'USN':<12} {'Name':<25} {'Department':<20} {'Year':<5} {'Performance':<12}")
        print("-" * 80)
        
        for participant in participants:
            print(f"{participant['usn']:<12} {participant['name']:<25} {participant['department']:<20} {participant['year']:<5} {participant['performance']:<12}")
    
    def view_upcoming_events(self):
        """View upcoming events"""
        print("\nUPCOMING EVENTS")
        print("===============")
        
        events = self.event_module.get_upcoming_events()
        
        if not events:
            print("No upcoming events found.")
            return
        
        print(f"{'ID':<5} {'Event Name':<30} {'Type':<15} {'Department':<20} {'Date':<12}")
        print("-" * 85)
        
        for event in events:
            print(f"{event['event_id']:<5} {event['name']:<30} {event['event_type']:<15} {event['department']:<20} {event['event_date'].strftime('%Y-%m-%d'):<12}")
    
    def view_past_events(self):
        """View past events"""
        print("\nPAST EVENTS")
        print("===========")
        
        events = self.event_module.get_past_events()
        
        if not events:
            print("No past events found.")
            return
        
        print(f"{'ID':<5} {'Event Name':<30} {'Type':<15} {'Department':<20} {'Date':<12}")
        print("-" * 85)
        
        for event in events:
            print(f"{event['event_id']:<5} {event['name']:<30} {event['event_type']:<15} {event['department']:<20} {event['event_date'].strftime('%Y-%m-%d'):<12}")
    
    def participation_menu(self):
        """Display participation management menu"""
        menu = {
            '1': ('Register Student for Event', self.register_participation),
            '2': ('View All Participations', self.view_all_participations),
            '3': ('Update Student Performance', self.update_performance),
            '4': ('Remove Participation', self.remove_participation),
            '5': ('View Event Winners', self.view_event_winners),
            '6': ('View Student Achievements', self.view_student_achievements)
        }
        
        while True:
            choice = self.display_menu(menu, "PARTICIPATION MANAGEMENT")
            
            if choice in menu:
                _, function = menu[choice]
                function()
                input("\nPress Enter to continue...")
            elif choice == 'b':
                break
            elif choice == 'q':
                self.quit_application()
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def register_participation(self):
        """Register a student for an event"""
        print("\nREGISTER PARTICIPATION")
        print("=====================")
        
        usn = input("Enter Student USN: ").strip().upper()
        student = self.student_module.get_student_by_usn(usn)
        if not student:
            print(f"No student found with USN: {usn}")
            return
        
        event_id = input("Enter Event ID: ").strip()
        try:
            event_id = int(event_id)
        except ValueError:
            print("Event ID must be a number.")
            return
        
        event = self.event_module.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID: {event_id}")
            return
        
        print("\nPerformance Categories:")
        print("1. Winner")
        print("2. Runner-up")
        print("3. Participant")
        
        performance_choice = input("\nSelect performance (default: Participant): ").strip()
        
        if performance_choice == '1':
            performance = "Winner"
        elif performance_choice == '2':
            performance = "Runner-up"
        else:
            performance = "Participant"
        
        success, message = self.participation_module.register_participation(usn, event_id, performance)
        print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
    
    def view_all_participations(self):
        """View all participation records"""
        print("\nALL PARTICIPATIONS")
        print("=================")
        
        participations = self.participation_module.get_all_participations()
        
        if not participations:
            print("No participation records found.")
            return
        
        print(f"{'Student':<25} {'USN':<12} {'Event':<30} {'Date':<12} {'Performance':<12}")
        print("-" * 95)
        
        for p in participations:
            print(f"{p['student_name']:<25} {p['usn']:<12} {p['event_name']:<30} {p['event_date'].strftime('%Y-%m-%d'):<12} {p['performance']:<12}")
    
    def update_performance(self):
        """Update student performance in an event"""
        print("\nUPDATE PERFORMANCE")
        print("=================")
        
        usn = input("Enter Student USN: ").strip().upper()
        event_id = input("Enter Event ID: ").strip()
        
        try:
            event_id = int(event_id)
        except ValueError:
            print("Event ID must be a number.")
            return
        
        # Check if participation exists
        participation = self.participation_module.get_participation(usn, event_id)
        if not participation:
            print("No participation record found for this student and event.")
            return
        
        student = self.student_module.get_student_by_usn(usn)
        event = self.event_module.get_event_by_id(event_id)
        
        print(f"\nUpdating performance for {student['name']} in {event['name']}")
        print("Current performance:", participation['performance'])
        
        print("\nPerformance Categories:")
        print("1. Winner")
        print("2. Runner-up")
        print("3. Participant")
        
        performance_choice = input("\nSelect new performance: ").strip()
        
        if performance_choice == '1':
            performance = "Winner"
        elif performance_choice == '2':
            performance = "Runner-up"
        elif performance_choice == '3':
            performance = "Participant"
        else:
            print("Invalid choice. Using 'Participant' as default.")
            performance = "Participant"
        
        success, message = self.participation_module.update_performance(usn, event_id, performance)
        print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
    
    def remove_participation(self):
        """Remove a participation record"""
        print("\nREMOVE PARTICIPATION")
        print("===================")
        
        usn = input("Enter Student USN: ").strip().upper()
        event_id = input("Enter Event ID: ").strip()
        
        try:
            event_id = int(event_id)
        except ValueError:
            print("Event ID must be a number.")
            return
        
        # Check if participation exists
        participation = self.participation_module.get_participation(usn, event_id)
        if not participation:
            print("No participation record found for this student and event.")
            return
        
        student = self.student_module.get_student_by_usn(usn)
        event = self.event_module.get_event_by_id(event_id)
        
        print(f"\nYou are about to remove {student['name']} from {event['name']}")
        confirm = input("Are you sure? (y/n): ").lower()
        
        if confirm == 'y':
            success, message = self.participation_module.delete_participation(usn, event_id)
            print(f"\n{'SUCCESS' if success else 'ERROR'}: {message}")
        else:
            print("\nOperation cancelled.")
    
    def view_event_winners(self):
        """View winners for an event"""
        print("\nEVENT WINNERS")
        print("=============")
        
        event_id = input("Enter Event ID: ").strip()
        
        try:
            event_id = int(event_id)
        except ValueError:
            print("Event ID must be a number.")
            return
        
        event = self.event_module.get_event_by_id(event_id)
        if not event:
            print(f"No event found with ID: {event_id}")
            return
        
        winners = self.participation_module.get_event_winners(event_id)
        if not winners:
            print(f"No winners or runners-up recorded for '{event['name']}'.")
            return
        
        print(f"\nWinners for '{event['name']}' on {event['event_date'].strftime('%Y-%m-%d')}:")
        print(f"{'Performance':<12} {'USN':<12} {'Name':<25} {'Department':<20} {'Year':<5}")
        print("-" * 80)
        
        for winner in winners:
            print(f"{winner['performance']:<12} {winner['usn']:<12} {winner['name']:<25} {winner['department']:<20} {winner['year']:<5}")
    
    def view_student_achievements(self):
        """View a student's achievements"""
        print("\nSTUDENT ACHIEVEMENTS")
        print("===================")
        
        usn = input("Enter Student USN: ").strip().upper()
        
        student = self.student_module.get_student_by_usn(usn)
        if not student:
            print(f"No student found with USN: {usn}")
            return
        
        achievements = self.participation_module.get_student_achievements(usn)
        if not achievements:
            print(f"{student['name']} has no recorded achievements (wins or runner-ups).")
            return
        
        print(f"\nAchievements for {student['name']}:")
        print(f"{'Performance':<12} {'Event Name':<30} {'Type':<15} {'Department':<20} {'Date':<12}")
        print("-" * 95)
        
        for achievement in achievements:
            print(f"{achievement['performance']:<12} {achievement['name']:<30} {achievement['event_type']:<15} {achievement['department']:<20} {achievement['event_date'].strftime('%Y-%m-%d'):<12}")
    
    def reports_menu(self):
        """Display reports menu"""
        menu = {
            '1': ('Top Participating Students', self.show_top_students),
            '2': ('Department-wise Participation', self.show_department_participation),
            '3': ('Events by Participation', self.show_events_by_participation),
            '4': ('Performance Summary', self.show_performance_summary),
            '5': ('Event Type Statistics', self.show_event_type_statistics),
            '6': ('Monthly Event Summary', self.show_monthly_summary),
            '7': ('Top Performers', self.show_top_performers),
            '8': ('Generate Comprehensive Report', self.generate_comprehensive_report)
        }
        
        while True:
            choice = self.display_menu(menu, "REPORTS")
            
            if choice in menu:
                _, function = menu[choice]
                function()
                input("\nPress Enter to continue...")
            elif choice == 'b':
                break
            elif choice == 'q':
                self.quit_application()
            else:
                input("Invalid choice. Press Enter to continue...")
    
    def show_top_students(self):
        """Show top participating students"""
        print("\nTOP PARTICIPATING STUDENTS")
        print("=========================")
        
        limit = input("Number of students to show (default: 10): ").strip()
        
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            print("Using default value: 10")
            limit = 10
        
        students = self.reports_module.get_top_participating_students(limit)
        
        if not students:
            print("No participation data found.")
            return
        
        print(f"\nTop {len(students)} Participating Students:")
        print(f"{'Rank':<5} {'USN':<12} {'Name':<25} {'Department':<20} {'Year':<5} {'Participations':<15}")
        print("-" * 85)
        
        for i, student in enumerate(students, 1):
            print(f"{i:<5} {student['usn']:<12} {student['name']:<25} {student['department']:<20} {student['year']:<5} {student['participation_count']:<15}")
    
    def show_department_participation(self):
        """Show department-wise participation"""
        print("\nDEPARTMENT-WISE PARTICIPATION")
        print("============================")
        
        data = self.reports_module.get_department_wise_participation()
        
        if not data:
            print("No department participation data found.")
            return
        
        print(f"{'Department':<20} {'Students':<10} {'Events':<10} {'Participations':<15} {'Avg/Student':<12}")
        print("-" * 70)
        
        for dept in data:
            print(f"{dept['department']:<20} {dept['total_students']:<10} {dept['unique_events_participated']:<10} {dept['total_participations']:<15} {dept['avg_per_student']:<12}")
    
    def show_events_by_participation(self):
        """Show events by participation count"""
        print("\nEVENTS BY PARTICIPATION")
        print("======================")
        
        limit = input("Number of events to show (default: 10): ").strip()
        
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            print("Using default value: 10")
            limit = 10
        
        events = self.reports_module

    def show_events_by_participation(self):
        """Show events by participation count"""
        print("\nEVENTS BY PARTICIPATION")
        print("======================")
        
        limit = input("Number of events to show (default: 10): ").strip()
        
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            print("Using default value: 10")
            limit = 10
        
        events = self.reports_module.get_events_by_participation(limit)
        
        if not events:
            print("No event participation data found.")
            return
        
        print(f"\nTop {len(events)} Events by Participation:")
        print(f"{'Rank':<5} {'ID':<5} {'Event Name':<30} {'Type':<15} {'Department':<20} {'Participants':<12}")
        print("-" * 90)
        
        for i, event in enumerate(events, 1):
            print(f"{i:<5} {event['event_id']:<5} {event['name']:<30} {event['event_type']:<15} {event['department']:<20} {event['participant_count']:<12}")
    
    def show_performance_summary(self):
        """Show performance summary"""
        print("\nPERFORMANCE SUMMARY")
        print("==================")
        
        summary = self.reports_module.get_performance_summary()
        
        if not summary:
            print("No performance data found.")
            return
        
        print(f"{'Performance':<12} {'Count':<8} {'Percentage':<12}")
        print("-" * 35)
        
        total = sum(item['count'] for item in summary)
        
        for item in summary:
            percentage = (item['count'] / total * 100) if total > 0 else 0
            print(f"{item['performance']:<12} {item['count']:<8} {percentage:.2f}%")
    
    def show_event_type_statistics(self):
        """Show statistics by event type"""
        print("\nEVENT TYPE STATISTICS")
        print("====================")
        
        stats = self.reports_module.get_event_type_statistics()
        
        if not stats:
            print("No event type statistics found.")
            return
        
        print(f"{'Event Type':<20} {'Total Events':<15} {'Total Participants':<20} {'Avg/Event':<12}")
        print("-" * 70)
        
        for stat in stats:
            avg = stat['total_participants'] / stat['total_events'] if stat['total_events'] > 0 else 0
            print(f"{stat['event_type']:<20} {stat['total_events']:<15} {stat['total_participants']:<20} {avg:.2f}")
    
    def show_monthly_summary(self):
        """Show monthly event summary"""
        print("\nMONTHLY EVENT SUMMARY")
        print("====================")
        
        year = input("Enter year to analyze (default: current year): ").strip()
        
        if not year:
            year = datetime.now().year
        else:
            try:
                year = int(year)
            except ValueError:
                print(f"Invalid year. Using current year: {datetime.now().year}")
                year = datetime.now().year
        
        summary = self.reports_module.get_monthly_summary(year)
        
        if not summary:
            print(f"No event data found for year {year}.")
            return
        
        print(f"\nMonthly Event Summary for {year}:")
        print(f"{'Month':<10} {'Events':<8} {'Participants':<15} {'Winners':<10} {'Runners-up':<12}")
        print("-" * 60)
        
        months = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
        
        for item in summary:
            month_name = months[item['month']-1]
            print(f"{month_name:<10} {item['event_count']:<8} {item['participant_count']:<15} {item['winner_count']:<10} {item['runner_up_count']:<12}")
    
    def show_top_performers(self):
        """Show top performers (winners and runners-up)"""
        print("\nTOP PERFORMERS")
        print("=============")
        
        limit = input("Number of students to show (default: 10): ").strip()
        
        try:
            limit = int(limit) if limit else 10
        except ValueError:
            print("Using default value: 10")
            limit = 10
        
        performers = self.reports_module.get_top_performers(limit)
        
        if not performers:
            print("No performance data found.")
            return
        
        print(f"\nTop {len(performers)} Performers:")
        print(f"{'Rank':<5} {'USN':<12} {'Name':<25} {'Department':<20} {'Wins':<6} {'Runner-ups':<12} {'Total':<6}")
        print("-" * 90)
        
        for i, performer in enumerate(performers, 1):
            total = performer['winner_count'] + performer['runner_up_count']
            print(f"{i:<5} {performer['usn']:<12} {performer['name']:<25} {performer['department']:<20} {performer['winner_count']:<6} {performer['runner_up_count']:<12} {total:<6}")
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive report"""
        print("\nGENERATE COMPREHENSIVE REPORT")
        print("============================")
        
        # Ask for basic report parameters
        print("\nReport Parameters:")
        year = input("Year (leave blank for all years): ").strip()
        department = input("Department (leave blank for all departments): ").strip()
        event_type = input("Event Type (leave blank for all types): ").strip()
        
        # Convert year to integer if provided
        if year:
            try:
                year = int(year)
            except ValueError:
                print("Invalid year format. Using all years.")
                year = None
        else:
            year = None
        
        report = self.reports_module.generate_comprehensive_report(year, department, event_type)
        
        if not report:
            print("No data available for the specified filters.")
            return
        
        # Display report header
        print("\n" + "=" * 80)
        print("                   COLLEGE EVENT PARTICIPATION REPORT")
        print("=" * 80)
        
        # Display filter information
        print("\nReport Filters:")
        print(f"Year: {year if year else 'All Years'}")
        print(f"Department: {department if department else 'All Departments'}")
        print(f"Event Type: {event_type if event_type else 'All Event Types'}")
        print("\n" + "-" * 80)
        
        # Summary statistics
        print("\nSUMMARY STATISTICS:")
        print(f"Total Students: {report['summary']['total_students']}")
        print(f"Total Events: {report['summary']['total_events']}")
        print(f"Total Participations: {report['summary']['total_participations']}")
        print(f"Average Participations per Student: {report['summary']['avg_participations_per_student']:.2f}")
        print(f"Average Participants per Event: {report['summary']['avg_participants_per_event']:.2f}")
        
        # Department statistics
        print("\nDEPARTMENT STATISTICS:")
        print(f"{'Department':<20} {'Students':<10} {'Participations':<15} {'Avg/Student':<12}")
        print("-" * 60)
        
        for dept in report['departments']:
            print(f"{dept['department']:<20} {dept['student_count']:<10} {dept['participation_count']:<15} {dept['avg_participations']:<12}")
        
        # Event type statistics
        print("\nEVENT TYPE STATISTICS:")
        print(f"{'Event Type':<20} {'Events':<8} {'Participations':<15} {'Avg/Event':<12}")
        print("-" * 60)
        
        for event_type in report['event_types']:
            print(f"{event_type['type']:<20} {event_type['event_count']:<8} {event_type['participation_count']:<15} {event_type['avg_participations']:<12}")
        
        # Top performing students
        print("\nTOP PERFORMING STUDENTS:")
        print(f"{'USN':<12} {'Name':<25} {'Department':<20} {'Wins':<6} {'Runner-ups':<12}")
        print("-" * 80)
        
        for student in report['top_performers'][:10]:  # Show top 10
            print(f"{student['usn']:<12} {student['name']:<25} {student['department']:<20} {student['winner_count']:<6} {student['runner_up_count']:<12}")
        
        # Most popular events
        print("\nMOST POPULAR EVENTS:")
        print(f"{'Event Name':<30} {'Type':<15} {'Department':<20} {'Participants':<12}")
        print("-" * 80)
        
        for event in report['popular_events'][:10]:  # Show top 10
            print(f"{event['name']:<30} {event['event_type']:<15} {event['department']:<20} {event['participant_count']:<12}")
        
        print("\n" + "=" * 80)
        print("Report generated on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 80)
    
    def quit_application(self):
        """Exit the application"""
        print("\nThank you for using College Event Participation Tracker!")
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    try:
        # Initialize the application
        app = CollegeEventTracker()
        app.run()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)
