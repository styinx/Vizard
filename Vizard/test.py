import pandas

from Analyzer.processing import AnalysisData

from Vizard.settings import REPORT, TASK_PATH
from source.util import unserialize

path = TASK_PATH + '/2c071276/result_cached.dat'
df = unserialize(path).df
headers = REPORT['Locust']['headers']

# df[4] = pandas.to_numeric(df[4])

print(df)
print(df.dtypes)