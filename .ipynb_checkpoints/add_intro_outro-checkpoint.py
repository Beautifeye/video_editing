import argparse
import os
from moviepy.editor import *

parser = argparse.ArgumentParser(description='Add intro and outro to your video.')

parser.add_argument('--intro',      help='path to the intro clip', required=True)
parser.add_argument('--outro',      help='path to the outro clip', default=None)
parser.add_argument('--input_dir',  help='folder containing all videos to be edited', required=True)
parser.add_argument('--output_dir', help='folder containing results', required=True)


def edit_video(intro, outro, video_path):
    
    # load video
    my_clip = VideoFileClip(video_path).subclip(0, 10)
    
    # add intro audio as video background
    original_audio = my_clip.audio
    intro_audio_reduced = intro.audio.volumex(0.2).audio_loop(duration=my_clip.duration)
    new_myaudio = CompositeAudioClip([my_clip.audio, intro_audio_reduced])
    my_clip.audio = new_myaudio
    
    # add transitions
    slided_clips = [
        CompositeVideoClip([intro.fx(transfx.fadeout, 2)]),
        CompositeVideoClip([my_clip]),
        CompositeVideoClip([intro.fx(transfx.fadein, 2)])
    ]
    
    # concatenate clips
    final_clip = concatenate_videoclips(slided_clips)
    
    return final_clip, original_audio
    
    
    


if __name__ == '__main__':
    
    # retrieve args
    args = parser.parse_args()
    
    # create output dir (if it exists already we keep its content)
    os.makedirs(args.output_dir, exist_ok=True)
    
    # load intro an outro
    # we subclip them since they have black screens that we don't want to load
    intro = VideoFileClip(args.intro).subclip(0, 3)
    outro = VideoFileClip(args.outro).subclip(2.5)
    
    # keep .mp4 files only
    fn_list = sorted([fn for fn in os.listdir(args.input_dir) if fn.endswith(".mp4")])
    
    # iterate video editing over all video in the input directory
    for i, fn in enumerate(fn_list):
        
        video_path = os.path.join(args.input_dir, fn)
        edited_video, original_audio = edit_video(
            intro=intro,
            outro=outro,
            video_path=video_path
        )
        
        edited_video.write_videofile(os.path.join(args.output_dir, fn.split(".")[0] + "-edited.mp4"))
        original_audio.write_audiofile(os.path.join(args.output_dir, fn.split(".")[0] + "-edited.mp3"))
        print("INFO: VIDEO {} / {} DONE".format(i + 1, len(fn_list)))
        print("-" * 50)
        print("-" * 50)
        print()