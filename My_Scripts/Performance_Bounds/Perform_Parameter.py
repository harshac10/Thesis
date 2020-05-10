""" List of performance parameters """
from enum import Enum


class PerformEnum(Enum):

    Delay = "Delay"
    Backlog = "Backlog"
    Backlog_Prob = "Backlog_Prob"
    Delay_Prob = "Delay_Prob"
    Output = "Output"


class PerformParam(object):

    def __init__(self, perform_metric: PerformEnum, value):
        self.perform_metric = perform_metric
        self.value = value
