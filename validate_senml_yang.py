import json
import yangson

from yangson import DataModel as DM
from yangson.enumerations import ContentType

# This function is required to convert all numerical values to strings due to yangson's strict typing 
def convert_numbers_to_strings(d):
    for key, value in d.items():
        if isinstance(value, (int, float)):
            d[key] = str(float(value))
        elif isinstance(value, dict):
            convert_numbers_to_strings(value)  # Recursive call for nested dictionaries
        elif isinstance(value, list):
            for item in value:
                convert_numbers_to_strings(item)
    return d

# Create a data model from model definition in JSON format and path to YANG modules
dm = DM.from_file("./yang-library-senml.json", ["./"])

# Load the SenML data in JSON format
jsonData = json.load(open("senml_example.json"))

jsonData = convert_numbers_to_strings(jsonData)
rootInstanceNode = dm.from_raw(jsonData)

# Validate the root instance node
try:
    rootInstanceNode.validate(ctype=ContentType.all)
    print("Validation successful")
except:
    print("Validation failed")