import pandas as pd
import numpy as np

from source.util import write, read


class AnalysisData:
    def __init__(self, data, headers):
        self.df = pd.DataFrame(data).T.rename(columns=headers)

    def store(self, filename):
        read(filename)
