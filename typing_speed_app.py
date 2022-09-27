import customtkinter
import random
import threading
import time

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class TypingSpeedApp:

    def __init__(self):
        self.all_words = []
        self.correct_words = []
        self.user_words = []
        self.wrong_words_idx = []
        self.random_words = ""

        self.running = False
        self.counter = 60
        self.passed_seconds = 0

        self.start_time = time.time()

        self.all_cpm_times = []
        self.all_wpm_times = []

        self.root = customtkinter.CTk()
        self.root.title("Typing Speed Test")
        self.root.geometry("720x500")

        self.timer_label = customtkinter.CTkLabel(master=self.root, text=f"Time Left: {self.counter}", text_font=("Helvetica", 14))
        self.timer_label.place(relx=0.14, rely=0.24, anchor='w')

        self.speed_label_cpm = customtkinter.CTkLabel(master=self.root, text="Speed: 0 CPM", text_font=("Helvetica", 14))
        self.speed_label_cpm.place(relx=0.65, rely=0.20, anchor='w')

        self.speed_label_wpm = customtkinter.CTkLabel(master=self.root, text="Speed: 0 WPM", text_font=("Helvetica", 14))
        self.speed_label_wpm.place(relx=0.65, rely=0.26)

        self.frame = customtkinter.CTkFrame(master=self.root, width=500, height=300, corner_radius=10)
        self.frame.pack(expand=True)

        self.label_upper = customtkinter.CTkLabel(master=self.frame, text=self.random_sentence(), text_font=("Helvetica", 20))
        self.label_upper.pack(padx=20, pady=20)

        self.entry = customtkinter.CTkEntry(master=self.frame, width=450, height=40, border_width=2, corner_radius=10)
        self.entry.pack(padx=20, pady=20)
        self.entry.bind("<KeyRelease>", self.start)

        self.root.mainloop()

    def random_sentence(self):
        if not self.all_words:
            with open("words.txt") as file:
                for word in file:
                    self.all_words.append(word.strip('\n'))
        self.random_words = ""
        for _ in range(6):
            self.random_words += f"{random.choice(self.all_words)} "
        return self.random_words

    def start(self, event):
        if not self.running:
            if not event.keycode in [16, 17, 18]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()
        self.check_texts()

    def check_texts(self):
        self.correct_words = []
        self.user_words = []
        self.wrong_words_idx = []

        self.correct_words = self.random_words.split(" ")[:-1]
        self.user_words = self.entry.get().split(" ")
        try:
            for index in range(len(self.correct_words)):
                if self.counter == 0:
                    self.entry.delete(0, 'end')
                    break
                if not self.wrong_words_idx:

                    if self.correct_words[index] == self.user_words[index]:
                        self.entry.configure(fg='green')

                    elif self.user_words[index] == "":
                        if self.user_words[index - 1] != self.correct_words[index - 1]:
                            self.wrong_words_idx.append(index - 1)
                            self.entry.configure(fg='red')

                    elif len(self.user_words[index]) >= len(self.correct_words[index]) and self.correct_words[index] != self.user_words[index]:
                        self.entry.configure(fg='red')

                    elif len(self.user_words[index]) < len(self.correct_words[index]):
                        self.entry.configure(fg='green')

                    # Check if user input is equal to random words
                    if len(self.user_words) == len(self.correct_words) + 1:
                        if self.user_words[-2] != self.correct_words[-1]:
                            self.wrong_words_idx.append(index - 1)
                            self.entry.configure(fg='red')
                        # Check if time is up
                        elif None:
                            pass
                        else:
                            # Generate new random words
                            self.entry.delete(0, 'end')
                            self.start_time = time.time()
                            self.passed_seconds = 0
                            self.label_upper.configure(text=self.random_sentence())
                            self.check_texts()
                else:
                    for wrong_word_idx in self.wrong_words_idx:
                        if self.correct_words[wrong_word_idx] == self.user_words[wrong_word_idx]:
                            self.wrong_words_idx.remove(wrong_word_idx)
                    self.entry.configure(fg='red')

        except IndexError:
            pass

    def time_thread(self):
        self.start_time = time.time()
        while self.running:
            if self.counter == 0:
                self.speed_label_cpm.configure(text=f"Final speed: {self.average(self.all_cpm_times)} CPM")
                self.speed_label_wpm.configure(text=f"Final speed: {self.average(self.all_wpm_times)} WPM")
                break
            time_elapse = max(time.time() - self.start_time, 1)
            time.sleep(1)
            self.passed_seconds += 1
            self.counter -= 1

            cps = len(self.entry.get()) / self.passed_seconds
            cpm = cps * 60

            wpm = (len(self.entry.get()) / (time_elapse / 60)) / 6

            last_time_cpm = round(cpm)
            last_time_wpm = round(wpm)

            self.timer_label.configure(text=f"Time Left: {self.counter}")
            self.speed_label_cpm.configure(text=f"Speed: {last_time_cpm} CPM")
            self.speed_label_wpm.configure(text=f"Speed: {last_time_wpm} WPM")

            self.all_cpm_times.append(last_time_cpm)
            self.all_wpm_times.append(last_time_wpm)

    def average(self, lst):
        return round(sum(lst) / len(lst))
