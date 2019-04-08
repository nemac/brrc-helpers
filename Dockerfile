
# Rasterio
# ====================================
#

FROM geographica/gdal2:2.4.1
MAINTAINER Daveism

# Install git
RUN apt-get update -y && apt-get install -y \
    git \
    python-pip \
    python3-pip

RUN pip3 install rasterio
RUN pip3 install matplotlib
RUN pip3 install geopandas
RUN pip3 install pycrs
