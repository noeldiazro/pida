import matplotlib.pyplot as plt
from benchmark import Benchmark
from pida.clock import time
from pida.links import SPIDataLink, SPIDataLinkConfiguration

class SPIDataLinkTest(Benchmark):

    def test_loopback(self):
        request = [
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0x40, 0x00, 0x00, 0x00, 0x00, 0x95,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
            0xDE, 0xAD, 0xBE, 0xEF, 0xBA, 0xAD,
            0xF0, 0x0D,
        ]
        max_speeds = [
            100000, # 100 KHz
            200000, # 200 KHz
            500000, # 500 KHz
            1000000, # 1 MHz
            2000000, # 2 MHz
            4000000, # 4 MHz
            8000000, # 8 MHz
            16000000, # 16 MHz
            32000000, # 32 MHz
            48000000, # 48 MHz
            64000000, # 64 MHz
        ]
        for max_speed in max_speeds:
            configuration = SPIDataLinkConfiguration(0, max_speed)
            with SPIDataLink(0, 0, configuration) as link:
                response = link.transfer(request)
                print('{}: {}'.format(max_speed, response == request))

    
    def _test_average_time_between_requests(self, request, n_samples, max_speed_hz):
        configuration = SPIDataLinkConfiguration(0, max_speed_hz)
        with SPIDataLink(0, 0, configuration) as link:
            start = time()
            for _ in range(n_samples):
                link.transfer(request)
            end = time()
        return (end - start) / n_samples
    
    def test_average_time_between_requests(self):
        request = [0x00] * 3
        n_samples = 10000
        max_speeds = [
            int(100e3),
            int(200e3),
            int(500e3),
            int(1e6),
            int(2e6),
            int(4e6),
            int(8e6),
            int(16e6),
            int(32e6),
            int(48e6),]

        averages = [1 / self._test_average_time_between_requests(request, n_samples, max_speed) for max_speed in max_speeds]
        plt.plot(max_speeds, averages, 'o-')
        plt.xlabel('Frecuencia reloj SPI (Hz)')
        plt.ylabel('Peticiones promedio por segundo')
        plt.grid(True)
        plt.show()
