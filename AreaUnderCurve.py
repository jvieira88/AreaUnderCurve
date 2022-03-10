from saleae.range_measurements import AnalogMeasurer
import numpy as np
from numpy import trapz

class AreaUnderCurve(AnalogMeasurer):
    supported_measurements = ["area"]

    """
    Class initialisation
    """
    def __init__(self, requested_measurements):
        super().__init__(requested_measurements)
        self.m_arrSamples = []
        self.m_fSamplingPeriod = None
        self.m_fArea = 0

    """
    Does not process data. Simply attaches
    samples to be processed later. Calculated sampling period 
    based on first samples.
    """
    def process_data(self, data):
        self.m_arrSamples.append(data.samples)
        if (self.m_fSamplingPeriod is None):
            self.m_fSamplingPeriod = float((data.end_time - data.start_time) / data.sample_count)

    """
    Calculates area under curve. This is done by integrating using
    a composite trapezoidal rule.
    """  
    def measure(self):
        values = {}

        data = np.concatenate(self.m_arrSamples)
        self.m_fArea =  trapz(data, dx=self.m_fSamplingPeriod) 
        values["area"] = self.m_fArea

        return values