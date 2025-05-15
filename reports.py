"""
reports.py - Reports generation module for College Event Participation Tracker
"""

from db_connection import db
from tabulate import tabulate
import os
from datetime import datetime


class ReportsModule:
    """Class to handle reports generation"""
    
    def get_top_participating_students(self, limit=10):
        """Get students with the most event participations"""
        query = """
        SELECT s.usn, s.name, s.department, s.year, 
               COUNT(p.id) AS participation_count
        FROM students s
        JOIN participation p ON s.usn = p.usn
        GROUP BY s.usn, s.name, s.department, s.year
        ORDER BY participation_count DESC
        LIMIT %s
        """
        return db.fetch_all(query, (limit,))
    
    def get_department_wise_participation(self):
        """Get participation statistics by department"""
        query = """
        SELECT s.department, 
               COUNT(DISTINCT s.usn) AS total_students,
               COUNT(DISTINCT p.event_id) AS unique_events_participated,
               COUNT(p.id) AS total_participations,
               ROUND(COUNT(p.id) / COUNT(DISTINCT s.usn), 2) AS avg_per_student
        FROM students s
        LEFT JOIN participation p ON s.usn = p.usn
        GROUP BY s.department
        ORDER BY total_participations DESC
        """
        return db.fetch_all(query)

    def get_events_by_participation(self, limit=10):
        """Get events with the most participants"""
        query = """
        SELECT e.event_id, e.name, e.event_type, e.department, 
               e.event_date, COUNT(p.id) AS participant_count
        FROM events e
        LEFT JOIN participation p ON e.event_id = p.event_id
        GROUP BY e.event_id, e.name, e.event_type, e.department, e.event_date
        ORDER BY participant_count DESC
        LIMIT %s
        """
        return db.fetch_all(query, (limit,))

    def get_performance_summary(self):
        """Get summary of student performances"""
        query = """
        SELECT s.department,
               COUNT(CASE WHEN p.performance = 'Winner' THEN 1 END) AS winners,
               COUNT(CASE WHEN p.performance = 'Runner-up' THEN 1 END) AS runners_up,
               COUNT(CASE WHEN p.performance = 'Participant' THEN 1 END) AS participants
        FROM students s
        JOIN participation p ON s.usn = p.usn
        GROUP BY s.department
        ORDER BY winners DESC, runners_up DESC
        """
        return db.fetch_all(query)

    def get_event_type_statistics(self):
        """Get statistics by event type"""
        query = """
        SELECT e.event_type,
               COUNT(DISTINCT e.event_id) AS total_events,
               COUNT(DISTINCT p.usn) AS total_unique_students,
               COUNT(p.id) AS total_participations
        FROM events e
        LEFT JOIN participation p ON e.event_id = p.event_id
        GROUP BY e.event_type
        ORDER BY total_participations DESC
        """
        return db.fetch_all(query)

    def get_monthly_event_summary(self):
        """Get monthly event and participation summary"""
        query = """
        SELECT 
            DATE_FORMAT(e.event_date, '%Y-%m') AS month,
            COUNT(DISTINCT e.event_id) AS total_events,
            COUNT(DISTINCT p.usn) AS total_participants,
            COUNT(p.id) AS total_participations
        FROM events e
        LEFT JOIN participation p ON e.event_id = p.event_id
        GROUP BY DATE_FORMAT(e.event_date, '%Y-%m')
        ORDER BY month
        """
        return db.fetch_all(query)

    def get_top_performers(self, limit=10):
        """Get top performing students based on a point system"""
        query = """
        SELECT s.usn, s.name, s.department, s.year,
               COUNT(CASE WHEN p.performance = 'Winner' THEN 1 END) AS wins,
               COUNT(CASE WHEN p.performance = 'Runner-up' THEN 1 END) AS runner_ups,
               COUNT(p.id) AS total_participations,
               (COUNT(CASE WHEN p.performance = 'Winner' THEN 1 END) * 3 + 
                COUNT(CASE WHEN p.performance = 'Runner-up' THEN 1 END) * 2 + 
                COUNT(CASE WHEN p.performance = 'Participant' THEN 1 END)) AS points
        FROM students s
        JOIN participation p ON s.usn = p.usn
        GROUP BY s.usn, s.name, s.department, s.year
        ORDER BY points DESC
        LIMIT %s
        """
        return db.fetch_all(query, (limit,))

    def format_report_table(self, data, title):
        """Format data as a table with title"""
        if not data:
            return f"\n{title}\n\nNo data available for this report."
        
        headers = data[0].keys()
        table_data = [list(row.values()) for row in data]
        
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        return f"\n{title}\n\n{table}"

    def save_report_to_file(self, report_content, filename=None):
        """Save report content to a file"""
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.txt"
        
        # Ensure the filename has .txt extension
        if not filename.endswith(".txt"):
            filename += ".txt"
        
        # Full path
        file_path = os.path.join("reports", filename)
        
        # Write to file
        with open(file_path, "w") as f:
            f.write(report_content)
        
        return file_path

    def generate_comprehensive_report(self):
        """Generate a comprehensive report combining all report types"""
        # Add report header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"COLLEGE EVENT PARTICIPATION TRACKER - COMPREHENSIVE REPORT\n"
        report += f"Generated on: {timestamp}\n"
        report += "="*80 + "\n\n"
        
        # Add top participating students
        top_students = self.get_top_participating_students(limit=10)
        report += self.format_report_table(top_students, "TOP 10 PARTICIPATING STUDENTS")
        report += "\n\n" + "="*80 + "\n\n"
        
        # Add department-wise participation
        dept_participation = self.get_department_wise_participation()
        report += self.format_report_table(dept_participation, "DEPARTMENT-WISE PARTICIPATION")
        report += "\n\n" + "="*80 + "\n\n"
        
        # Add events by participation
        top_events = self.get_events_by_participation(limit=10)
        report += self.format_report_table(top_events, "TOP 10 EVENTS BY PARTICIPATION")
        report += "\n\n" + "="*80 + "\n\n"
        
        # Add performance summary
        performance = self.get_performance_summary()
        report += self.format_report_table(performance, "PERFORMANCE SUMMARY BY DEPARTMENT")
        report += "\n\n" + "="*80 + "\n\n"
        
        # Add event type statistics
        event_stats = self.get_event_type_statistics()
        report += self.format_report_table(event_stats, "EVENT TYPE STATISTICS")
        report += "\n\n" + "="*80 + "\n\n"
        
        # Add monthly summary
        monthly = self.get_monthly_event_summary()
        report += self.format_report_table(monthly, "MONTHLY EVENT SUMMARY")
        report += "\n\n" + "="*80 + "\n\n"
        
        # Add top performers
        top_performers = self.get_top_performers(limit=10)
        report += self.format_report_table(top_performers, "TOP 10 PERFORMERS (BY POINTS)")
        
        return report


# For testing the module
if __name__ == "__main__":
    reports_module = ReportsModule()
    
    # Generate and print a sample report
    top_students = reports_module.get_top_participating_students(5)
    print(reports_module.format_report_table(top_students, "TOP 5 PARTICIPATING STUDENTS"))
    
    # Generate comprehensive report
    report = reports_module.generate_comprehensive_report()
    file_path = reports_module.save_report_to_file(report, "comprehensive_report.txt")
    print(f"Comprehensive report saved to: {file_path}")
