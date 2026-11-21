import os
import random
import time
import re
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter import messagebox
import threading
import subprocess
from pathlib import Path
import matplotlib.pyplot as plt
from weekly_report import weekly_report
from voice import speak
LOG_FILE = "study_log1.txt"
DATA_FILE = "new data .txt"   # exact original filename

import sys

IS_WINDOWS = sys.platform == "win32"
if IS_WINDOWS:
    import winsound
    sys.stdout.reconfigure(encoding="utf-8")   # lets emojis print without UnicodeEncodeError

WIN_SOUNDS = {
    "Glass": ("SystemAsterisk","SystemHand",),
    "Blow": "SystemExclamation",
    "Tink": "SystemQuestion",
    "Hero": "SystemHand",
    "Sosumi": "SystemDefault",
}


def play_sound(sound="Glass"):
    if IS_WINDOWS:
        selected = random.choice(WIN_SOUNDS.get(sound, ("SystemDefault",)))


        winsound.PlaySound(
            selected,
            winsound.SND_ALIAS | winsound.SND_ASYNC
        )
    else:
        subprocess.Popen(["afplay", f"/System/Library/Sounds/{sound}.aiff"])


def play_mp3(audio_name):
    """Open an MP3 from the same folder as this script in the default audio player."""
    audio_path = Path(__file__).resolve().parent / audio_name
    if not audio_path.is_file():
        raise FileNotFoundError(f"MP3 file not found: {audio_path}")

    if IS_WINDOWS:
        os.startfile(str(audio_path))
    elif sys.platform == "darwin":
        subprocess.Popen(["afplay", str(audio_path)])
    else:
        subprocess.Popen(["xdg-open", str(audio_path)])



def ensure_data_files():
    """
    Ensure the log files exist so read operations won't raise FileNotFoundError.
    Opening in append mode creates the file if it doesn't exist, then closes it.
    """
    open(LOG_FILE, "a").close()
    open(DATA_FILE, "a").close()


