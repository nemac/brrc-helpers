# brrc-helpers
GDAL Utility Scripts

Clone or download this repo. Then from a command line build the Docker image.
```bash
$ docker build . -t rasterio-gdal
```

## Run using Docker Compose
start docker containers
```bash
$ docker-compose  -p brrc-helper -f docker-compose.yml up -d
```

run conversion, converts road_noise.tif to Albers Conic and changes pixel size 275x275 meters
```bash
$ docker exec brrc-helper python3 /home/datafolder/convert_imagery.py /home/datafolder/road_noise.tif -r 275
```

Shutdown the containers
```bash
$ docker-compose  -p brrc-helper -f docker-compose.yml down
```

## Or run using docker
start docker containers
```bash
$ docker run -v $(pwd)/data/:/home/datafolder --name rasterio-gdalps -it --rm rasterio-gdal /bin/bash
```

What can I do with the script?
```bash
$ python3 /home/datafolder/convert_imagery.py -h
```

```bash
usage: convert_imagery.py [-h] [-s SEED_IMAGE] [-r NEW_RESOLTION] new_image

Converts an image to match the projection of a seed image and rescales the
pixel size

positional arguments:
  new_image         The new or output image

optional arguments:
  -h, --help        show this help message and exit
  -s SEED_IMAGE     The seed image default is a conus image projected to EPSG:
                    42303 - "Albers Conic"
  -r NEW_RESOLTION  new spatial ressolution or pixel size, default is 270
```


Example of converting an image, converts road_noise.tif to script defaults: Albers Conic and pixel size 250x250 meters
```bash
$ python3 /home/datafolder/convert_imagery.py /home/datafolder/road_noise.tif
```
