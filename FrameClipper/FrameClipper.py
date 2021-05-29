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

class FrameClipper:

    def __init__(self):
        self.opt = BaseOptions.BaseOptions().parse()
        print("Frame Clipper Loaded")

    def GetRelativeOutDiretory(self, filepath):
        head_tail = os.path.split(filepath)
        namesplit = os.path.splitext(head_tail[1])
        outname = namesplit[0] + '_$F.png' 
        outdirectory = head_tail[0]+ '/'+namesplit[0]
        outfilepath = outdirectory + '/'+outname
        if not os.path.exists(outdirectory):
            os.makedirs(outdirectory)
        return outfilepath

    def ClipRandomFrame(self, filepath):
        
        VidFrameClipper_ = VidFrameClipper(filepath,self.opt.dimensionx, self.opt.dimensiony, self.opt.cropx, self.opt.cropy, self.opt.randomCrop,self.opt.frameStart, self.opt.frameEnd, self.opt.output)
        VidFrameClipper_.WriteRandomFramesToImageFiles(self.opt.dataroot, self.opt.shotcount)    
        # VidFrameClipper_.WriteRandomFramesToImageFiles(GetRelativeOutDiretory(filepath), self.opt.shotcount)    
        VidFrameClipper_.Close()    

    def ClipFrames(self, filepath):
        
        VidFrameClipper_ = VidFrameClipper(filepath,self.opt.dimensionx, self.opt.dimensiony, self.opt.cropx, self.opt.cropy, self.opt.randomCrop,self.opt.frameStart, self.opt.frameEnd, self.opt.output)
        VidFrameClipper_.WriteFramesToImageFiles(self.opt.dataroot, self.opt.shotcount)    
        VidFrameClipper_.Close()    

    def GetFilesInFolder(self):
        types = ('*.mp4')
        images_list = []
        for files in types:
            images_list.extend(glob.glob(os.path.join(self.opt.dataroot, files)))
        images_list.pop()
        return images_list

    def GetImageFilesInFolder(self):
        result = list(Path(self.opt.dataroot).glob('**/*.' + self.opt.extension))

        return  result


    def ProcessDirectory(self):
        
        directory = self.opt.dataroot
        files = self.GetFilesInFolder(directory)
        count = 0
        for filee in files:
            print("Currently Rendering : ",count , filee)
            if self.opt.randomClip == True:
                self.ClipRandomFrame(filee)
            else:
                self.ClipFrames(filee)
            count += 1
        self.ConsolidateImagesInDirectory(directory)

    def ConsolidateImagesInDirectory(self):
        datasetpath = self.opt.dataroot + "/datasetimgs"
        if not os.path.exists(datasetpath):
            os.makedirs(datasetpath)
            
        files = self.GetImageFilesInFolder(self.opt.dataroot, 'png')
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

        
    def GetRandomFile(self, filelist, usedlist):
        framenumber = random.randint(0, len(filelist) - 1)
        if framenumber in usedlist:
            framenumber = self.GetRandomFile(filelist, usedlist)
        return framenumber

    def ZipListFiles(self, filelist, outpath):
        with zipfile.ZipFile(outpath, 'w') as zipMe:        
            for file in filelist:
                zipMe.write(file, compress_type=zipfile.ZIP_DEFLATED)

    def PruneDirectory(self):
        if not os.path.exists(self.opt.output):
            os.makedirs(self.opt.output)
        files = self.GetImageFilesInFolder(self.opt.dataroot, self.opt.extension)
        countt = 0
        usedlist = []
        prunelist = []
        print('count', self.opt.shotcount)
        for f in range(0,self.opt.shotcount):
            framenumber = self.GetRandomFile(files, usedlist)
            usedlist.append(framenumber)
            file = files[framenumber]
            prunelist.append(file)
            
            head_tail = os.path.split(file)
            filename = self.opt.output + '/' + head_tail[1]
            if not os.path.exists(filename):
                shutil.copy(file, filename)
                print("Currently Copying : ",countt , filename)
            else:
                print("Skipping Existing : ",countt , filename)
                
            countt += 1
            
        self.ZipListFiles(prunelist, self.opt.output +".zip")
        

    def ZipDirectory(self):
        if not os.path.exists(self.opt.output):
            os.makedirs(self.opt.output)
        files = self.GetImageFilesInFolder(self.opt.dataroot, self.opt.extension)
        countt = 0
        usedlist = []
        prunelist = []
        print('count', self.opt.shotcount)
        for f in range(0,self.opt.shotcount):
            
            file = files[f]
            prunelist.append(file)
            
            head_tail = os.path.split(file)
            filename = self.opt.output + '/' + head_tail[1]
            if not os.path.exists(filename):
                shutil.copy(file, filename)
                print("Currently Copying : ",countt , filename)
            else:
                print("Skipping Existing : ",countt , filename)
                
            countt += 1
            
        self.ZipListFiles(prunelist, self.opt.output +".zip")
        

    def ProcessFile(self, filepath):
        if self.opt.randomClip == True:
            self.ClipRandomFrame(filepath)
        else:
            self.ClipFrames(filepath)

    def PruneDataset(self):
        datasetdirectory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/datasetimgs"
        datasetPrunedirectory = "M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/datasetimgs_prune"
        # PruneDirectory(datasetdirectory,datasetPrunedirectory, 500, 'png')


    def ProcessStart(self):
        if self.opt.processType == 'crop':
            if self.opt.isDirectory == True:
                self.ProcessDirectory()
            else:
                self.ProcessFile(self.opt.dataroot)
            
        if self.opt.processType == 'consolidate':
            self.ConsolidateImagesInDirectory()
            
        if self.opt.processType == 'prune':
            self.PruneDirectory()
            # PruneDirectory(self.opt.dataroot,self.opt.dataroot+'/temp',self.opt.shotcount,self.opt.extension)

        if self.opt.processType == 'zip':
            self.ZipDirectory()
            # ZipDirectory(self.opt.dataroot,self.opt.dataroot+'/temp',self.opt.extension)
            

def main():
    opt = BaseOptions.BaseOptions().parse()
    # ProcessStart(opt)
    
        
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