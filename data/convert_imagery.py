
#! /usr/bin/python
#-------------------------------------------------------------------------------
# Name:         convert_imagery.py
# Purpose:      Take a new “layer” and do three things.
#               Reproject the new layer to match a seed image - EPSG: 42303 - “Albers Conic”,
#               Clip a new layer to so the extent matches the seed image
#               Change the new layer’s resolution or pixel size. for new layer’s extent to matche
#               the seed images exttent
#
# Author:      dave michelson
#              dmichels@unca.edu
# '''This code was developed in the public domain.  This code is provided as is, without warranty of any kind,
#  express or implied, including but not limited to the warranties of
#  merchantability, fitness for a particular purpose and noninfringement.
#  In no event shall the authors be liable for any claim, damages or
#  other liability, whether in an action of contract, tort or otherwise,
#  arising from, out of or in connection with the software or the use or
#  other dealings in the software.'''
# #-----------------------------------------------------------------------------
import os, sys
import argparse
from osgeo import gdal
import rasterio
import geopandas as gpd
from shapely.geometry import box

# from rasterio.plot import show
# from rasterio.mask import mask
# from rasterio.warp import calculate_default_transform, reproject, Resampling

parser = argparse.ArgumentParser(description="test")

parser.add_argument('new_image',
                    help='The new or output image')

parser.add_argument('-s',
                    action='store',
                    dest='seed_image',
                    help='The seed image default is a conus image projected to EPSG: 42303 - \"Albers Conic\" ',
                    default=None,
                    required = False)

parser.add_argument('-r',
                    action='store',
                    dest='new_resoltion',
                    help='new spatial ressolution or pixel size, default is 270',
                    default=270,
                    required = False)


# print(parser.parse_args())
# [new_image, seed_image, new_resoltion ] = parser.parse_args()
args = parser.parse_args()


# print(args.new_resoltion, args.seed_image)

if args.seed_image is not None:
    print('seed_image is not none:', args.seed_image)
else:
    print('seed_image is  none:', args.seed_image)
    seedImage =  '/home/datafolder/seed.tif'

print(args.new_image)

seedRaster = rasterio.open(seedImage)
seedCRS = seedRaster.crs
seedBounds = seedRaster.bounds

print(seedCRS.to_wkt())

newRaster = rasterio.open(args.new_image)
newCRS = newRaster.crs
newBounds = newRaster.bounds

bbox = box(seedBounds.left, seedBounds.bottom, seedBounds.right, seedBounds.top)

yrdy = gpd.GeoDataFrame({'geometry': bbox}, index=[0])
# yrdy.crs  = seedRaster.crs

# geob = gpd.GeoDataFrame.from_features(yrdy.to_json()['features'])


# yrdy.crs = seedCRS
# geo = yrdy.to_crs(crs=seedCRS)
yrdy.to_file("/home/datafolder/cutline.geojson", driver='GeoJSON')

# print(yrdy)


# gdal.Warp('/home/datafolder/seedout.tif', args.new_image, cutlineDSName="/home/datafolder/cutline.geojson", resampleAlg=gdal.GRA_Average, dstSRS=seedRaster.crs,  xRes=args.new_resoltion,  yRes=args.new_resoltion)
# gdal.Warp('/home/datafolder/seedout.tif', args.new_image, cropToCutline=True, cutlineDSName="/home/datafolder/cutline.geojson", resampleAlg=gdal.GRA_Average, srcNodata=0, dstNodata=0, dstSRS=seedCRS.to_wkt(),  xRes=args.new_resoltion,  yRes=args.new_resoltion)
gdal.Warp('/home/datafolder/seedout.tif', args.new_image,
            outputBounds=[seedBounds.left, seedBounds.bottom, seedBounds.right, seedBounds.top], 
            resampleAlg=gdal.GRA_Average,
            srcNodata=0,
            dstNodata=0,
            dstSRS=seedCRS.to_wkt(),
            xRes=args.new_resoltion,
            yRes=args.new_resoltion)

# gdalwarp -tr 270 270  -cutline $data_location/clipper.shp -crop_to_cutline -r average -srcnodata 0 -dstnodata 0 -overwrite $data_location/road_noise.tif $data_location/road_noise_270_gdal.tif  -t_srs $data_location/wkt.txt
