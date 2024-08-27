import textgrids as tgt
# to download : pip install praat-textgrids

TEXTGRID_PATH = "ALS01.TextGrid"

words = tgt.TextGrid(TEXTGRID_PATH)["words"]
for word in words:
    # Check if this is a pause
    if word.text == "":
        continue
    print(word.text)
    print(word.xmin)
    print(words.xmax)

all_words = [word.text for word in words if word.text != ""]
print(all_words)
