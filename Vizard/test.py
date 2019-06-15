from Analyzer.processing import AnalysisData
import numpy as np

headers = {i: x for i, x in enumerate(['eins', 'zwei', 'drei'])}
d = {
    '1246456': [0, 2, 9, "false"],
    '1246457': [1, 2, 5, "false"],
    '1246458': [3, 2, 3, "false"],
    '1246459': [2, 2, 2, "true"],
    '1246460': [6, 5, 8, "false"],
    '1246461': [2, 2, 3, "false"],
    '1246462': [4, 7, 3, "false"],
}

df = AnalysisData(d, headers).df

print(df)

print([[x[0], x[1]] for x in df['eins'].items()])