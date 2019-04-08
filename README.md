# brrc-helpers
GDAL Utility Scripts


Build the Docker image
```
docker build . -t rasterio-gdal
```


Run Docker
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



Example of converting an image
```bash
$ python3 /home/datafolder/convert_imagery.py /home/datafolder/road_noise.tif
```
