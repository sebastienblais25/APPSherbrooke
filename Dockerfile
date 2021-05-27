# Docker container that installs Python 3.6, GDAL and necessary shippable dependencies for CI
FROM python:3.7-stretch

# Update base container install
RUN apt-get update
RUN apt-get upgrade -y

# Add unstable repo to allow us to access latest GDAL builds
RUN echo deb http://ftp.uk.debian.org/debian stable main contrib non-free >> /etc/apt/sources.list
RUN apt-get update

## Install GDAL dependencies
RUN apt-get install -y libgdal-dev g++
#
## Update C env vars so compiler can find gdal
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
#
## This will install latest version of GDAL
RUN pip install GDAL==2.4.2
## This will install rtree
RUN pip install rtree
## This will install numpy
RUN pip install numpy

RUN mkdir /source
RUN mkdir /data

COPY source/source.csv /source
COPY source/source2.csv /source

ADD /APP_data /data
ADD main.py .
ADD Geoprocessing.py .
ADD AnalyseMultiCritere.py .
ADD Layer.py .
ADD read_csv.py .


# During debugging, this entry point will be overridden. For more information
CMD ["python", "./main.py"]
