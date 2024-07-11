import sys
import glob
import whisper


def get_transcription_from_audio(video_path, data_dir):
    """
    Generates captions from audio of a given video using the Whisper library.
    Returns:
    None
    """
    model = whisper.load_model("large-v2")
    video_id = video_path.split("/")[-1].split(".")[0]
    transcription_file = f"{data_dir}../transcripts/{video_id}.txt"
    captions = model.transcribe(video_path)
    with open(transcription_file, "w", encoding="utf-8") as f:
        for segment in captions["segments"]:
            f.write(f"{segment['text']}\n")



def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 transcription_wtimestamps.py /path/to/corpus")
    audio_files = glob.glob(f"{sys.argv[1]}/*.wav")
    for audio_path in audio_files:
        get_transcription_from_audio(audio_path, sys.argv[1])


if __name__ == "__main__":
    main()
