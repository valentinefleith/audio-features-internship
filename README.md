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

