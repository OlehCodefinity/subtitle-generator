import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import whisper
import os
from moviepy import *
import ssl
import threading

# Виправлення SSL-помилки
ssl._create_default_https_context = ssl._create_unverified_context


class SubtitleGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор субтитрів")

        self.video_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.model = whisper.load_model("base")

        self.create_widgets()

    def create_widgets(self):
        # Поле вибору директорії з відео
        tk.Label(self.root, text="Папка з відео:").pack(anchor="w")
        tk.Entry(self.root, textvariable=self.video_dir, width=50).pack(anchor="w")
        tk.Button(self.root, text="Обрати папку", command=self.browse_video_directory).pack(anchor="w")

        # Поле вибору директорії для субтитрів
        tk.Label(self.root, text="Директорія для субтитрів:").pack(anchor="w")
        tk.Entry(self.root, textvariable=self.output_dir, width=50).pack(anchor="w")
        tk.Button(self.root, text="Обрати папку", command=self.browse_output_directory).pack(anchor="w")

        # Кнопка запуску генерації
        tk.Button(self.root, text="Генерувати субтитри", command=self.start_generation).pack()

        # Логи
        tk.Label(self.root, text="Логи:").pack(anchor="w")
        self.log_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.log_text.pack()

    def browse_video_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.video_dir.set(directory)

    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir.set(directory)

    def start_generation(self):
        video_dir = self.video_dir.get()
        output_dir = self.output_dir.get()

        if not video_dir or not output_dir:
            messagebox.showerror("Помилка", "Оберіть папку з відео та папку для субтитрів")
            return

        self.log("Починається обробка відео...")
        threading.Thread(target=self.generate_subtitles, args=(video_dir, output_dir)).start()

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_mp4_files(self, directory):
        return [file for file in os.listdir(directory) if file.endswith(".mp4")]

    def extract_audio(self, video_path, audio_path="temp_audio.mp3"):
        self.log(f"Витягуємо аудіо з {video_path}...")
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, codec='mp3')
        return audio_path

    def transcribe_audio(self, video_path):
        self.log(f"Транскрибуємо аудіо з {video_path}...")
        audio_path = self.extract_audio(video_path)
        result = self.model.transcribe(audio_path)
        os.remove(audio_path)
        return result["segments"]

    def save_vtt(self, segments, output_vtt):
        self.log(f"Зберігаємо субтитри у {output_vtt}...")
        with open(output_vtt, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for segment in segments:
                start_time = self.format_time_vtt(segment["start"])
                end_time = self.format_time_vtt(segment["end"])
                text = segment["text"]
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        self.log(f"Субтитри збережено у {output_vtt}")

    def format_time_vtt(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{milliseconds:03}"

    def generate_subtitles(self, video_dir, output_dir):
        mp4_files = self.get_mp4_files(video_dir)

        if not mp4_files:
            self.log("MP4 файли не знайдено.")
            return



        for file in mp4_files:
            video_path = os.path.join(video_dir, file)
            output_vtt = os.path.join(output_dir, os.path.splitext(file)[0] + ".vtt")

            self.log(f"Обробка: {file}")
            segments = self.transcribe_audio(video_path)
            self.save_vtt(segments, output_vtt)

        self.log("Готово!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleGeneratorApp(root)
    root.mainloop()