# Use this to clip randomm still frames from a video file
# Arguments:
#  python main.py --dataroot "./DrivingVideo.mp4"  --processType crop --extension mp4 --shotcount 24 --dimensionx 1280 --dimensiony 720 --cropx 500 --cropy 500 --randomCrop 
# 



# Importing all necessary libraries
import cv2
import os
import glob
import shutil
from pathlib import Path
import random
import zipfile
import argparse
from options import BaseOptions

from opencv.VidFrameClipper import VidFrameClipper

from FrameClipper.FrameClipper import FrameClipper

def GetRelativeOutDiretory(filepath):
    head_tail = os.path.split(filepath)
    namesplit = os.path.splitext(head_tail[1])
    outname = namesplit[0] + '_$F.png' 
    outdirectory = head_tail[0]+ '/'+namesplit[0]
    outfilepath = outdirectory + '/'+outname
    if not os.path.exists(outdirectory):
        os.makedirs(outdirectory)
    return outfilepath

def ClipRandomFrame(filepath, outpath, count, dimensions, cropdimensions):
    
    VidFrameClipper_ = VidFrameClipper(filepath, dimensions[0], dimensions[1], cropdimensions[0], cropdimensions[1], True)
    VidFrameClipper_.WriteRandomFramesToImageFiles(outpath, count)    
    # VidFrameClipper_.WriteRandomFramesToImageFiles(GetRelativeOutDiretory(filepath), count)    
    VidFrameClipper_.Close()    

def ClipFrames(filepath, outpath,count, dimensions, cropdimensions):
    
    VidFrameClipper_ = VidFrameClipper(filepath, dimensions[0], dimensions[1], cropdimensions[0], cropdimensions[1], True)
    VidFrameClipper_.WriteFramesToImageFiles(outpath, count)    
    VidFrameClipper_.Close()    

def GetFilesInFolder(directory):
    types = ('*.mp4')
    images_list = []
    for files in types:
        images_list.extend(glob.glob(os.path.join(directory, files)))
    images_list.pop()
    return images_list

def GetImageFilesInFolder(directory, ext):
    types = ('*.png')
    result = list(Path(directory).glob('**/*.'+ext))

    return  result


def ProcessDirectory(directory, outpath, screenshoutCount):
    directory = directory
    files = GetFilesInFolder(directory)
    count = 0
    dimensions =  [1000, 1000]
    cropdimensions =  [500, 500]
    for filee in files:
        print("Currently Rendering : ",count , filee)
        
        ClipRandomFrame(filee, outpath, screenshoutCount, dimensions, cropdimensions)
        count += 1
    ConsolidateImagesInDirectory(directory)

def ConsolidateImagesInDirectory(directory):
    datasetpath = directory + "/datasetimgs"
    if not os.path.exists(datasetpath):
        os.makedirs(datasetpath)
        
    files = GetImageFilesInFolder(directory, 'png')
    count = 0
    
    for file in files:
        head_tail = os.path.split(file)
        filename = datasetpath + '/' + head_tail[1]
        if not os.path.exists(filename):
            shutil.copy(file, filename)
            print("Currently Copying : ",count , filename)
        else:
            print("Skipping Existing : ",count , filename)
            
        count += 1

      
def GetRandomFile(filelist, usedlist):
    framenumber = random.randint(0, len(filelist) - 1)
    if framenumber in usedlist:
        framenumber = GetRandomFile(filelist, usedlist)
    return framenumber

def ZipListFiles(filelist, outpath):
    with zipfile.ZipFile(outpath, 'w') as zipMe:        
        for file in filelist:
            zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

def PruneDirectory(directory, outputpath, count, extension):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    files = GetImageFilesInFolder(directory, extension)
    countt = 0
    usedlist = []
    prunelist = []
    print('count', count)
    for f in range(0,count):
        framenumber = GetRandomFile(files, usedlist)
        usedlist.append(framenumber)
        file = files[framenumber]
        prunelist.append(file)
        
        head_tail = os.path.split(file)
        filename = outputpath + '/' + head_tail[1]
        if not os.path.exists(filename):
            shutil.copy(file, filename)
            print("Currently Copying : ",countt , filename)
        else:
            print("Skipping Existing : ",countt , filename)
            
        countt += 1
        
    ZipListFiles(prunelist, outputpath +".zip")
    

def ZipDirectory(directory, outputpath, count, extension):
    if not os.path.exists(outputpath):
        os.makedirs(outputpath)
    files = GetImageFilesInFolder(directory, extension)
    countt = 0
    usedlist = []
    prunelist = []
    print('count', count)
    for f in range(0,count):
        
        file = files[f]
        prunelist.append(file)
        
        head_tail = os.path.split(file)
        filename = outputpath + '/' + head_tail[1]
        if not os.path.exists(filename):
            shutil.copy(file, filename)
            print("Currently Copying : ",countt , filename)
        else:
            print("Skipping Existing : ",countt , filename)
            
        countt += 1
        
    ZipListFiles(prunelist, outputpath +".zip")
    

def ProcessFile(filepath, outpath, screenshoutCount):
    dimensions =  [1280, 720]
    cropdimensions =  [500, 500]
    ClipRandomFrame(filepath, outpath, screenshoutCount, dimensions, cropdimensions)

def PruneDataset():
    datasetdirectory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/datasetimgs"
    datasetPrunedirectory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/datasetimgs_prune"
    # PruneDirectory(datasetdirectory,datasetPrunedirectory, 500, 'png')


def ProcessStart(options):
    if options.processType == 'crop':
        if options.isDirectory == True:
            ProcessDirectory(options.dataroot, options.output, options.shotcount)
        else:
            ProcessFile(options.dataroot, options.output, options.shotcount)
        
    if options.processType == 'consolidate':
        ConsolidateImagesInDirectory(options.dataroot)
        
    if options.processType == 'prune':
        PruneDirectory(options.dataroot, options.output, options.shotcount, options.extension)
        # PruneDirectory(options.dataroot, options.dataroot+'/temp', options.shotcount, options.extension)

    if options.processType == 'zip':
        ZipDirectory(options.dataroot, options.output, options.extension)
        # ZipDirectory(options.dataroot, options.dataroot+'/temp', options.extension)
        

def main():
    # opt = BaseOptions.BaseOptions().parse()
    # ProcessStart(opt)
    FrameClipper_ = FrameClipper()
    FrameClipper_.ProcessStart()
    # Process a directory of files
    # directory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/02"
    # directory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/GTAViceCity/GTAVC-BridgeTraveling"
    # directory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/GTAViceCity/GTAVC-Heli"
    # ProcessDirectory(directory, 50)
    # print(GetImageFilesInFolder(directory, 'png'))
    
    # directory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/02/DrivingMiami/DrivingMiami/datasets"
    # filee = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/DrivingMiami/DrivingMiami/DrivingTour-MiamiBeach.mkv"
    
    # filee = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/GTAViceCity/GTA Vice City - Full Game Walkthrough in 4K.mp4"
    # filee = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/02/pexels-herve-piglowski-5649316.mp4"
    # filee2 = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/02/pexels-herve-piglowski-5681670.mp4"
    
    
    # ProcessFile(filee, 3000)
    
    # ProcessFile(filee2, 20)
    # ClipRandomFrame(filee,  5)
    # PruneDirectory(directory,directory +'/prune', 800, 'jpg')
    
    # ConsolidateImagesInDirectory(directory)
    
    # PruneDataset()
    


if __name__=="__main__":
    main()