def append_records(file_path, records):
    if not records:
        return

    with open(file_path, "a+") as file:
        file.seek(0)
        existing = file.read()
        if existing and not existing.endswith(("\n", "\r")):
            file.write("\n")
        for record in records:
            file.write(f"{record}\n")


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
        
        speak("Timer's set good luck")
        
        play_sound("Tink")

        while seconds >= 0:
            mins = (seconds // 60) % 60 #// divides and round the answer to nearest value of seconds
            secs = seconds % 60         # % used as mod.
            hours = int(seconds / 3600)
            print(f"|||- ⏳  Time remaining: {hours:02}:{mins:02}:{secs:02}  ⏳ -|||", end="\r", flush=True)
            time.sleep(1)
            seconds -= 1

        print("\n⏰ Time's up! Great job studying!")
        play_sound("Hero")
        speak("time'up great job studying")

    def save_to_file(self):
        """
        Append session lines to study_log1.txt and a daily total line to new data .txt.
        Date format is YYYY-MM-DD to match view_summary and other readers.
        """
        entry_date = self.today.strftime('%Y-%m-%d')
        append_records(
            LOG_FILE,
            [f"{entry_date} | {session['topic']} | {session['time']}" for session in self.study_log],
        )
        append_records(DATA_FILE, [f"{entry_date} | {self.total_study_time}"])
        self.total_study_time = 0  # Reset after saving to avoid double counting in future sessions.
        self.study_log.clear()

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

            play_mp3("time_up.mp3")
            time_extra = int(input("How much extra time did you take? (0 if none): "))


            total_time = time_spent + time_extra
            self.total_study_time += total_time
            self.study_log.append({"topic": topic_name, "time": total_time})

            print(f"✅ Logged: {topic_name} — {total_time} minutes")
            speak(f"Logged {topic_name}: {total_time} minutes.")
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
            speak("Successfully logged your study session.", wait=False)
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
        print("\nWhich day's summary would you like to view?")
        print("1. Yesterday")
        print("2. Today")
        while True:
            day_choice = input("Select an option (1-2): ").strip()
            if day_choice in ("1", "2"):
                break
            print("❌ Invalid choice. Please select 1 for yesterday or 2 for today.")

        selected_day = date.today()
        if day_choice == "1":
            selected_day -= timedelta(days=1)
        selected_date = selected_day.strftime('%Y-%m-%d')
        day_label = "yesterday" if day_choice == "1" else "today"
        total_minutes = 0
        selected_entries = []

        try:
            with open(DATA_FILE, "r") as f:
                contents = f.read()
                records = re.finditer(
                    r"(\d{4}-\d{2}-\d{2})\s*\|\s*(-?\d+)(?=\s|$|\d{4}-\d{2}-\d{2}\s*\|)",
                    contents,
                )
                for record in records:
                    entry_date, minutes = record.groups()
                    if entry_date == selected_date:
                        total_minutes += int(minutes)
                        selected_entries.append(f"{entry_date} | {minutes} min")
        except FileNotFoundError:
            # Should not happen because ensure_data_files() runs at startup
            print("No study data file found yet.")
            return

        print(f"\n📊 Study Summary for {day_label} 📊")
        print(f"[----- You studied for a total of {total_minutes} minutes {day_label}. -----]")
        for entry in selected_entries:
            print(entry)

        if total_minutes >= 100:
            print("Great consistency! Keep it up.")
            speak(f"You studied for {total_minutes} minutes {day_label}. Great consistency! Keep it up.")
            self.motivational_quote()
        else:
            print("You're doing well—keep pushing yourself a little more!")
            speak(
                f"You studied for {total_minutes} minutes {day_label}. "
                "You're doing well. Keep pushing yourself a little more."
            )

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
                        # Extract only the numbers (e.g., "240 (Predicted...)" becomes "240")
                        time_str = parts[1].split()[0] 
                        hours = round(int(time_str) / 60, 2)
                        
                        date_obj = datetime.strptime(parts[0], "%Y-%m-%d")
                        month_name = date_obj.strftime("%B")
                        monthly_totals[month_name] = monthly_totals.get(month_name, 0) + hours
                    except ValueError:
                        continue

            if monthly_totals:
                average = sum(monthly_totals.values()) / len(monthly_totals)
                print("Average study hours per month:", round(average,1))
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
            speak(f"Goal achieved! You studied {total_from_file} minutes today.")
            play_sound("Hero")
            self.motivational_quote()
        else:
            remaining = goal - total_from_file
            print(f"⚠️ Keep going — only {remaining} more minutes to reach your goal!")
            speak(
                f"You studied {total_from_file} minutes today. "
                f"Only {remaining} more minutes to reach your goal."
            )
            self.daily_goals.append(False)

    def random_study_tip(self):
        study_tips = [
            "Break big tasks into smaller chunks.",
            "Use active recall when reviewing notes.",
            "Take short breaks every 25–30 minutes.",
            "Teach someone else to reinforce your learning.",
            "Review your mistakes—they're gold mines for growth!",
            "Simulate Exams: Practice answering questions under timed conditions."
            "When stuck, identify exactly what you know, what you need, and where the gap is."
            "Your mistakes are a personalized syllabus."
            "Don’t solve the whole problem at once. Solve the next identifiable step."
            "If you can’t explain it without your notes, you’re not done learning it."
            "Protect your deep-focus time from tasks that only look urgent."
            "If you’ve been reading the same sentence for two minutes, congratulations: you’ve discovered a very inefficient form of meditation."
        ]
        tip = random.choice(study_tips)
        print(f"\n📌 Study Tip: {tip}")
        speak(tip)


def main():
    # Ensure files exist before any read attempts
    ensure_data_files()

    tracker = StudyTracker()
    threading.Thread(
        target=speak,
        args=("How can I help you today?",),
        daemon=True,
    ).start()
    while True:
        print("\n📚 🧑‍🎓 Daily Study Tracker 📚💻")
        print(f"How can I help you today?")
        print("1. Add Study Session (with timer)")
        print("2. View Summary")
        print("3. Set Daily Goal")
        print("4. Manually Add Study Session")
        print("5. Study Tips")
        print("6. view study log & Graph")
        print("7. Weekly Study Report")
        print("8. exit")
        choice = input("\nSelect an option (1-8): ").strip()

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
            weekly_report()
        elif choice == "8":
            speak("That's it for today  sir see you soon")
            print("This is it for now, see you next time!")
            play_sound("Sosumi")
            break
        else:
            print("\n❌ Invalid choice. Please select a valid option (1-8).")

if __name__ == "__main__":
    play_mp3("welcome_back_jarvis.mp3")
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)   # keeps the popup on top on Windows
    messagebox.showinfo("Welcome",
                        "Welcome back to Daily Study Tracker.",
                        parent=root)
    root.destroy()
    main()
