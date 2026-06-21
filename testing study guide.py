import time
import random
from datetime import datetime
import threading
import subprocess


LOG_FILE = "study_log1.txt"


def play_sound(sound="Glass"):
    """Play a macOS system sound."""
    subprocess.Popen(["afplay", f"/System/Library/Sounds/{sound}.aiff"])


def reminder(message, delay):   #This will remind to take a break after first 55 minutes of opening the app.
    def task():
        time.sleep(delay)
        print(f"\nReminder: {message}")
        play_sound("Ping")
    threading.Thread(target=task, daemon=True).start()
    reminder("Reminder: take a break...", 3300)


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
            mins = seconds // 60
            secs = seconds % 60
            print(f"|||- ⏳  Time remaining: {mins:02}:{secs:02}  ⏳ -|||", end="\r", flush=True)
            time.sleep(1)
            seconds -= 1

        print("\n⏰ Time's up! Great job studying!")
        play_sound("Hero")  # time's up!
        subprocess.Popen(["say", "Time is up! Great job studying!"])

    def save_to_file(self):
        with open(LOG_FILE, "a") as file:
            for session in self.study_log:
                file.write(f"{self.today.strftime('%Y-%m-%d')} | {session['topic']} | {session['time']}\n")

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

            play_sound("Tink")
            time_extra = int(input("How much extra time did you take? (0 if none): "))

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
            print(f"✅ Logged: {topic_name} — {time_spent} minutes")
            play_sound("Glass")

        self.save_to_file()
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
        print('\n📊 Today\'s Study Summary 📊')
        print(f"[----- You studied for a total of {self.total_study_time} minutes today. -----]")
        print(self.study_log)
        if self.total_study_time >= 100:
            print("Great consistency! Keep it up.")
            self.motivational_quote()
        else:
            print("You're doing well—keep pushing yourself a little more!")

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
        print("6. view study log")
        print("7. exit")

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
        elif choice == "7":
            print("This is it for now, see you next time!")
            print(f"Your study time today: {tracker.total_study_time} minutes")
            play_sound("Sosumi")
            break
        else:
            print("\n❌ Invalid choice. Please select a valid option (1-7).")


if __name__ == "__main__":
    main()
