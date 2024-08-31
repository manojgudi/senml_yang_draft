import json
import pycoreconf
 
 
# Create the model object
#ccm = pycoreconf.CORECONFModel("/home/alonso/projects/lpwan_examples/senml_yang_draft/examples/ietf-lora@2016-06-01.sid", "/home/alonso/projects/lpwan_examples/senml_yang_draft/examples/senml@unknown.sid")

ccm = pycoreconf.CORECONFModel("./senml@unknown.sid")
# Read JSON configuration file
config_file = "/home/alonso/projects/lpwan_examples/senml_yang_draft/senml_example.json"

with open(config_file, "r") as f:
    json_data = f.read()
    # Small hack to rename module name from "senml:e" to "e" as CORECONF does not support module names
    json_data = json_data.replace("senml:e", "e")

print("Input JSON config data =\n", json_data, sep='')

# Convert configuration to CORECONF/CBOR
cbor_data = ccm.toCORECONF(json_data) # can also take json_data
print("Encoded CBOR data (CORECONF payload) =", cbor_data.hex())
