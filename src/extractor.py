import ffmpeg
import os
import tempfile
import re
from pydub import AudioSegment
import math

FRAME_NAME_PATTERN = "frame-%08d.jpg"

def get_filename_from_path(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

FRACTION_PATTERN = r"(\d+)/(\d+)"
FRACTION_RE = re.compile(FRACTION_PATTERN)

def convert_fraction(frac):
    match = FRACTION_RE.match(frac)
    return float(match[1]) / float(match[2])

def get_video_duration(path):
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    time_base = video_stream["time_base"]
    duration_ts = video_stream["duration_ts"]
    duration = convert_fraction(time_base) * float(duration_ts)
    return duration

def extract_frames(path,frame_dir_name):
    save_path = os.path.join(frame_dir_name,FRAME_NAME_PATTERN)
    
    stream = ffmpeg.input(path)
    stream = ffmpeg.output(stream, save_path)
    stream.run()

def extract_audio(path,audio_dir_name):
    save_path = os.path.join(audio_dir_name,"audio.mp3")
    
    stream = ffmpeg.input(path)
    stream = ffmpeg.output(stream, save_path, acodec="libmp3lame",f="mp3")
    stream.run()

    return save_path

def translate(value, from_min, from_max, to_min, to_max):
    from_range = from_max - from_min
    to_range = to_max - to_min

    left_mapped = float(value - from_min) / float(from_range)

    translated = to_min + (left_mapped * to_range)

    if translated < 0.0001 or math.isinf(translated):
        return 0
    else:
        return translated

SILENCE = -99.5
LOUDEST = 99.5

def to_db(amplitude):
    return 10 * math.log(amplitude)

def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    else:
        return False

def remove_frame(frame_number,frame_dir_path):
    filename = "frame-{:08d}.jpg".format(frame_number)
    filepath = os.path.join(frame_dir_path,filename)
    delete_file(filepath)

def extract(input_path,output_path,threshold_ratio=0.7):
    video_name = get_filename_from_path(input_path)

    temp_dir = tempfile.TemporaryDirectory(suffix="_"+video_name)
    temp_dir_name = temp_dir.name

    duration = get_video_duration(input_path)
    duration_millis = duration*1000
    
    extract_frames(input_path,temp_dir_name)

    framecount = len([name for name in os.listdir(temp_dir_name) if os.path.isfile(os.path.join(temp_dir_name, name))])
    fps = framecount/duration
    
    millis_per_frame = duration_millis/framecount

    audio_path = extract_audio(input_path,temp_dir_name)

    audio = AudioSegment.from_file(audio_path)

    threshold = LOUDEST*threshold_ratio

    new_audio = AudioSegment.empty()
    for i in range(1,framecount):
        start = (i-1) * millis_per_frame
        end = i * millis_per_frame
        clip = audio[start:end]
        volume = to_db(clip.max)
        if volume > threshold:
            remove_frame(i,temp_dir_name)
        else:
            new_audio += clip

    new_audio_path = os.path.join(temp_dir_name,"new_audio.mp3")

    new_audio.export(new_audio_path, format="mp3")

    frames_stream = ffmpeg.input(temp_dir_name+ "/*.jpg", pattern_type='glob', framerate=fps)
    audio_stream = ffmpeg.input(new_audio_path)
    stream = ffmpeg.output(frames_stream,audio_stream,output_path)
    try:
        stream.run()
    except:
        return False
    else:
        return os.path.exists(output_path)