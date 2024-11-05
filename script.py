import geopandas as gpd
import pandas as pd
#import numpy as np
import os
#import shutil
from zipfile import ZipFile
from glob import glob
#import subprocess
import csv

# Define Data Paths
data_path = os.getenv('DATA_PATH', '/data')
inputs_path = os.path.join(data_path,'inputs')


# Define Input Paths
boundary_path = os.path.join(inputs_path,'boundary')
vector_path = os.path.join(inputs_path, 'reservoirs')
parameters_path = os.path.join(inputs_path, 'parameters')

# Define and Create Output Paths
outputs_path = os.path.join(data_path, 'outputs')
outputs_path_ = data_path + '/' + 'outputs'
if not os.path.exists(outputs_path):
    os.mkdir(outputs_path_)
reservoircoeffs_path = os.path.join(outputs_path, 'reservoirs')
reservoircoeffs_path_ = outputs_path + '/' + 'reservoirs'
if not os.path.exists(reservoircoeffs_path):
    os.mkdir(reservoircoeffs_path_)
# parameter_outputs_path = os.path.join(outputs_path, 'parameters')
# parameter_outputs_path_ = outputs_path + '/' + 'parameters'
# if not os.path.exists(parameter_outputs_path):
#     os.mkdir(parameter_outputs_path_)

# Look to see if a parameter file has been added
parameter_file = glob(parameters_path + "/*.csv", recursive = True)
print('parameter_file:', parameter_file)

# Identify the EPSG projection code
if len(parameter_file) == 1 :
    parameters = pd.read_csv(parameter_file[0])
    with open(parameter_file[0]) as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            try:
                if row[0] == 'PROJECTION':
                    projection = row[1]
            except:
                continue
else:
    projection = os.getenv('PROJECTION')

print('projection:',projection)

# Identify input polygons and shapes (boundary of city, and OS grid cell references)
boundary_1 = glob(boundary_path + "/*.*", recursive = True)
print('Boundary File:',boundary_1)

# Read in the boundary
boundary = gpd.read_file(boundary_1[0])

# Check boundary crs matches the projection
if boundary.crs != projection:
    boundary.to_crs(epsg=projection, inplace=True)

print('boundary_crs:', boundary.crs)

# Identify the name of the boundary file for the city name
file_path = os.path.splitext(boundary_1[0])
print('File_path:',file_path)
print(os.name)
#code for file names is messy and needs to be done better
if os.name=='nt':
    filename=file_path[0].split("\\")
else:
    filename=file_path[0].split("/")
print('filename:',filename)
location = filename[-1]
print('Location:',location)

# Identify if the buildings are saved in a zip file
reservoir_files_zip = glob(vector_path + "/*.zip", recursive = True)
print(reservoir_files_zip)

# If yes, unzip the file (if the user has formatted the data correctly, this should reveal a .gpkg)
if len(reservoir_files_zip) != 0:
    for i in range (0,len(reservoir_files_zip)):
        print('zip file found')
        with ZipFile(reservoir_files_zip[i],'r') as zip:
            zip.extractall(vector_path)

# Identify geopackages containing the polygons of the buildings
reservoir_files = glob(vector_path + "/*.gpkg", recursive = True)

if len(reservoir_files) != 0:
    # Create a list of all of the gpkgs to be merged
    to_merge=[]
    to_merge=['XX' for n in range(len(reservoir_files))]
    for i in range (0,len(reservoir_files)):
        file_path = os.path.splitext(reservoir_files[i])
        if os.name=='nt':
            filename=file_path[0].split("\\")
        else:
            filename=file_path[0].split("/")
        to_merge[i]=filename[-1]+'.gpkg'

    print('to_merge:',to_merge)

    # Create a geodatabase and merge the data from each gpkg together
    all_reservoir = []
    all_reservoir=gpd.GeoDataFrame(all_reservoir)
    for cell in to_merge:
        #gdf = gpd.read_file('/data/inputs/reservoir_coeffs/%s' %cell)
        gdf = gpd.read_file(vector_path +'/' + cell)
        all_reservoir = pd.concat([gdf, all_reservoir],ignore_index=True)

    all_reservoir.to_crs(epsg=projection, inplace=True)

    clipped = gpd.clip(all_reservoir,boundary)

    permeable_areas = 'polygons'

    all_reservoirs = clipped.to_file(os.path.join(outputs_path,'all_reservoircoeffs.shp'))
    all_reservoirs = gpd.read_file(os.path.join(outputs_path,'all_reservoircoeffs.shp'))
    all_reservoirs = all_reservoirs.explode()
    all_reservoirs.reset_index(inplace=True, drop=True)
    all_reservoirs1 = all_reservoirs.to_file(os.path.join(reservoircoeffs_path, location + '.gpkg'),driver='GPKG',index=False)
    
    os.remove(os.path.join(outputs_path,'all_reservoircoeffs.shp'))
    os.remove(os.path.join(outputs_path,'all_reservoircoeffs.cpg'))
    os.remove(os.path.join(outputs_path,'all_reservoircoeffs.dbf'))
    os.remove(os.path.join(outputs_path,'all_reservoircoeffs.prj'))
    os.remove(os.path.join(outputs_path,'all_reservoircoeffs.shx'))
    


