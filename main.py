# Import the libraries
import os
import librosa
import soundfile as sf
import sounddevice as sd
import scipy.io.wavfile as wav

# Define the folder paths
dataset_raw_path = "Celsia/dataset_raw"
dataset_clean_path = "Celsia/dataset_clean"

# Define the minimum and maximum duration of each audio slice in seconds
min_duration = 2
max_duration = 10

# Define the sound quality options
sound_quality = "sounddevice" # Choose from "low", "medium", "uncompressed" or "sounddevice"
if sound_quality == "low":
    format = "OGG"
    subtype = "FLOAT16"
elif sound_quality == "medium":
    format = "FLAC"
    subtype = "FLOAT32"
elif sound_quality == "uncompressed":
    format = "WAV"
    subtype = "DOUBLE"
elif sound_quality == "sounddevice":
    format = None # Use NumPy arrays and scipy to save as WAV files
    subtype = None
else:
    raise ValueError("Invalid sound quality option")

# Define the stereo option
stereo = True # Set to True or False

# Create the clean folder if it does not exist
if not os.path.exists(dataset_clean_path):
    os.makedirs(dataset_clean_path)

# Loop through the files in the raw folder
for file in os.listdir(dataset_raw_path):
    # Check if the file is a wav or mp3 file
    if file.endswith(".wav") or file.endswith(".mp3"):
        # Load the audio file
        audio, sr = librosa.load(os.path.join(dataset_raw_path, file))
        # Detect the silence intervals
        intervals = librosa.effects.split(audio, top_db=30)
        # Loop through the intervals
        for i, (start, end) in enumerate(intervals):
            # Extract the slice of audio
            slice = audio[start:end]
            # Check if stereo option is enabled
            if stereo:
                # Convert the slice to mono if it has more than one channel
                if slice.ndim > 1:
                    slice = librosa.to_mono(slice)
                # Convert the slice to stereo by duplicating the channel
                slice = librosa.to_stereo(slice)
            # Calculate the duration of the slice in seconds
            duration = (end - start) / sr
            # Check if the duration is within the range
            if min_duration <= duration <= max_duration:
                # Save the slice to the clean folder with a new name and format
                new_name = file[:-4] + "_slice_" + str(i+1)
                if format is None:
                    # Use scipy to save as WAV files with NumPy arrays
                    wav.write(os.path.join(dataset_clean_path, new_name + ".wav"), sr, slice)
                else:
                    # Use soundfile to save as other formats with subtypes
                    sf.write(os.path.join(dataset_clean_path, new_name + "." + format.lower()), slice, sr, format=format, subtype=subtype)
            elif duration < min_duration:
                # Skip the slice if it is too short
                continue
            else:
                # Split the slice into smaller slices of equal length
                num_slices = int(duration / max_duration) + 1
                slice_length = int(len(slice) / num_slices)
                for j in range(num_slices):
                    # Extract the smaller slice of audio
                    small_slice = slice[j*slice_length:(j+1)*slice_length]
                    # Check if stereo option is enabled
                    if stereo:
                        # Convert the small slice to mono if it has more than one channel
                        if small_slice.ndim > 1:
                            small_slice = librosa.to_mono(small_slice)
                        # Convert the small slice to stereo by duplicating the channel
                        small_slice = librosa.to_stereo(small_slice)
                    # Calculate the duration of the smaller slice in seconds
                    small_duration = len(small_slice) / sr
                    # Check if the smaller slice fits into the range
                    if min_duration <= small_duration <= max_duration:
                        # Save the smaller slice to the clean folder with a new name and format
                        new_name = file[:-4] + "_slice_" + str(i+1) + "_" + str(j+1)
                        if format is None:
                            # Use scipy to save as WAV files with NumPy arrays
                            wav.write(os.path.join(dataset_clean_path, new_name + ".wav"), sr, small_slice)
                        else:
                            # Use soundfile to save as other formats with subtypes
                            sf.write(os.path.join(dataset_clean_path, new_name + "." + format.lower()), small_slice, sr, format=format, subtype=subtype)
                    elif small_duration > max_duration:
                        # Make a longest split that fits into the range and delete the rest of the slice
                        longest_slice = small_slice[:int(max_duration*sr)]
                        new_name = file[:-4] + "_slice_" + str(i+1) + "_" + str(j+1)
                        if format is None:
                            # Use scipy to save as WAV files with NumPy arrays
                            wav.write(os.path.join(dataset_clean_path, new_name + ".wav"), sr, longest_slice)
                        else:
                            # Use soundfile to save as other formats with subtypes
                            sf.write(os.path.join(dataset_clean_path, new_name + "." + format.lower()), longest_slice, sr, format=format, subtype=subtype)
                        break
