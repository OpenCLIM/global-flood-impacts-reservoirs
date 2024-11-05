# Reservoirs
This model takes reservoir polygons supplied by the user, clips the data to the domain and ensures the data is in the correct projection.

## Description
The CityCAT model can use reservoir polygons to determine an initial reservoir depth in specific locations. This is assumed to fail and the released water flows through the domain. This model accepts reservoir data in .gpkg format, clips the data to the selected area, and ensures all data is in the same projection. If the file sizes are too large, multiple .gpkgs can be added directly, or zipped.

The water level in the reservoir is called "Value" in the gpkg file

## Input Parameters


## Input Files (data slots)
* Boundary
  * Description: A .gpkg of the geographical area of interest. 
  * Location: /data/inputs/boundary
* Parameters
  * Description: location and projection
  * Location: /data/inputs/parameters
* Reservoirs
  * Description: A .gpkg with the water level in the reservoir set as "Value"
  * Location: /data/inputs/reervoirs
 

## Outputs
* The model should output only one file - a .gpkg file of the chosen area containing the reservoir water level.
  * Location: /data/outputs/reservoirs
