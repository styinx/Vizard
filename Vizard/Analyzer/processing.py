import pandas as pd


class AnalysisData:
    def __init__(self, data, headers, csv=True):
        if csv:
            self.df = pd.read_csv(data).set_index(headers[0])
        else:
            self.df = pd.DataFrame(data).T.rename(columns=headers)

        self.df = self.df.sort_index()
        self.df = self.df.loc[~self.df.index.duplicated(keep='first')]
