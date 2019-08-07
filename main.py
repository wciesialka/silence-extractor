import ffmpeg
import src.dialog as dialog
import os
import tempfile

FRAME_NAME_PATTERN = "frame-%04d.jpg"

def ask_for_file():
    file_selected = False
    video_path = None
    while not file_selected:
        video_path = dialog.open_dialog("Open Video File","MP4 files (.mp4)|*.mp4|All Files|*.*",".")
        if video_path == None:
            raise SystemExit # user clicked cancel, exit program
        file_selected = dialog.ok_cancel_dialog("Use video file\n\"" + video_path + "\"\nin Silence Extractor?","Silence Extractor")
    return video_path

def get_filename_from_path(path):
    base = os.path.basename(path)
    return os.path.splitext(base)[0]

def get_video_duration(path):
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    print(video_stream)
    return 0

def extract_frames(path):
    video_name = get_filename_from_path(path)
    frame_dir = tempfile.TemporaryDirectory(suffix=video_name)
    frame_dir_name = frame_dir.name
    save_path = os.path.join(frame_dir_name,FRAME_NAME_PATTERN)
    
    stream = ffmpeg.input(path)
    stream = ffmpeg.output(stream, save_path)
    stream.run()

    return frame_dir_name

def main():
    video_path = ask_for_file()
    duration = get_video_duration(video_path)
    # frames_dir = extract_frames(video_path)


if __name__ == "__main__":
    main()