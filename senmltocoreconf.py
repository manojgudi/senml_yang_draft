import pycoreconf

sid_file = "./senml@unknown.sid"
config_file = "./senml_example.json"
ccm = pycoreconf.CORECONFModel(sid_file, model_description_file=None)

coreconfByteString = (ccm.toCORECONF(config_file))
# Print hex string of the byte string

print(coreconfByteString.hex(), "\nLength:", len(coreconfByteString))
