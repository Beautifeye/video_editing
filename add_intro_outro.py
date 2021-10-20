import argparse
import os
from moviepy.editor import *

parser = argparse.ArgumentParser(description='Add intro and outro to your video.')

parser.add_argument('-i','--intro', help='path to the intro clip', required=True)
parser.add_argument('-v','--video', help='path to the video to edit', required=True)
parser.add_argument('-o','--outro', help='path to the outro clip', default=None)

parser.add_argument('-d','--dest', help='destination folder', default='./')

if __name__ == '__main__':
    
    # retrieve args
    args = vars(parser.parse_args())
    
    # get file_name
    fn = args['video'].split('/')[-1].split('.')[0]
    
    # add intro as outro if outro not present
    if args['outro'] is None:
        args['outro'] = args['intro']
    
    # read clips
    my_clip = VideoFileClip(args['video'])
    intro = VideoFileClip(args['intro'])
    outro = VideoFileClip(args['outro'])

    # add intro audio as video background
    intro_audio_reduced = intro.audio.volumex(0.1).audio_loop(duration=my_clip.duration)
    new_myaudio = CompositeAudioClip([my_clip.audio, intro_audio_reduced])
    my_clip.audio = new_myaudio
    
    # add transitions
    slided_clips = [
        CompositeVideoClip([intro.fx(transfx.fadeout, 2)]),
        CompositeVideoClip([my_clip.fx(transfx.crossfadein, 1).fx(transfx.crossfadeout, 1)]),
        CompositeVideoClip([intro.fx(transfx.fadein, 1).fx(transfx.fadeout, 3)])]
    
    # concatenate clips
    final_clip = concatenate_videoclips(slided_clips)
    
    # forge video
    final_clip.write_videofile(os.path.join(args['dest'], fn+'_edited.mp4'))