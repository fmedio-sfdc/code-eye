import ast
from io import StringIO
import json
import pandas as pd
import numpy as np
import subprocess
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics

import re
import p4cache

#may need this later to resolve data types
def tryeval(val):
    try:
        val = ast.literal_eval(val)
    except ValueError:
        pass
    return val

def get_features(filename):
    stream=p4cache.p4print(filename)

    #output='{"targetFilename":"'+targetFilename+'","fieldCount":16,"varsPerMethodCount":0,"variableCount":17,"methodCount":28}'
    jarpath='/Users/stager/Documents/Documents/dev/java-source-analyzer/target/java-source-analyzer-1.0-SNAPSHOT.jar'
    jarpath='/Users/stager/Documents/Documents/dev/code-stat/target/java-source-analyzer-1.0-SNAPSHOT.jar'
    #jarpath='/Users/lauren.valdivia/ML_Patches/code-stat/target/java-source-analyzer-1.0-SNAPSHOT.jar'
    cmd=['java','-jar',jarpath]

    p = subprocess.run(cmd, stdout=subprocess.PIPE, input=stream, stderr=subprocess.DEVNULL, check=True)
    output=p.stdout.decode()
    feats=pd.DataFrame(json.loads(output),index=[0])
    return feats

def make_dataset(file_list):
    df=pd.DataFrame()
    for clFileVersion in file_list:
        # skip non-java files
        if (".java" in clFileVersion):
            if (p4cache.is_patch_path(clFileVersion)):
                analyzedFileVersion = p4cache.decrement_patch_versions(clFileVersion)
            else:
                analyzedFileVersion = clFileVersion

            feats=get_features(analyzedFileVersion)
            feats['filename']= analyzedFileVersion
            feats['label']=int(p4cache.is_patch_path(clFileVersion))
            df=df.append(feats,ignore_index=True)
    return df
