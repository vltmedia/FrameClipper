
import random

def GetRandomCrop(height, width, cropx, cropy):
    Ycrop = abs(random.randint(0 ,height - cropx))
    Xcrop = abs(random.randint(0 ,width - cropy))

    if Ycrop + cropy > height:
        print("YCrop TOO LOW")
        GetRandomCrop(height, width, cropx, cropy)
    if Xcrop + cropx > width:
        print("XCrop TOO LOW")
        GetRandomCrop(height, width, cropx, cropy)
    return([Xcrop, Ycrop])
    
def main():
    height = 1920
    width = 1080
    cropx = 500
    cropy = 500
    for i in range(0, 20):
        crops = GetRandomCrop(height, width, cropx, cropy)
        print ("crops ",crops)

if __name__ == '__main__':
    main()