import numpy


class MemoryModel:    
    def calc_p(self, input_data: dict, memory_data: dict, distance: float) -> float:
        r = distance
        t = input_data['time'] - memory_data['time']
        g = memory_data['grad']
        p = (1 - numpy.exp((-r) * numpy.exp(-t / g))) / (1 - numpy.exp(-1))
        return p

    def calc_g(self, data: dict, count) -> float:
        g = data['grad']
        t = count - data['time']
        g = g + (1 - numpy.exp(-t)) / (1 + numpy.exp(-t))
        return g