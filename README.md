# CameraCalibration

## Commands

Build docker image
```
docker build -t camera_calibration .
```
\
Launching a container
```
docker run -it --rm --init --user=$(id -u):$(id -g) --name=$(basename $PWD) -e TZ=Asia/Tokyo --volume=$PWD:/workspace 8-point_algorithm bash
```
\
Running main program
```
python src/main.py data=???
```
or
```
python src/main.py data=???,...??? -m
```
The "data" can be one of the file names in conf/data.
\
```
python src/main.py data=small_depth-same_plane-8,small_depth-same_plane-16,small_depth-same_plane-21,small_depth-same_plane-31 -m
```
