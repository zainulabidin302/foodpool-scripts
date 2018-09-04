
from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import sys
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, '../')
sys.path.insert(0, './')
import mysqlconnect
con = mysqlconnect.Connector("../env")


def predict(id, n=10):
    pass
