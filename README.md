# Frame Clipper

Clip frames from videos for use in compositing, editing,  datasets and other needs.

# Requirements

- OpenCV2+
- Python 3.5+

# Usage
## Template

```bash
python FrameClipper_app.py --dataroot "C:/dataset/DrivingTour-MiamiBeach.mkv" --output "C:/dataset/DrivingTour-MiamiBeach"  --processType crop --extension mp4 --shotcount 24 --frameStart 100 --frameEnd 300  --randomClip --dimensionx 1280 --dimensiony 720 --cropx 500 --cropy 500 --randomCrop 
```

# Arguments

| Option        | Type       | Description                                                  | Example                                 | Required |
| ------------- | ---------- | ------------------------------------------------------------ | --------------------------------------- | -------- |
| --dataroot    | str        | path to video or directory of videos to process              | "C:/dataset/DrivingTour-MiamiBeach.mkv" | True     |
| --output      | str        | path to output directory                                     | "C:/dataset/DrivingTour-MiamiBeach"     | True     |
| --isDirectory | store_true | if dataroot is a directory or not                            | --isDirectory                           | False    |
| --shotcount   | int        | \# images to export                                          | 50                                      | False    |
| --dimensionx  | int        | x dimension to scale the input video to before cropping      | 1280                                    | False    |
| --dimensiony  | int        | y dimension to scale the input video to before cropping      | 720                                     | False    |
| --cropx       | int        | crop x dimension for final output'                           | 500                                     | False    |
| --cropy       | int        | crop y dimension for final output'                           | 50                                      | False    |
| --randomCrop  | store_true | if the clipper should randomly crop instead of being in the middle | --randomCrop                            | False    |
| --randomClip  | store_true | get random frames instead of a straight frame sequence       | --randomClip                            | False    |
| --frameStart  | int        | First frame of the video to use                              | 100                                     | False    |
| --frameEnd    | int        | last frame of the video to use                               | 5000                                    | False    |
| --extension   | str        | extension of files to process                                | png                                     | False    |
| --processType | str        | Process type to use: (crop, consolidate, zip)                | crop                                    | False    |
