"""
Module to define a FeatureExtractor class for extracting audio features.
"""

import json
import librosa
import numpy as np


class FeatureExtractor:
    """
    Utility class for extracting features from audio files.
    """

    def __init__(self, config_file):
        """Initialize the FeatureExtractor object with configuration parameters from a JSON file.

        Args:
            config_file (str): Path to the JSON configuration file.
        """
        with open(config_file, 'r', encoding='utf-8') as file:
            self.config = json.load(file)

        self.mode = self.config['mode']
        self.sample_rate = self.config['sample_rate']
        self.n_fft = self.config['n_fft']
        self.hop_length = self.config['hop_length']
        self.n_mfcc = self.config['n_mfcc']
        self.deltas = self.config['deltas']
        self.max_padding = self.config['max_padding']

    def extract_features(self, filepath):
        """Extract features from an audio file.

        Args:
            filepath (str): Path to the audio file.

        Returns:
            audio_features (np.ndarray): Extracted audio features.
        """
        audio_file, _ = librosa.load(
            filepath, sr=self.sample_rate, duration=4)
        if self.mode == 'mfcc':
            audio_features = self.compute_mfcc(
                audio_file, self.sample_rate, self.n_fft, self.n_mfcc, self.deltas)
        elif self.mode == 'stft':
            audio_features = self.compute_stft(
                audio_file, self.n_fft, self.hop_length)
        elif self.mode == 'mel-spectogram':
            audio_features = self.compute_mel_spectogram(
                audio_file, self.sample_rate, self.n_fft, self.hop_length)

        audio_features = np.pad(audio_features,
                                pad_width=((0, 0), (0, self.max_padding - audio_features.shape[1])))
        audio_features = np.expand_dims(audio_features, -1)
        return audio_features

    @staticmethod
    def compute_mel_spectogram(audio_file: np.ndarray,
                               sample_rate: int,
                               n_fft: int,
                               hop_length: int
                               ):
        """Compute the Mel spectrogram of the given audio file.

        Args:
            audio_file (np.ndarray): Input audio signal.
            sample_rate (int): Sampling rate of the audio signal.
            n_fft (int): Length of the FFT window.
            hop_length (int): Hop length for the STFT.

        Returns:
            mel_spectrogram (np.ndarray): Computed Mel spectrogram.
        """
        return librosa.feature.melspectrogram(audio_file,
                                              sr=sample_rate,
                                              n_fft=n_fft,
                                              hop_length=hop_length)

    @staticmethod
    def compute_stft(audio_file: np.ndarray, n_fft: int, hop_length: int):
        """Compute the Short-Time Fourier Transform (STFT) of the given audio file.

        Args:
            audio_file (np.ndarray): Input audio signal.
            n_fft (int): Length of the FFT window.
            hop_length (int): Hop length for the STFT.

        Returns:
            stft (np.ndarray): Short-Time Fourier Transform of the audio signal.
        """
        return librosa.stft(audio_file, n_fft=n_fft, hop_length=hop_length)

    @staticmethod
    def compute_mfcc(audio_file: np.ndarray, sample_rate: int, n_fft: int, n_mfcc: int,
                     deltas=False):
        """ Compute the Mel-frequency cepstral coefficients (MFCCs) of the given audio file.

        Args:
            audio_file (np.ndarray): Input audio signal.
            sample_rate (int): Sampling rate of the audio signal.
            n_fft (int): Length of the FFT window.
            n_mfcc (int): Number of MFCCs to compute.
            deltas (bool, optional): Whether to compute delta and delta-delta features.

        Returns:
            mfccs (np.ndarray): Computed MFCCs.
        """
        mfccs = librosa.feature.mfcc(y=audio_file,
                                     sr=sample_rate,
                                     n_fft=n_fft,
                                     n_mfcc=n_mfcc,
                                     )
        # Change mode from interpolation to nearest
        if deltas:
            delta_mfccs = librosa.feature.delta(mfccs, mode='nearest')
            delta2_mfccs = librosa.feature.delta(
                mfccs, order=2, mode='nearest')
            return np.concatenate((mfccs, delta_mfccs, delta2_mfccs))
        return mfccs
