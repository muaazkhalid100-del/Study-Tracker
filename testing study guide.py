import random
import time
from datetime import datetime, date
import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
import matplotlib.pyplot as plt

LOG_FILE = "study_log1.txt"
DATA_FILE = "new data .txt"   # exact original filename


def play_sound(sound="Glass"):
    """Play a macOS system sound."""
    subprocess.Popen(["afplay", f"/System/Library/Sounds/{sound}.aiff"])


def reminder(message, delay):
    """Reminder to take a break after delay seconds."""
    def task():
        time.sleep(delay)
        print(f"\nReminder: {message}")
        play_sound("Blow")
        subprocess.Popen(["say", "Take a break if you need 1 hour already"])
    threading.Thread(target=task, daemon=True).start()


def ensure_data_files():
    """
    Ensure the log files exist so read operations won't raise FileNotFoundError.
    Opening in append mode creates the file if it doesn't exist, then closes it.
    """
    open(LOG_FILE, "a").close()
    open(DATA_FILE, "a").close()


class StudyTracker:
    def __init__(self):
        self.today = datetime.today()
        self.study_log = []
        self.total_study_time = 0
        self.daily_goals = []
    def gettotalstudytime(self):
        return self.total_study_time

    def motivational_quote(self):
        quotes = [
            "The beautiful thing about learning is that no one can take it away from you. - B.B. King",
            "It always seems impossible until it's done.",
            "The harder you work for something, the greater you'll feel when you achieve it.",
            "Great things are done by a series of small things brought together. - Vincent van Gogh",
            "Education is our passport to the future, for tomorrow belongs to the people who prepare for it today.",
            "Learning is a treasure that will follow its owner everywhere."
        ]
        print("\n🌟 Motivational Quote 🌟")
        print(random.choice(quotes))

    def start_timer(self, minutes):
        seconds = minutes * 60
        print(f"\n< Timer set for {minutes} minutes. Starting now... >")
        subprocess.Popen(["say", "Timer is set Good Luck."])
        play_sound("Tink")

        while seconds >= 0:
            mins = (seconds // 60) % 60
            secs = seconds % 60
            hours = int(seconds / 3600)
            print(f"|||- ⏳  Time remaining: {hours:02}:{mins:02}:{secs:02}  ⏳ -|||", end="\r", flush=True)
            time.sleep(1)
            seconds -= 1

        print("\n⏰ Time's up! Great job studying!")
        play_sound("Hero")
        subprocess.Popen(["say", "Time is up! Great job studying!"])

    def save_to_file(self):
        """
        Append session lines to study_log1.txt and a daily total line to new data .txt.
        Date format is YYYY-MM-DD to match view_summary and other readers.
        """
        with open(LOG_FILE, "a") as file:
            for session in self.study_log:
                file.write(f"{self.today.strftime('%Y-%m-%d')} | {session['topic']} | {session['time']}\n")
        with open(DATA_FILE, "a") as file:
            file.write(f"{self.today.strftime('%Y-%m-%d')} | {self.total_study_time}\n")

    def add_study_session(self):
        while True:
            try:
                play_sound("Tink")
                topic_num = int(input("Enter the number of topics you want to study today: "))
                break
            except ValueError:
                print("Invalid! Please re-enter a number.")

        for count in range(1, topic_num + 1):
            play_sound("Tink")
            topic_name = input(f"\nEnter the name of topic {count}: ")
            play_sound("Tink")
            while True:
                try:
                    time_spent = int(input(f"Enter study time in minutes for {topic_name}: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter minutes as a number.")

            self.start_timer(time_spent)
            try:
                play_sound("Tink")
                time_extra = int(input("How much extra time did you take? (0 if none): "))
            except ValueError:
                print("Invalid input, defaulting to 0.")
                time_extra = 0

            total_time = time_spent + time_extra
            self.total_study_time += total_time
            self.study_log.append({"topic": topic_name, "time": total_time})

            print(f"✅ Logged: {topic_name} — {total_time} minutes")
            play_sound("Glass")

        self.save_to_file()
        print(f"\n📊 Total study time recorded today: {self.total_study_time} minutes.")

    def manually_add_session(self):
        print("📚 You're about to log a study session. Press Enter to continue ➡️")
        input()

        try:
            topic_total = int(input("🔢 How many topics did you study? "))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return

        for i in range(topic_total):
            play_sound("Tink")
            topic_name = input(f"📝 Enter the name of topic #{i + 1}: ")
            try:
                time_spent = int(input(f"⏱️ Time spent on '{topic_name}' (in minutes): "))
            except ValueError:
                print("❌ Invalid time input. Skipping this topic.")
                continue

            self.total_study_time += time_spent
            self.study_log.append({"topic": topic_name, "time": time_spent})
            self.save_to_file()
            print(f"✅ Logged: {topic_name} — {time_spent} minutes")
            subprocess.Popen(["say", "Successfully logged"])
            play_sound("Glass")

        print(f"\n📊 Total study time recorded so far: {self.total_study_time} minutes")

    def view_study_log(self):
        try:
            with open(LOG_FILE, "r") as file:
                print("\n📜 Study Log:")
                for line in file:
                    line = line.strip()
                    if line:
                        print(line)
        except FileNotFoundError:
            # Should not happen because ensure_data_files() runs at startup
            print("❌ No study log found yet. Start a session to create the log file.")

    def view_summary(self):
        today = date.today().strftime('%Y-%m-%d')
        total_minutes = 0
        todays_entries = []

        try:
            with open(DATA_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) != 2:
                        continue
                    entry_date, minutes = parts
                    if entry_date == today:
                        try:
                            total_minutes += int(minutes)
                            todays_entries.append(f"{entry_date} | {minutes} min")
                        except ValueError:
                            # skip malformed minutes
                            continue
        except FileNotFoundError:
            # Should not happen because ensure_data_files() runs at startup
            print("No study data file found yet.")
            return

        print("\n📊 Today's Study Summary 📊")
        print(f"[----- You studied for a total of {total_minutes} minutes today. -----]")
        for entry in todays_entries:
            print(entry)

        if total_minutes >= 100:
            print("Great consistency! Keep it up.")
            subprocess.Popen(["say", "Keep up the great work"])
            self.motivational_quote()
        else:
            print("You're doing well—keep pushing yourself a little more!")

    def Study_graph(self):
        monthly_totals = {}
        try:
            with open(DATA_FILE, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line or "|" not in line:
                        continue
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) != 2:
                        continue
                    try:
                        hours = int(parts[1]) / 60
                        date_obj = datetime.strptime(parts[0], "%Y-%m-%d")
                        month_name = date_obj.strftime("%B")
                        monthly_totals[month_name] = monthly_totals.get(month_name, 0) + hours
                    except ValueError:
                        continue

            if monthly_totals:
                average = sum(monthly_totals.values()) / len(monthly_totals)
                print("Average study hours per month:", average)
                print("Monthly totals:", monthly_totals)

                months = list(monthly_totals.keys())
                totals = list(monthly_totals.values())

                plt.bar(months, totals, color="#4260f5")
                plt.xlabel("Month", family="Arial")
                plt.ylabel("Hours studied", family="Arial")
                plt.title("Study Time Per Month", fontweight="bold", color="#4260f5")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            else:
                print("No valid study data to plot yet.")
        except FileNotFoundError:
            print("No study data file found yet.")

    def check_daily_goal(self):
        try:
            goal = int(input("\nEnter your daily study goal in minutes: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return

        today = datetime.today().strftime('%Y-%m-%d')
        total_from_file = 0

        try:
            with open(LOG_FILE, "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) >= 3 and parts[0] == today:
                        try:
                            minutes = int(parts[2])
                            total_from_file += minutes
                        except ValueError:
                            continue
        except FileNotFoundError:
            print("❌ No study log found. Start a session first!")
            return

        print(f"Your daily study time today: {total_from_file} minutes.")

        if total_from_file >= goal:
            print("✅ Goal achieved! Amazing work")
            play_sound("Hero")
            self.motivational_quote()
        else:
            remaining = goal - total_from_file
            print(f"⚠️ Keep going — only {remaining} more minutes to reach your goal!")
            self.daily_goals.append(False)

    def random_study_tip(self):
        study_tips = [
            "Break big tasks into smaller chunks.",
            "Use active recall when reviewing notes.",
            "Take short breaks every 25–30 minutes.",
            "Teach someone else to reinforce your learning.",
            "Review your mistakes—they're gold mines for growth!",
            "Simulate Exams: Practice answering questions under timed conditions."
        ]
        print(f"\n📌 Study Tip: {random.choice(study_tips)}")


def main():
    # Ensure files exist before any read attempts
    ensure_data_files()

    tracker = StudyTracker()
    while True:
        print("\n📚 🧑‍🎓 Daily Study Tracker 📚💻")
        print(f"Logged in today: {tracker.today.strftime('%Y-%m-%d')}")
        print("1. Add Study Session (with timer)")
        print("2. View Today's Summary")
        print("3. Set Daily Goal")
        print("4. Manually Add Study Session")
        print("5. Study Tips")
        print("6. view study log & Graph")
        print("7. exit")
        reminder("Take a break if you need 1hr into studying", 3600)  # reminder for a break after an hour completes.
        choice = input("\nSelect an option (1-7): ").strip()

        if choice == "1":
            tracker.add_study_session()
        elif choice == "2":
            tracker.view_summary()
        elif choice == "3":
            tracker.check_daily_goal()
        elif choice == "4":
            tracker.manually_add_session()
        elif choice == "5":
            tracker.random_study_tip()
        elif choice == "6":
            tracker.view_study_log()
            tracker.Study_graph()
        elif choice == "7":
            subprocess.Popen(["say", "That's it for today Sir ,   see you soon"])
            print("This is it for now, see you next time!")
            play_sound("Sosumi")
            break
        else:
            print("\n❌ Invalid choice. Please select a valid option (1-7).")


if __name__ == "__main__":
    subprocess.Popen(["say", "Welcome from your assistant voice. Glad You're back."])
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Welcome", "Welcome to Daily Study Tracker"
                                   "Glad You're back.")
    root.destroy()
    main()
