# python testoptions.py --dataroot "./DrivingVideo.mp4"  --processType crop  --isDirectory --shotcount 24 --dimensionx 1280 --dimensiony 720 --cropx 500 --cropy 500 --randomCrop 

from options import BaseOptions


def main():
    opt = BaseOptions.BaseOptions().parse()  # get test options

    print(opt)
    
if __name__ == '__main__':
    main()