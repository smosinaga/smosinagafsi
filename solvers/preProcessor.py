from fsi import models
import importlib, json, pathlib
from operator import attrgetter

def read(caseName):
    # Open the input file
    casePath = pathlib.Path(__file__).parent.absolute()/".."/"cases"
    caseName += ".json"

    with open(casePath/caseName, 'r') as f:
        caseDict = json.load(f) # Load the input file
        caseDict["caseName"] = caseName[:-5] #Saving the original file name
    
    attr = caseDict["geometry"] + "_" + caseDict["boundaries"]
    modelImported = getattr(models,attr)(caseDict)
    
    return modelImported
