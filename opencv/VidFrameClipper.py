# Use this to clip randomm still frames from a video file
# Arguments:
#  -video string -output -width int -height int -seed int


# Importing all necessary libraries
import cv2
import os
import random
from pathlib import Path

class VidFrameClipper:

    def __init__(self, inputfile, width, height, cropx, cropy, randomcrop, framestart, frameend, outputfolder):
        self.Loaded = False
        self.width = width
        self.height = height
        self.cropx = cropx
        self.cropy = cropy
        self.randomcrop = randomcrop
        self.framestart = framestart
        self.frameend = frameend
        self.inputfile = inputfile
        self.outputfolder = outputfolder
        self.dirname = os.path.dirname(inputfile)
        self.filesplitext = os.path.splitext(os.path.basename(inputfile))
        self.outputfiletemplate = outputfolder +  '/' + self.filesplitext[0] + '$F.png'
        # self.outputfiletemplate = outputfolder + '/' + self.filesplitext[0] + '/' + self.filesplitext[0] + '$F.png'
        self.CheckOutputFolder()
        self.currentFrame = 0
        self.LoadVideo(inputfile)
    def CheckOutputFolder(self):
        if not os.path.exists(self.outputfolder):
            Path(self.outputfolder).mkdir(parents=True, exist_ok=True)
            
            
    def LoadVideo(self, filepath):
        self.filepath = filepath
        self.cap = cv2.VideoCapture(filepath)
        
        # cap = cv2.VideoCapture("M:/Projects/GAN/VG2City/01-Working/28-JJ/00-Source/01-VIDZ/CityStock/Pexels Videos 1578970.mp4")
        property_id = int(cv2.CAP_PROP_FRAME_COUNT) 
        fps_id = int(cv2.CAP_PROP_FPS) 
        self.framelength = int(cv2.VideoCapture.get(self.cap, property_id))
        self.fps = int(cv2.VideoCapture.get(self.cap, fps_id))
        self.cap.set(1,self.currentFrame);
        self.ret, self.frame = self.cap.read()
        
        self.SetWidthHeightImage()
        print( self.framelength )
        
    def SetOutput(self,filepath):
        self.outpath = filepath
        
    def ScaleImage(self, scalePercent):
            #percent by which the image is resized
        self.scalePercent = scalePercent
        #calculate the 50 percent of original dimensions
        print("shape1 ", self.frame.shape[1])
        print("shape0 ", self.frame.shape[0])
        width = int(self.frame.shape[1] * self.scalePercent / 100)
        height = int(self.frame.shape[0] * self.scalePercent / 100)
        print("width ", width)
        print("height ", height)

        # dsize
        dsize = (width, height)

        # resize image
        self.frame = cv2.resize(self.frame, dsize)
        self.CropImage()
        
        
    def SetWidthHeightImage(self):

        # dsize
        dsize = (self.width, self.height)
        try:
            self.frame = cv2.resize(self.frame, dsize)
        except :
            print("Failed Resize")
        # resize image
        self.CropImage()
    def GetRandomCrops(self):
        Ycrop = 20
        Xcrop = 100
        if self.randomcrop == True:
            Ycrop = abs(random.randint(0 ,self.height - self.cropx))
            Xcrop = abs(random.randint(0 ,self.width - self.cropy))

            if Ycrop + self.cropy > self.height:
                print("YCrop TOO LOW")
                self.GetRandomCrop()
            if Xcrop + self.cropx > self.width:
                print("XCrop TOO LOW")
                self.GetRandomCrop()
        return([Xcrop, Ycrop])
        
    def CropImage(self):
        Ycrop = 20
        Xcrop = 100
        if self.randomcrop == True:
            crops = self.GetRandomCrops()
            Ycrop = crops[1]
            Xcrop = crops[0]
            print("YCrop, XCrop ", [Ycrop, Xcrop])
            print("YCrop ", abs(Ycrop - (self.cropy)))
            print("Xcrop ", abs(Xcrop - (self.cropx)))
        try:
            self.frame= self.frame[Ycrop:Ycrop +  self.cropy, Xcrop:Xcrop +  self.cropx]
            # self.frame= self.frame[20:abs(Ycrop - (self.cropy)), 100:abs(Xcrop - (self.cropx))]
            # self.frame= self.frame[20:self.cropy+20, 100:self.cropx+100]

        except :
            print("Failed Crop")
        # print( [int((self.frame.shape[0]/2) +(self.cropy/2 )), int((self.frame.shape[0]/2) - (self.cropy/2 )), int( (self.frame.shape[1]/2) - (self.cropx/2 ) ) , int((self.frame.shape[1]/2) +(self.cropx/2 ) )])
        # updatedframe = self.frame[ int((self.frame.shape[0]/2) +(self.cropy/2 )):  int((self.frame.shape[0]/2) - (self.cropy/2 )),int( (self.frame.shape[1]/2) - (self.cropx/2 ) )  :   int((self.frame.shape[1]/2) +(self.cropx/2 ) )]
        # self.frame = updatedframe
        # return self.frame[self.cropy:self.cropy+self.height, self.cropx:self.cropx+self.width]

    # def SetFrame(self, framenumber):
    #     self.cap.set(1,framenumber);
    #     self.currentFrame = framenumber
    #     self.ret, self.frame = self.cap.read()
    #     self.SetWidthHeightImage()
        
    
    def SetRandomFrame(self):
        firstframe = self.framestart
        endframe = self.frameend
        
        if firstframe == -1:
            firstframe = 0
        if endframe == -1:
            endframe = self.framelength
        framenumber = random.randint(firstframe, endframe)
        # framenumber = random.randint(0, self.framelength)
        self.cap.set(1,framenumber);
        self.currentFrame = framenumber
        
        try:
            self.ret, self.frame = self.cap.read()
            self.SetWidthHeightImage()
        except :
            self.SetRandomFrame()
        
    def SetFrame(self, frame):
        framenumber = frame
        self.cap.set(1,framenumber);
        self.currentFrame = framenumber
        
        try:
            self.ret, self.frame = self.cap.read()
            self.SetWidthHeightImage()
        except :
            self.SetRandomFrame()
    
    def ShowFrame(self):
        
        # self.SetFrame(framenumber)
        my_video_name = "Vidd_"

        cv2.imshow(my_video_name+' frame ',self.frame)

        #Set waitKey 
        cv2.waitKey()

        # When everything done, release the capture
        cv2.destroyAllWindows()
        
    def WriteImageFile(self, filepath):
        cleanupdfilepath = filepath.replace('$F', str(self.currentFrame))
        self.SetOutput(cleanupdfilepath)
        cv2.imwrite(cleanupdfilepath, self.frame)
                
    def WriteFramesToImageFiles(self, filepath, count):
        for i in range(0,count):
            print('Writing Screenshot : ' + str(i) +'/'+str (count))
            self.SetFrame(self.framestart + i)
        # VidFrameClipper_.ShowFrame()
            cleanupdfilepath = filepath.replace('$F', str(self.currentFrame))
            self.SetOutput(cleanupdfilepath)
            try:
                cv2.imwrite(cleanupdfilepath, self.frame)
            except :
                print('(ERROR:1101) Failed to write : ' + cleanupdfilepath)
                i += -1
                        
    def WriteRandomFramesToImageFiles(self, filepath, count):
        for i in range(0,count):
            print('Writing Screenshot : ' + str(i) +'/'+str (count))
            self.SetRandomFrame()
        # VidFrameClipper_.ShowFrame()

            cleanupdfilepath = self.outputfiletemplate.replace('$PATH', filepath)
            cleanupdfilepath = cleanupdfilepath.replace('$F', str(self.currentFrame))
            # cleanupdfilepath = filepath.replace('$F', str(self.currentFrame))
            self.SetOutput(cleanupdfilepath)
            try:
                cv2.imwrite(cleanupdfilepath, self.frame)
                print('Wrote: ' + cleanupdfilepath )
                
            except :
                print('(ERROR:1102) Failed to write : ' + cleanupdfilepath)
                i += -1
        
    def Close(self):
        self.cap.release()
        
        

