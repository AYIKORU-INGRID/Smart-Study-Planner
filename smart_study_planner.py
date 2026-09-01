Data_file = "study_log.txt"
def classify_session(duration):
    """ Classify a study based on the duration(in minutes)
    Short -> under 30 minutes
    Medium -> under 30 to 90 minutes (inclusive)
    Long -> over 90 minutes """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"
def add_session(sessions):
    """Prompts the user forthe subject name,topic covered a date or day label
    and the duration of the session in minutes. Ensures that the duration entered
    is positive and keeps re-asking until the valid value is given
    and also keeps the session in a list"""
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
    """
    Display every logged session in a neatly formatted table, including
    the Short/Medium/Long classification for each one.
    """
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
    """
    Display all sessions recorded for a given subject (case-insensitive
    match) along with the total time spent on it. Shows a clear message
    if no sessions match instead of an empty table.
    """
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
    """
    Compute and display overall study statistics:
    - total hours studied overall
    - total hours studied per subject
    - the subject with the least total study time (weakest area)
    - the single longest session recorded
    """
    if not sessions:
        print("\nNo study sessions have been logged yet, so no statistics to show.\n")
        return
 
    # Build a dictionary mapping subject -> total minutes studied
    subject_totals = {}
    for session in sessions:
        subject = session["subject"]
        subject_totals[subject] = subject_totals.get(subject, 0) + session["duration"]
 
    total_minutes = sum(subject_totals.values())
 
    # Subject with the least total study time = the weakest area
    weakest_subject = min(subject_totals, key=subject_totals.get)
 
    # The single longest session recorded, by duration
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
    """
    Save every logged session to a text file, one session per line,
    using '|' as a field separator. Called when the user exits.
    """
    with open(filename, "w") as file:
        for session in sessions:
            line = f"{session['subject']}|{session['topic']}|{session['date']}|{session['duration']}\n"
            file.write(line)
    print(f"Sessions saved to {filename}.")
 
 
def load_sessions(filename=Data_file):
    """
    Load sessions from the data file at programme start-up, if it
    exists. Returns an empty list (instead of crashing) if the file
    is missing, e.g. on the very first run of the programme.
    """
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
        # No saved data yet - that's fine, just start with an empty list
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
    """
    Main programme loop. Loads any existing sessions on start-up,
    displays the menu until the user chooses to exit, and rejects
    invalid choices without crashing.
    """
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
            # Invalid choice - loop back to the menu instead of crashing
            print("Invalid choice. Please enter a number from 1 to 5.")
 
 
if __name__ == "__main__":
    main()         

