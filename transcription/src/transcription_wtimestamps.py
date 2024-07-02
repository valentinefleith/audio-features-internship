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
    transcription_file = f"{data_dir}../transcripts/{video_id}.csv"
    captions = model.transcribe(video_path)
    with open(transcription_file, "w", encoding="utf-8") as f:
        f.write("start;end;trancript\n")
        for segment in captions["segments"]:
            start_time = timecode_managing(segment["start"])
            end_time = timecode_managing(segment["end"])
            f.write(f"{start_time};{end_time};{segment['text']}\n")


def timecode_managing(seconds):
    """
    Formats timecodes from seconds to HH:MM:SS.

    Parameters:
    seconds (float): Time duration in seconds.

    Returns:
    str: Timecode in HH:MM:SS format.
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:03d}"


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 transcription_wtimestamps.py /path/to/corpus")
    audio_files = glob.glob(f"{sys.argv[1]}/*.wav")
    for audio_path in audio_files:
        get_transcription_from_audio(audio_path, sys.argv[1])


if __name__ == "__main__":
    main()
