# video_editing
Video editing automations

1/ Intro & Outro blended on main track
2/ background sound track during main audio
3/ extract .mp3 file from final clip

input_dir 	: directory where all clips to edit are to be placed 
output_dir	: directory where all final clips, audio and other files will be saved 
intro 		: intro clip, to be appended at the beginning of each clip in input_dir
outro		: outro clip to be appended at the end of each clip in input_dir
bg_music 	: music file to mix in background with audio of each file in input_dir 


@todo 

- if output_dir is not given automatically create a directory called sparkd_video_output
- if bg_music is not provided, skip the mixing with clip audio 
- parameterise padding and background_mixed_track_level, so that from the args of the script I can pass the desired parameters 