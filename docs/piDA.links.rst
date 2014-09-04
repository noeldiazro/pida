===================
Módulo :mod:`links`
===================
.. module:: piDA.links

Este módulo incluye clases para gestionar enlaces de datos.

.. inheritance-diagram:: DataLink
			 SPIDataLink

Clase :class:`DataLink`
-----------------------
.. class:: DataLink(identifier, description, max_speed)

   Clase base para la definición de enlaces de datos.

   Es una clase abstracta.

   Clase base: :class:`object`.

   :param identifier: identificador del enlace de datos.
   :type identifier: :class:`String`
   :param description: descripción del enlace de datos.
   :type description: :class:`String`
   :param max_speed: máxima velocidad en herzios del enlace de datos.
   :type max_speed: :class:`Number`

   .. method:: close()
      
      Cierra el enlace de datos. Debe invocarse este método cuando no
      vayan a realizarse más transferencias de datos a través del
      enlace.

      .. warning:: Es un método abstracto.

   .. attribute:: description
      
      Descripción del enlace de datos.

      Es una propiedad de sólo lectura.

   .. attribute:: identifier

      Identificador del enlace de datos.

      Es una propiedad de sólo lectura.

   .. attribute:: max_speed

      Velocidad máxima en herzios del enlace de datos.

      Es una propiedad de sólo lectura.

   .. method:: open()

      Abre el enlace de datos. Este método debe invocarse antes de
      realizar la primera transferencia por el enlace.

      .. warning:: Es un método abstracto.

   .. method:: transfer(data)
   
      Envía los datos que se pasan como parámetro a otro dispositivo a
      través del enlace de datos. Devuelve una lista con los datos
      recibidos del dispositivo en respuesta a los datos enviados.

      :param data: lista con los datos a enviar. Cada elemento de la
                   lista es un byte.
      :type data: :class:`List`

      .. warning:: Es un método abstracto.

Clase :class:`SPIDataLink`
--------------------------
.. class:: SPIDataLink(bus, device, max_speed)
   
   Clase que gestiona un enlace Serial Peripheral Interface (SPI).

   Clase base: :class:`DataLink`

   .. attribute:: bus

      Identificador del bus SPI que se usa para el enlace de datos.

      .. note:: Raspberry Pi ofrece a través de su puerto GPIO un
                único bus SPI cuyo identificador es 0.

      Es una propiedad de sólo lectura.

   .. attribute:: device
      
      Línea de selección de chip SPI activa en el enlace de datos.

      .. note:: El bus SPI 0 de Raspberry Pi puede, a través del
                puerto GPIO, activar dos líneas de selección de chip
                SPI: 0 y 1.

      Es una propiedad de sólo lectura.
