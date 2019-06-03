# -*- coding: utf-8 -*-

import os
import sys
sys.path.append('../')
from pytube import YouTube
from annotator import Annotator
import argparse



def run_tool(clips_folder, video_file, json_file):

    # Set up some folders
    clips_folder = clips_folder
    youtube_filename = video_file

    # Create the folders
    if not os.path.exists(clips_folder):
        os.mkdir(clips_folder)
        
    # Initialise the annotator
    annotator = Annotator([
            {'name': 'play', 'color': (0, 255, 0)},
            {'name': 'no_play', 'color': (0, 0, 255)}],
            clips_folder, sort_files_list=True, N_show_approx=16, screen_ratio=16/9, 
            image_resize=1, loop_duration=None, annotation_file=json_file)

    bClippingRequired = True
    try:
        filesArr = os.listdir(clips_folder)
        if len(filesArr) > 0:
            bClippingRequired = False
    except:
        print("no files")

    if bClippingRequired:
        # Split the video into clips
        print('Generating clips from the video...')
        annotator.video_to_clips(youtube_filename, clips_folder, clip_length=60, overlap=0, resize=0.5)

    # Run the annotator
    annotator.main()

"""
Example Usage: 
python badminton/example_badminton.py -f ./badminton/baddy.mp4

"""

if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='sample')    
    parser.add_argument('-f', '--file_video', help='Video filename')    

    args = parser.parse_args()

    videoFileName = args.file_video.split("/")[-1].split(".")[0]
    clips_folder = os.path.dirname(args.file_video) + "/clips_" + videoFileName
    json_file = args.file_video.replace("mp4", "json")

    

    if args.file_video:
        run_tool(clips_folder, args.file_video, json_file)