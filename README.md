# Subtitle Generator

A desktop app for automatically generating subtitles (`.vtt`) from `.mp4` videos using OpenAI's [Whisper](https://github.com/openai/whisper) model. Includes a simple GUI built with Tkinter.

## 📦 Features

- Select a folder with video files
- Choose a folder to save subtitles
- Extract audio from `.mp4` videos
- Transcribe audio using Whisper
- Save subtitles in `.vtt` format
- View logs in the app


## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/OlehCodefinity/subtitle-generator.git
cd subtitle-generator
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note**: Whisper requires `ffmpeg`. If you don’t have it installed:
>
> - **Windows**: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
> - **macOS**: `brew install ffmpeg`
> - **Linux**: `sudo apt install ffmpeg`

## 🚀 Usage

```bash
python main.py
```

A window will open where you can choose:
- A folder with `.mp4` videos
- A folder where subtitles should be saved

Then press "Generate Subtitles" and wait for the process to complete.

## 📂 Output

Subtitles are saved in `.vtt` format in the selected output folder.

## ⚙️ Tech Stack

- Python 3.x
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [MoviePy](https://zulko.github.io/moviepy/)

# subtitle-generator
