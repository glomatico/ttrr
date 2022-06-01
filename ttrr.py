from glob import glob
import os
import shutil
import random
import traceback


def main():
    phase_files = glob('phase_*.mf')
    if not phase_files:
        exit("No phase files were found! Make sure to run this program inside Toontown Rewritten's game folder.")
    phase_folders = []
    for i in range(len(phase_files)):
        phase_folders.append(phase_files[i][:-3])
    print('Extracting phase files...')
    for i in range(len(phase_files)):
        response = os.system('multify -x -f' + phase_files[i])
        if response != 0:
            exit('Failed to run multify to extract phase files! Make sure to install Panda3D SDK before running this program.')
    print('Cleaning up phase folders...')
    for i in range(len(phase_files)):
        contents = glob(phase_folders[i] + '/*')
        for i in range(len(contents)):
            if os.path.isdir(contents[i]):
                if 'audio' not in contents[i]:
                    shutil.rmtree(contents[i])
            else:
                os.remove(contents[i])
        contents = glob(phase_folders[i] + '/*')
        if not contents:
            os.rmdir(phase_folders[i])
    to_randomize = ['bgm', 'dial', 'sfx']
    for a in range(3):
        print('Randomizing ' + to_randomize[a] + '...')
        audio_files = []
        for i in range(len(phase_files)):
            contents = glob(phase_folders[i] + '/audio/*/')
            for i in range(len(contents)):
                if to_randomize[a] in contents[i]:
                    audio_files += glob(contents[i] + '*.*')
        random_indexes = random.sample(range(0, len(audio_files)), len(audio_files))
        for i in range(len(audio_files)):
            if audio_files[i] == audio_files[random_indexes[i]]:
                continue
            shutil.copy(audio_files[i], audio_files[random_indexes[i]])
    print('Creating content pack file...')
    if not os.path.exists('resources'):
        os.mkdir('resources')
    os.system(f'multify -c -f resources/TTRR.mf {" ".join(phase_folders)}')
    print('Removing phase folders...')
    for i in range(len(phase_folders)):
        shutil.rmtree(phase_folders[i])
    print('The content pack file has been created inside a folder called "resources" where you have run this program. Have fun!')


try:
    main()
except:
    traceback.print_exc()
input("Press Enter to exit.")
