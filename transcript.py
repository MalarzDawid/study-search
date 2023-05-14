import os
from tqdm import tqdm
import subprocess
import whisper


def get_filename(file):
    return file.split(".")[0]


def video_to_audio(video_dir, audio_dir, ext="mp3") -> None:
    for video_file in tqdm(os.listdir(video_dir)):
        filename = get_filename(video_file)
        subprocess.call(
            [
                "ffmpeg",
                "-i",
                os.path.join(video_dir, video_file),
                os.path.join(audio_dir, f"{filename}.{ext}"),
            ]
        )


def audio_to_transcript(audio_dir, transcript_dir, model) -> None:
    for audio_file in tqdm(os.listdir(audio_dir)):
        filename = get_filename(audio_file)
        transcript = model.transcribe(os.path.join(audio_dir, audio_file))

        with open(os.path.join(transcript_dir, f"{filename}.txt"), "w") as file:
            file.writelines(transcript["text"])


if __name__ == "__main__":
    model = whisper.load_model("base")
    audio_to_transcript("data/audio", "data/transcript", model)
