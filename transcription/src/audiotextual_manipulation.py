import sys
import glob
import parselmouth as pm
import textgrids as tgt


def get_specific_phoneme(sounds, transcripts, phoneme):
    phone_extracts = []
    for sound_path, transcript_path in zip(sounds, transcripts):
        extracts = []
        audio = pm.Sound(sound_path)
        transcript = tgt.TextGrid(transcript_path)
        # words = transcript["words"]
        phones = transcript["phones"]
        for phone in phones:
            if phone.text == phoneme:
                # print(f"ə phone: {phone.xmin} : {phone.xmax}")
                extract = audio.extract_part(
                    phone.xmin, phone.xmax, pm.WindowShape.RECTANGULAR, 1, False
                )
                extracts.append(extract)
        concatenation = audio.extract_part(
            0, 0.001, pm.WindowShape.RECTANGULAR, 1, False
        )
        concatenation = concatenation.concatenate(extracts)
        phone_extracts.append(concatenation)
    return phone_extracts


def get_empty_extracts(sounds, transcripts):
    empty_extracts = []
    for sound_path, transcript_path in zip(sounds, transcripts):
        extracts = []
        audio = pm.Sound(sound_path)
        transcript = tgt.TextGrid(transcript_path)
        words = transcript["words"]
        # phones = transcript["phones"]
        for word in words:
            if word.text == "":
                # print(f"Empty word: {word.xmin} : {word.xmax}")
                extract = audio.extract_part(
                    word.xmin, word.xmax, pm.WindowShape.RECTANGULAR, 1, False
                )
                extracts.append(extract)
        concatenation = audio.extract_part(
            0, 0.001, pm.WindowShape.RECTANGULAR, 1, False
        )
        concatenation = concatenation.concatenate(extracts)
        empty_extracts.append(concatenation)
    return empty_extracts


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 audiotextual_manipulation.py /path/to/corpus")
    corpus_dir = sys.argv[1]
    sounds = []
    transcripts = []
    with open(f"{corpus_dir}/all_folders", "r") as folders:
        all_folders = folders.readlines()
        for folder in all_folders:
            sounds += glob.glob(f"{corpus_dir}/{folder.strip()}/*.wav")
            transcripts += glob.glob(f"{corpus_dir}/{folder.strip()}/*.TextGrid")
    empty_extracts = get_empty_extracts(sounds, transcripts)
    for i, extract in enumerate(empty_extracts):
        extract.save(f"{corpus_dir}/{all_folders[i].strip()}_empty.wav", "WAV")
    e_extracts = get_specific_phoneme(sounds, transcripts, "ə")
    for i, extract in enumerate(e_extracts):
        extract.save(f"{corpus_dir}/{all_folders[i].strip()}_e.wav", "WAV")


if __name__ == "__main__":
    main()
