# Summer internship in Telecom-Paris (june-august)

## Audio features extraction for classification/regression

### Audio features extraction

First step was to convert the whole corpus in `.wav` format from the video using the `pydub` library for that task.
We used the  `eGeMAPS feature set` and extracted the features with `OpenSMILE.` We divided the features in 5 different groups: **Frequency, Intensity, Voice quality, Spectrum and Cepstrum**. 
```
Summary of descriptors:
Frequency related parameters:
pitch (logarithmic F_0)
jitter (deviation in individual consecutive F_0)
formant 1, 2 and 3 frequency (center frequency)
formant 1 (bandwidth) 
Energy/Amplitude related parameters:
Shimmer difference of the peak amplitudes of consecutive F_0 periods
Loudness (perceived signal intensity)
Harmonic-to-Noise Ratio (HNR)
Spectral (balance) parameters:
alpha ratio
Hammarberg Index
Spectral slope 0-500 Hz and 500-1500 Hz
Formant 1, 2 and 3 relative energy
Harmonic difference H1-H2 (F_0 harmonic)
Harmonic difference H1-A3

Spectral (balance/shape/dynamics) parameters:
MFCC 1-4 (Mel-Frequency Cepstral Coefficients)
Spectral flux difference of 2 consecutive frames
Frequency related parameters:
Formant 2-3 bandwidth
```

The total number of descriptors is **88**.

### Classification

We performed **binary classification** on persuasiveness and engagement. We used 4 machine learning algorithms : **Naive Bayes, SVM, Random Forest and Logistic regression**. We also had some parameters to play with (score aggregation method and class separator especially). 
**Results:** The best **accuracy score** we had = *0.6169*. Best **f1-score** we got is *0.7611*. Class separator mean and aggregation method mean. Best score was with Logistic Regression. Generally, results were lower for engagement than persuasiveness. 
![image](https://github.com/user-attachments/assets/f32a5dd7-5cbf-49e8-ad2c-847580de71d8)
![image](https://github.com/user-attachments/assets/b650574c-dfc7-4bd4-bb38-44aaff93ec5c)

We also tried classification with audio and textual features together (concatenated). Best accuracy score = 0.5833 (almost random) with SVM.

### Regression

We performed **regression** also on persuasiveness and engagement. We used 5 different regression types: **Linear Regression, Ridge Regression, Lasso Regression, Elastic Net Regression and Random Forest Regression**. 
This time we got the best scores using Root Mean Square as an aggregation method. Best result was with Random Forest Regression (*MAE = 0.261, RMSE = 0.365*). 

![image](https://github.com/user-attachments/assets/59a8dfb9-5a8c-4049-ad74-f867122be4ff)

We tried again to **concatenate audio and textual features**. Results were globally worse than audio features solely, except for Random Forest which was similar (best results again). _MAE = 0.245, RMSE = 0.372_.

## New audio-textual features extraction

### Audio-textual alignment

We used the tool called **Montreal Forced Aligner** to generate transcript alignment. The tool uses a **pronunciation dictionary** and a pre-trained **acoustic model**. The acoustic model calculates how likely a phone is given the acoustic features, and the pronunciation dictionary is used to map words.

It generates an aligned `TextGrid` with 2 tiers: phones and words. 
Example:
![image](https://github.com/user-attachments/assets/5899e271-4bd0-4985-be3f-f82fbceeb927)

### Stressed words extraction

We used a tool called `Prosogram`, a part of it is called `Polytonia`. This tool analyses and transcripts the pitch variations in speech. It annotates the pitch levels and pitch movements in speech based on the syllables (if no syllable alignment is provided, it bases on the vowels). 
The annotation in Polytonia distinguishes 5 pitch levels: **L (low), M (mid), H (high), B (bottom) and T (top)**. The first 3 are defined relative to one another; the latter 2 are defined relative to the pitch range of the speaker. In addition there are 5 pitch movements: **R (large rise), F (large fall), r (small rise), f (small fall), and _ (level)**. Levels and movements may be combined, e.g. HF indicates a large fall starting from a high pitch level.
Example of output:

![image](https://github.com/user-attachments/assets/b2aba3c2-0814-4232-97c4-82dcd83fdc48)

The goal of our experiment is to extract some words in the audio based on their pitch level (for example, all of them who have an H or a L in them). What we want is to find out what words are stressed in speech. 

For each data sample, we generated a json file containing words and their index in the transcription which are classed as high-pitched or low-pitched. 
Example of a json file:
```json
{
	"high": [
    	{
        	"word": "end",
        	"index": 2
    	},
    	{
        	"word": "maison",
        	"index": 8
    	},
…
```
### Use of BERT embeddings
Then, the goal of the experiment is to use BERT embeddings on those words and try new models to see if this may be linked with the quality of the public speech. The BERT part is unfinished yet.

### Deep learning

We tried to train CNN from the spectrograms of the audio files but it did not work very well.

First we generated spectrograms using `librosa` python library :
![image](https://github.com/user-attachments/assets/f61c0147-0137-4252-8ab1-8a07a556db47)

Here the results:

![image](https://github.com/user-attachments/assets/863b2224-d8ce-4423-a701-6678172b3f32)

Then we tried to use a pre-trained model called `MobileNetV2` to maybe improve the accuracy on spectrogram, but it overfitted (probably because of unbalanced dataset).

![image](https://github.com/user-attachments/assets/9a5a318b-ed89-466a-b3a0-ee3df0d666a2)

## Audio-textual Pattern analysis

We performed pattern analysis for audio and text simultaneously using LIWC categories and pitch levels of words.
![image](https://github.com/user-attachments/assets/1c7fc145-7cdd-4cce-a9e6-3438f4a5bf2a)
