# -*- coding: utf-8 -*-
import os, sys, argparse
from shutil import copyfile
sys.path.append('../')
from annotator import Annotator

def run_tool(video_file, labels_json):

    videoFileName = video_file.split("/")[-1].split(".")[0]
    
    #output_folder = f'{os.getcwd()}/output/{videoFileName}/'
    output_folder = f'./output/{videoFileName}/'
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    clips_folder = output_folder+'clips/'
    json_file = f'{output_folder}{videoFileName}.json'
    ref_labels = f'{output_folder}{videoFileName}_ref_labels.json'

    #Copy the reference json file in to the folder
    copyfile(labels_json, ref_labels)

    # Set up some folders
    clips_folder = clips_folder

    # Create the folders
    if not os.path.exists(clips_folder):
        os.mkdir(clips_folder)
        
    print(json_file)
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
        annotator.video_to_clips(video_file, clips_folder, clip_length=60, overlap=0, resize=0.5)

    # Run the annotator
    annotator.main()

"""
Example Usage: 
python badminton/example_badminton.py -f ./badminton/baddy.mp4

"""

if __name__ =="__main__":
    parser = argparse.ArgumentParser(description='sample')    
    parser.add_argument('-f', '--file_video', help='Video filename')
    parser.add_argument('-l', '--labels_json', help='Json with the required labels')

    args = parser.parse_args()

    if args.file_video and args.labels_json:
        run_tool(args.file_video, args.labels_json)
    else:
        print('Please input all the arguments required.')