def s(val, text):
    res = str(val) + " " + text
    if abs(val) == 1:
        return res
    return res + "s"


class Report:
    def __init__(self, tool):
        self.tool = tool
