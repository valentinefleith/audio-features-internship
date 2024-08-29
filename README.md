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



