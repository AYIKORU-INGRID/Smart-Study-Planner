Data_file = "study_log.txt"
def classify_session(duration):
    
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"
def add_session(sessions):

    subject = input("Enter the subject name:").strip() 
    topic = input("Enter the topic:").strip() 
    date = input("Enter the date/day:").strip()

    while True:
        duration_input = input("Enter the duration of session(in minutes): ").strip()

        try:
           duration = float(duration_input)
           if duration > 0:
              break 
           else:
               print("Duration must be a positive number. Please try again.")
        except ValueError:
             print("Invalid number.Please try again.")
    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration,
    } 
    sessions.append(session)
    print(f"\nSession added: {subject}({classify_session(duration)},{duration}min)\n")   

def view_sessions(sessions):

    if not sessions:
        print("\nNo study sessions have been logged yet.\n")
        return
 
    print("\n" + "-" * 70)
    print(f"{'Subject':<15}{'Topic':<20}{'Date':<12}{'Duration':<10}{'Type':<10}")
    print("-" * 70)
 
    for session in sessions:
        classification = classify_session(session["duration"])
        print(
            f"{session['subject']:<15}"
            f"{session['topic']:<20}"
            f"{session['date']:<12}"
            f"{session['duration']:<10.0f}"
            f"{classification:<10}"
        )
 
    print("-" * 70 + "\n")
 
 
def search_by_subject(sessions, subject):
    
    matches = [s for s in sessions if s["subject"].lower() == subject.lower()]
 
    if not matches:
        print(f"\nNo sessions found for subject '{subject}'.\n")
        return
 
    print("\n" + "-" * 70)
    print(f"{'Subject':<15}{'Topic':<20}{'Date':<12}{'Duration':<10}{'Type':<10}")
    print("-" * 70)
 
    total_time = 0
    for session in matches:
        classification = classify_session(session["duration"])
        print(
            f"{session['subject']:<15}"
            f"{session['topic']:<20}"
            f"{session['date']:<12}"
            f"{session['duration']:<10.0f}"
            f"{classification:<10}"
        )
        total_time += session["duration"]
 
    print("-" * 70)
    print(f"Total time spent on {subject}: {total_time:.0f} minutes\n")
 
 
def study_statistics(sessions):

    if not sessions:
        print("\nNo study sessions have been logged yet, so no statistics to show.\n")
        return
 
    
    subject_totals = {}
    for session in sessions:
        subject = session["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + session["duration"]
 
    total_minutes = sum(subject_totals.values())
 
    
    weakest_subject = min(subject_totals, key=subject_totals.get)
 
    
    longest_session = max(sessions, key=lambda s: s["duration"])
 
    print("\n----- STUDY STATISTICS -----")
    print(f"Total time studied overall: {total_minutes / 60:.2f} hours\n")
 
    print("Time studied per subject:")
    for subject, minutes in subject_totals.items():
        print(f"  {subject:<15}: {minutes / 60:.2f} hours")
 
    print(f"\nWeakest area (least total study time): {weakest_subject}")
 
    print(
        "\nLongest session recorded: "
        f"{longest_session['subject']} - {longest_session['topic']} "
        f"({longest_session['duration']:.0f} minutes on {longest_session['date']})"
    )
    print("-----------------------------\n")
 
 
def save_sessions(sessions, filename=Data_file):
    
    with open(filename, "w") as file:
        for session in sessions:
            line = f"{session['subject']}|{session['topic']}|{session['date']}|{session['duration']}\n"
            file.write(line)
    print(f"Sessions saved to {filename}.")
 
 
def load_sessions(filename=Data_file):
    
    sessions = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                subject, topic, date, duration = line.split("|")
                sessions.append(
                    {
                        "subject": subject,
                        "topic": topic,
                        "date": date,
                        "duration": float(duration),
                    }
                )
    except FileNotFoundError:
        
        pass
 
    return sessions
 
 
def display_menu():
    """Print the main menu options."""
    print("\n===== SMART STUDY PLANNER =====")
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("================================")
 
 
def main():
    
    sessions = load_sessions()
    print(f"Loaded {len(sessions)} existing session(s) from {Data_file}.")
 
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
 
        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            subject = input("Enter subject to search for: ").strip()
            search_by_subject(sessions, subject)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Goodbye! Keep up the good study habits.")
            break
        else:
            
            print("Invalid choice. Please enter a number from 1 to 5.")
 
 
if __name__ == "__main__":
    main()         

