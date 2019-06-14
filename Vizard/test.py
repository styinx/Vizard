from Analyzer.processing import AnalysisData
import numpy as np

headers = {i: x for i, x in enumerate(['eins', 'zwei', 'drei'])}
d = {
    '1246456': [0, 2, 9],
    '1246457': [1, 2, 5],
    '1246458': [3, 2, 3],
    '1246459': [2, 2, 2],
    '1246460': [6, 5, 8],
    '1246461': [2, 2, 3],
    '1246462': [4, 7, 3],
}

print(AnalysisData(d, headers).df.eins.rank())