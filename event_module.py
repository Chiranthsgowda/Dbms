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
