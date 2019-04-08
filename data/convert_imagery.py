
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
from rasterio.plot import show
from rasterio.mask import mask
from rasterio.warp import calculate_default_transform, reproject, Resampling

parser = argparse.ArgumentParser(description="Converts an image to match the projection of a seed image and rescales the pixel size")

# arguments for converter
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


args = parser.parse_args()

# check if seed image is available
if args.seed_image is not None:
    seedImage = args.seed_image
else:
    seedImage =  '/home/datafolder/seed.tif'

# get seed image crs and bounds
seedRaster = rasterio.open(seedImage)
seedCRS = seedRaster.crs
seedBounds = seedRaster.bounds

# get input image to convert crs and bounds
newRaster = rasterio.open(args.new_image)
newCRS = newRaster.crs
newBounds = newRaster.bounds

#output name with the resolution appeneded
currentFileName = newRaster.name
newFileNanme = currentFileName.replace('.tif', '_' + str(args.new_resoltion) + '.tif')

# warp the image to new seed image crs,  change pixel size, crop to seed image's bounds, and use average Resampling
gdal.Warp(  newFileNanme,
            args.new_image,
            outputBounds=[seedBounds.left, seedBounds.bottom, seedBounds.right, seedBounds.top],
            resampleAlg=gdal.GRA_Average,
            srcNodata=0,
            dstNodata=0,
            dstSRS=seedCRS.to_wkt(),
            xRes=args.new_resoltion,
            yRes=args.new_resoltion)

newRaster.close()
seedRaster.close()
