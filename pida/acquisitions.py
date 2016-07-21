# -*- coding: utf-8 -*-
"""Este módulo contiene las clases necesarias para
gestionar las adquisiciones de datos hechas a través
de alguna de las interfaces de adquisición de datos
disponibles.
"""
from abc import ABCMeta, abstractmethod
from threading import Thread, Lock
from clock import time, sleep

class Acquisition(Thread):
    """Clase base abstracta para controlar una adquisición de datos.

    :param channel: Canal de una interfaz de adquisición a través del
        cual se toman los datos.
    :param max_count: Número máximo de muestras a tomar en la
        adquisición. El valor por defecto (0) indica que no hay límite.

    .. method:: start()
    
        Comienza la adquisición de datos.
    """
    __metaclass__ = ABCMeta

    def __init__(self, channel=None, max_count=0):
        Thread.__init__(self)
        self._channel = None
        self._max_count = 0
        self.channel = channel
        self.max_count = max_count
        self._data = []
        self._status = 'waiting'
        self._elapsed_time = 0.0
        self._running = True
        self._start_time = 0.0
        # Lock to access start_time
        self.start_time_lock = Lock()
        """Cierre de exclusión mútua para acceder a :attr:`start_time`. El
        hilo que quiera leer :attr:`start_time` debe previamente
        adquirir el cierre."""

        self.start_time_lock.acquire()
        self.daemon = True

        self.LOCK = Lock()

    # Channel
    @property
    def channel(self):
        """Canal de entrada de una interfaz de adquisición de datos por el
        que se toman las muestras de la adquisición.
        """
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel

    @channel.deleter
    def channel(self):
        raise AttributeError("Can't delete attribute")

    # Max count
    @property
    def max_count(self):
        """Máximo número de muestras a tomar durante la adquisición.
                         
        Si se fija un valor 0 no hay límite de muestras y la adquisición
        se detiene únicamente cuando se invoca el método :meth:`stop`.

        Eleva una excepción :exc:`ValueError` si el valor que se intenta
        fijar no es 0 o un número positivo.
        """
        return self._max_count

    @max_count.setter
    def max_count(self, max_count):
        if max_count < 0:
            raise ValueError("Positive number expected")
        self._max_count = int(max_count)

    @max_count.deleter
    def max_count(self):
        raise AttributeError("Can't delete attribute")

    # Data
    def get_data(self, n_count=0):
        """Devuelve una lista con los últimos datos adquiridos.

        :param n_count: Número de muestras a incluir en la lista
            devuelta. El valor por defecto 0 incluye todos los datos
            adquiridos hasta ese momento.
        """
        return self._data[-n_count:]

    def print_data(self, n_count=0):
        """Escribe en pantalla un listado de los últimos datos adquiridos.

        :param n_count: Número de muestras a incluir en el listado.  El
            valor por defecto 0 incluye todos los datos adquiridos hasta
            ese momento.
        """
        print "Elapsed Time\tValue"
        for [elapsed_time, adc_value] in self.get_data(n_count):
            print "{:.6f}".format(elapsed_time) + "\t" + str(adc_value)

    # Status
    @property
    def status(self):
        """Estado de la adquisición.

        Puede tomar los siguientes valores:

        * ``'waiting'``, esperando el comienzo de la adquisición mediante el método :meth:`start`.
        * ``'running'``, adquiriendo muestras.
        * ``'stopped'``, la adquisición ha finalizado, porque se ha alcanzado
            el máximo número de muestras :attr:`max_count` o porque se ha invocado
            el método :meth:`stop` del objeto.

        Es una propiedad de sólo lectura.
        """
        return self._status

    # Elapsed Time
    @property
    def elapsed_time(self):
        """Tiempo de adquisición transcurrido en segundos, con una
        precisión de 1 nanosegundo.

        Sólo se actualiza el tiempo transcurrido mientras se están
        acquiriendo muestras, no mientras se está esperando a su
        comienzo o ya se ha finalizado la toma de datos. Visto de otro
        modo, sólo se actualiza mientras la adquisición está en estado
        ``'running'`` (ver :attr:`status`).

        Es una propiedad de sólo lectura.
        """
        return self._elapsed_time

    # Start Time
    @property
    def start_time(self):
        """Tiempo de referencia de comienzo de la adquisición.

        .. warning:: El hilo desde el que se quiere leer esta propiedad
            debe ser dueño del cierre de exclusión mútua :attr:`start_time_lock`.

        .. note:: En Raspberry Pi este valor es el número de segundos
            entre el encendido del computador y el comienzo de la
            adquisición. Sin embargo, en otras plataformas podría tener
            un significado totalmente diferente.

        Es una propiedad de sólo lectura.
        """
        return self._start_time

    @abstractmethod
    def run(self):
        """Define el proceso para adquirir los datos. Es usado por el método :meth:`start`.
        Este método no debe invocarse directamente.

        .. warning:: Es un método abstracto que debe ser implementado por todas las clases que hereden de ésta.
        """
        pass

    def stop(self):
        """Detiene la adquisición de datos."""
        self._running = False

class SynchronousAcquisition(Acquisition):
    """Gestiona una adquisición de datos síncrona en la que a través de un canal
    de una interfaz de adquisición de datos se toman valores con una frecuencia
    de muestreo específica.

    :param channel: Canal de una interfaz de adquisición a través del
        cual se toman los datos.
    :param max_count: Número máximo de muestras a tomar en la
        adquisición. El valor por defecto (0) indica que no hay límite.
    :param sampling_rate: Frecuencia de muestreo en hertzios. El valor
        por defecto (0) provoca que las muestras se tomen a la máxima
        tasa posible.
    """

    def __init__(self, channel=None, max_count=0, sampling_rate=0):
        Acquisition.__init__(self, channel, max_count)
        self._sampling_rate = 0.0
        self._sampling_period = 0.0
        self.sampling_rate = sampling_rate

    # Sampling rate
    @property
    def sampling_rate(self):
        """Frecuencia de muestreo de la adquisición en hertzios.
                             
        Un valor 0 de esta propiedad implica que las muestras se toman a
        la máxima tasa posible.
                            
        Eleva una excepción :exc:`ValueError` si el valor que se intenta
        fijar no es 0 o un número positivo.
        """
        return self._sampling_rate

    @sampling_rate.setter
    def sampling_rate(self, sampling_rate):
        if sampling_rate > 0:
            self._sampling_rate = 1.0 * sampling_rate
            self._sampling_period = 1.0 / sampling_rate
        elif sampling_rate == 0:
            self._sampling_rate = 0.0
            self._sampling_period = 0.0
        else:
            raise ValueError("Positive number expected")

    @sampling_rate.deleter
    def sampling_rate(self):
        raise AttributeError("Can't delete attribute")

    def run(self):
        self.channel.open()
        self._status = 'running'

        self._start_time = time()
        self.start_time_lock.release()

        request = self._start_time
        i = 0
        while self._running and (self._max_count == 0 or i < self._max_count):
            # Calculate iteration end time
            request += self._sampling_period

            # Add new data poing
            self._elapsed_time = time() - self._start_time
            value = self.channel.read()
            self._data.append([self._elapsed_time, value])

            # Sleep till iteration end time
            sleep(request)
            i = i + 1

        self._elapsed_time = time() - self._start_time
        self.channel.close()
        self._status = 'stopped'
