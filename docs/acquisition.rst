.. currentmodule:: piDA

Clase :class:`Acquisition`
--------------------------

.. class:: Acquisition(sampling_rate=0, channel=None, max_count=0)

   Crea un objeto para gestionar una adquisición de datos.

   Clase base: :class:`threading:Thread`.

   :param sampling_rate: Frecuencia de muestreo en hertzios. El valor
       por defecto (0) provoca que las muestras se tomen a la máxima
       tasa posible.
   :type sampling_rate: :class:`Number`
   :param channel: Canal de una interfaz de adquisición a través del
       cual se toman los datos.
   :type channel: :class:`Channel`
   :param max_count: Número máximo de muestras a tomar en la
       adquisición. El valor por defecto (0) indica que no hay límite.
   :type max_count: :class:`Number`

   .. attribute:: channel

      Canal de entrada de una interfaz de adquisición de datos por el
      que se toman las muestras de la adquisición.
                       
      Eleva una excepción :exc:`TypeError` si el valor que se intenta
      fijar no es un objeto de la clase :class:`Channel`.

   .. attribute:: data

      Lista de datos adquiridos. Cada miembro de la lista es, a su
      vez, una lista de dos elementos: el primero es el tiempo de
      adquisición y el segundo el valor medido.

   .. attribute:: elapsed_time

      Tiempo de adquisición transcurrido en segundos, con una
      precisión de 1 nanosegundo.

      Sólo se actualiza el tiempo transcurrido mientras se están
      acquiriendo muestras, no mientras se está esperando a su
      comienzo o ya se ha finalizado la toma de datos. Visto de otro
      modo, sólo se actualiza mientras la adquisición está en estado
      ``'running'`` (ver :attr:`status`).

      Es una propiedad de sólo lectura.

   .. method:: get_channel()

      Devuelve el canal de entrada usado en la adquisición.

      .. deprecated:: 1.0
	 Use :attr:`channel` en su lugar.

   .. method:: get_data(n_count=0)

      Devuelve una lista con los últimos datos adquiridos.

      :param n_count: Número de muestras a incluir en la lista
         devuelta. El valor por defecto 0 incluye todos los datos
         adquiridos hasta ese momento.
      :type n_count: :class:`Number`

   .. method:: get_elapsed_time()

      Devuelve el tiempo de adquisición transcurrido en segundos, con
      una precisión de 1 nanosegundo.

      Sólo se actualiza el tiempo transcurrido mientras se están
      acquiriendo muestras, no mientras se está esperando a su
      comienzo o ya se ha finalizado la toma de datos. Visto de otro
      modo, sólo se actualiza mientras la adquisición está en estado
      ``'running'`` (ver :attr:`status`).

      .. deprecated:: 1.0
        Use :attr:`elapsed_time` en su lugar.

   .. method:: get_max_count()

      Devuelve el máximo número de muestras a tomar durante la
      adquisición.

      .. deprecated:: 1.0
	 Use :attr:`max_count` en su lugar.

   .. method:: get_sampling_rate()

      Devuelve la frecuencia de muestreo en hertzios que se ha
      fijado para la adquisición.

      .. deprecated:: 1.0
	 Use :attr:`sampling_rate` en su lugar.

   .. method:: get_status()

      Devuelve el estado de la adquisición.

      Puede tomar los siguientes valores:

      * ``'waiting'``, esperando el comienzo de la adquisición
        mediante el método :meth:`start`.
      * ``'running'``, adquiriendo muestras.
      * ``'stopped'``, la adquisición ha finalizado, porque se ha
        alcanzado el máximo número de muestras :attr:`max_count` o
        porque se ha invocado el método :meth:`stop` del objeto.

      .. deprecated:: 1.0
	 Use :attr:`status` en su lugar.      

   .. attribute:: max_count

      Máximo número de muestras a tomar durante la adquisición.
                         
      Si se fija un valor 0 no hay límite de muestras y la adquisición
      se detiene únicamente cuando se invoca el método :meth:`stop`.
                         
      Eleva una excepción :exc:`TypeError` si el valor no es 0 o un
      número positivo.

   .. method:: print_data(n_count=0)

      Escribe en pantalla un listado de los últimos datos adquiridos.

      :param n_count: Número de muestras a incluir en el listado.  El
         valor por defecto 0 incluye todos los datos adquiridos hasta
         ese momento.
      :type n_count: :class:`Number`

   .. attribute:: sampling_rate

      Frecuencia de muestreo de la adquisición en hertzios.
                             
      Un valor 0 de esta propiedad implica que las muestras se toman a
      la máxima tasa posible.
                            
      Eleva una excepción :exc:`TypeError` si el valor que se intenta
      fijar no es 0 o un número positivo.

   .. method:: set_channel(channel)

      Fija el canal de entrada a usar en la adquisición.

      :param channel: Canal de entrada.
      :type channel: :class:`Channel`

      Eleva una excepción :exc:`TypeError` si el valor que se intenta
      fijar no es un objeto :class:`Channel`.

      .. deprecated:: 1.0
	 Use :attr:`channel` en su lugar.

   .. method:: set_max_count(max_count)

      Fija el máximo número de muestras a tomar durante la
      adquisición.

      :param max_count: Máximo número de muestras. Se se fija un valor
	 0 no hay límite en el número de muestras y la adquisición se
	 detiene únicamente cuando se invoca el método :meth:`stop`.
      :type max_count: :class:`Number`

      Eleva una excepción :exc:`TypeError` si el valor no es 0 o un
      número positivo.

      .. deprecated:: 1.0
	 Use :attr:`max_count` en su lugar.

   .. method:: set_sampling_rate(sampling_rate)

      Fija la frecuencia de muestreo de la adquisición en hertzios.

      :param sampling_rate: Valor que se quiere dar a la frecuencia de
	 muestreo. Si se fija un valor 0 para la frecuencia de
	 muestreo, no se fuerza ningún tiempo de espera entre muestras
	 consecutivas, con lo que las muestras se toman a la mayor
	 tasa posible.
      :type sampling_rate: :class:`Number`

      Eleva una excepción :exc:`TypeError` si el valor no es 0 o un
      número positivo.

      .. deprecated:: 1.0
	 Use :attr:`sampling_rate` en su lugar.

   .. method:: start()

      Comienza la adquisición de datos.

   .. attribute:: start_time

      Tiempo de referencia de comienzo de la adquisición.

      .. warning:: El hilo desde el que se quiere leer esta propiedad
	 debe ser dueño del cierre de exclusión mútua :attr:`start_time_lock`.

      .. note:: En Raspberry Pi este valor es el número de segundos
	 entre el encendido del computador y el comienzo de la
	 adquisición. Sin embargo, en otras plataformas podría tener
	 un significado totalmente diferente.

      Es una propiedad de sólo lectura.

   .. attribute:: start_time_lock

      Cierre de exclusión mútua para acceder a :attr:`start_time`. El
      hilo que quiera leer :attr:`start_time` debe previamente
      adquirir el cierre.

   .. attribute:: status

      Estado de la adquisición.

      Puede tomar los siguientes valores:

      * ``'waiting'``, esperando el comienzo de la adquisición
        mediante el método :meth:`start`.
      * ``'running'``, adquiriendo muestras.
      * ``'stopped'``, la adquisición ha finalizado, porque se ha
        alcanzado el máximo número de muestras :attr:`max_count` o
        porque se ha invocado el método :meth:`stop` del objeto.

      Es una propiedad de sólo lectura.

   .. method:: stop()

      Detiene la adquisición de datos. 
   
