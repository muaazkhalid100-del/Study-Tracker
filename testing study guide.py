import random
import time
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import threading
import subprocess
import matplotlib.pyplot as plt
LOG_FILE = "study_log1.txt"


def play_sound(sound="Glass"):
    """Play a macOS system sound."""
    subprocess.Popen(["afplay", f"/System/Library/Sounds/{sound}.aiff"])


def reminder(message, delay):
    def task():
        seconds = delay
        while seconds >= 0:
            time.sleep(1)
            seconds -= 1
        print(f"\nReminder: {message}")
        play_sound("Blow")
        subprocess.Popen(["say", "Take a break if you need 1 hour already"])

    threading.Thread(target=task, daemon=True).start()


class StudyTracker:
    def __init__(self):
        self.today = datetime.today()
        self.study_log = []
        self.total_study_time = int(0)
        self.daily_goals = []

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
        play_sound("Tink")  # timer started

        while seconds >= 0:
            mins = (seconds // 60) % 60
            secs = seconds % 60
            hours = int(seconds / 3600)
            print(f"|||- ⏳  Time remaining: {hours:02}:{mins:02}:{secs:02}  ⏳ -|||", end="\r", flush=True)
            time.sleep(1)
            seconds -= 1

        print("\n⏰ Time's up! Great job studying!")
        play_sound("Hero")  # time's up!
        subprocess.Popen(["say", "Time is up! Great job studying!"])

    def save_to_file(self):
        with open(LOG_FILE, "a") as file:
            for session in self.study_log:
                file.write(f"{self.today.strftime('%Y-%m-%d')} | {session['topic']} | {session['time']}\n")
        with open("new data .txt","a") as file:
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
            time_spent = int(input(f"Enter study time in minutes for {topic_name}: "))

            self.start_timer(time_spent)
            try:
                play_sound("Tink")
                time_extra = int(input("How much extra time did you take? (0 if none):"))
            except ValueError:
                print("Sir I asked for the time you entered a wrong thing")
                time_extra = input("re-enter:")

            total_time = time_spent + time_extra
            self.total_study_time += total_time
            self.study_log.append({"topic": topic_name, "time": total_time})


            print(f"✅ Logged: {topic_name} — {total_time} minutes")
            play_sound("Glass")  # session logged

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
            print("❌ No study log found yet.")

    def view_summary(self):
        from datetime import date

        today = date.today().isoformat()  # e.g. '2026-06-12'
        total_minutes = 0
        todays_entries = []

        try:
            with open('new data .txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or '|' not in line:
                        continue
                    entry_date, minutes = [p.strip() for p in line.split('|')]
                    if entry_date == today:
                        total_minutes += int(minutes)
                        todays_entries.append(f"{entry_date} | {minutes} min")
        except FileNotFoundError:
            print("No study data file found yet.")
            return

        print('\n📊 Today\'s Study Summary 📊')
        print(f"[----- You studied for a total of {total_minutes} minutes today. -----]")
        for entry in todays_entries:
            print(entry)

        if total_minutes >= 100:
            print("Great consistency! Keep it up.")
            subprocess.Popen(["say","Keep up the great work"])
            self.motivational_quote()
        else:
            print("You're doing well—keep pushing yourself a little more!")
    def Study_graph(self):
        dates = []
        minutes = []
        try:
            with open("new data .txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split(" | ")
                    if len(parts) != 2:
                        continue  # skip corrupted/malformed lines
                    try:
                        mins = int(parts[1]) / 60
                    except ValueError:
                        continue  # skip lines where minutes isn't a clean number
                    dates.append(parts[0])
                    minutes.append(mins)
            if dates:  # only plot if we actually have valid data
                plt.plot(dates, minutes, marker=".")
                plt.xlabel("Date")
                plt.ylabel("Minutes studied")
                plt.title("Study Time Over Days")
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
                    parts = line.split(" | ")
                    if parts[0] == today:
                        minutes = int(parts[2])

                        total_from_file += minutes
        except FileNotFoundError:
            print("❌ No study log found. Start a session first!")
            return

        print(f"Your daily study time today: {total_from_file} minutes.")

        if total_from_file >= goal:
            print("✅ Goal achieved! Amazing work!")
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
    tracker = StudyTracker()
    while True:
        print("\n📚 🧑‍🎓 Daily Study Tracker 📚💻")
        print(f"Logged in today: {tracker.today.strftime('%Y-%m-%d')}")
        print("1. Add Study Session (with timer)")
        print("2. View Today's Summary")
        print("3. Check Daily Goal")
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
            print(f"Your study time today: {tracker.total_study_time} minutes")
            play_sound("Sosumi")
            break
        else:
            print("\n❌ Invalid choice. Please select a valid option (1-7).")


if __name__ == "__main__":
    subprocess.Popen(["say", "Welcome to study-tracker app ,I am alex  your assistant voice. Please press ok to proceed."])
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Welcome", "Welcome to Daily Study Tracker"
                                   "Glad You're back.")
    root.destroy()
    main()
