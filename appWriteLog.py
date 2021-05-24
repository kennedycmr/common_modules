### Logging Setup 
import os, logging, google.cloud.logging
from google.cloud.logging_v2.resource import Resource

# These are the OS ENV variables we are expecting
osVariables = ['functionName', 'gcpRegion', 'gcpProjectId']
osEnv = {} 
osVals = []

# Get all our environment variables and add to our dictionary
for var in osVariables :
  osEnv[var] = os.environ.get(var, False)
  osVals.append(osEnv[var])

### Load OS Environment variables
functionName = osEnv['functionName']
gcpRegion    = osEnv['gcpRegion']
gcpProjectId = osEnv['gcpProjectId']

### Setup Logging
log_client = google.cloud.logging.Client(project=gcpProjectId)
log_name   = 'cloudfunctions.googleapis.com%2Fcloud-functions' 
logger     = log_client.logger(log_name.format(gcpProjectId))


def appWriteLog(transactionId, severity, text):
    logLabels = {"message": text, "function_name": functionName, "region": gcpRegion, "transactionId": transactionId}    
    res = Resource(type="cloud_function", labels=logLabels)
    try:
        logger.log_struct(
            {"transactionId":transactionId, "message": str(text)}, 
            resource=res, 
            severity=severity
        )
        return True
    except:
        return False

def appWriteInfo(transactionId, text) :  # backward compatibility
    result = appWriteLog(transactionId, 'INFO', str(text))
    return result

def appWriteWarning(transactionId, text) : # backward compatibility
    result = appWriteLog(transactionId, 'WARNING', str(text))
    return result

def appWriteError(transactionId, text) : # backward compatibility    
    result = appWriteLog(transactionId, 'ERROR', str(text))
    return result
