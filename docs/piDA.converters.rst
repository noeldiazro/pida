=============================
Módulo :mod:`piDA.converters`
=============================
.. module:: piDA.converters

Este módulo incluye clases para gestionar convertidores de datos
analógico/digitales y digital/analógicos.

Clase :class:`Converter`
------------------------
.. class:: Converter(identifier, description, vref, bits, channels, data_link)

   Clase base para la definición de convertidores de datos.

   Es una clase abstracta.

   Clase base: :class:`object`.

   :param identifier: identificador del conversor.
   :type identifier: :class:`String`
   :param description: descripción del conversor.
   :type description: :class:`String`
   :param vref: tensión de referencia del conversor.
   :type vref: :class:`Number`
   :param bits: resolución en bits del conversor.
   :type bits: :class:`Integer`
   :param channels: número de canales del conversor.
   :type channels: :class:`Integer`
   :param data_link: enlace de datos para la comunicación con el conversor.
   :type data_link: :class:`piDA.links.DataLink`

   .. attribute:: bits

      Resolución en número de bits del conversor de datos.

      Es una propiedad de sólo lectura.

   .. attribute:: channels

      Número de canales del conversor de datos.

      Es una propiedad de sólo lectura.

   .. method:: close()

      Cierra la comunicación con el conversor. Debe invocarse este
      método tras haber realizado todas las lecturas/escrituras
      requeridas del conversor.

   .. attribute:: data_link

      Enlace de datos que se usa en la comunicación con el conversor.

      Es una propiedad de sólo lectura.

   .. attribute:: description

      Descripción del conversor de datos.

      Es una propiedad de sólo lectura.

   .. attribute:: identifier

      Identificador del conversor de datos.

      Es una propiedad de sólo lectura.

   .. attribute:: levels

      Resolución en número de niveles del conversor de datos.

      Es una propiedad de sólo lectura.

   .. method:: open()

      Abre la comunicación con el conversor. Debe invocarse este
      método antes de realizar cualquier lectura/escritura del
      conversor.

   .. attribute:: vref

      Tensión de referencia del conversor. Es la tensión en voltios
      que se corresponde con el nivel más alto del conversor.

      Es una propiedad de sólo lectura.

Clase :class:`ADC`
------------------
.. class:: ADC(identifier, description, vref, bits, channels, data_link)

   Clase base para la definición de convertidores de datos
   analógico/digitales.

   Es una clase abstracta.

   Clase base: :class:`Converter`.

   :param identifier: identificador del conversor.
   :type identifier: :class:`String`
   :param description: descripción del conversor.
   :type description: :class:`String`
   :param vref: tensión de referencia del conversor.
   :type vref: :class:`Number`
   :param bits: resolución en bits del conversor.
   :type bits: :class:`Integer`
   :param channels: número de canales del conversor.
   :type channels: :class:`Integer`
   :param data_link: enlace de datos para la comunicación con el conversor.
   :type data_link: :class:`piDA.links.DataLink`

   .. method:: read(channel)
      
      Realiza una lectura de un canal del conversor analógico/digital
      y devuelve su valor en voltios.

      :param channel: Canal del conversor que quiere leerse.
      :type channel: :class:`Number`

   .. method:: read_code(channel)

      Realiza una lectura de un canal del conversor analógico/digital
      y devuelve el código de su valor.

      :param channel: Canal del conversor que quiere leerse.
      :type channel: :class:`Number`

      .. warning:: Es un método abstracto. Debe ser implementado por
	 cada heredero que defina un modelo concreto de conversor
	 analógico/digital.

Clase :class:`DAC`
------------------
.. class:: DAC(identifier, description, vref, bits, channels, data_link)
   
   Clase base para la definición de convertidores de datos
   digital/analógicos.

   Es una clase abstracta.

   Clase base: :class:`Converter`.

   :param identifier: identificador del conversor.
   :type identifier: :class:`String`
   :param description: descripción del conversor.
   :type description: :class:`String`
   :param vref: tensión de referencia del conversor.
   :type vref: :class:`Number`
   :param bits: resolución en bits del conversor.
   :type bits: :class:`Integer`
   :param channels: número de canales del conversor.
   :type channels: :class:`Integer`
   :param data_link: enlace de datos para la comunicación con el conversor.
   :type data_link: :class:`piDA.links.DataLink`

   .. method:: write(value, channel)

      Fija en un canal del conversor digital/analógico el valor
      especificado en voltios.

      :param value: Valor a fijar en voltios.
      :type value: :class:`Number`
      :param channel: Canal del conversor que quiere escribirse.
      :type channel: :class:`Number`

   .. method:: write_code(value, channel)

      Fija en un canal del conversor digital/analógico el valor
      especificado como código.

      :param value: Código del valor a escribir.
      :type value: :class:`Number`
      :param channel: Canal del conversor que quiere escribirse.
      :type channel: :class:`Number`

      .. warning:: Es un método abstracto. Debe ser implementado por
         cada heredero que defina un modelo concreto de conversor
         digital/analógico.

Clase :class:`MCP3002`
----------------------
.. class:: MCP3002(vref, data_link)

   Clase para gestionar el convertidor analógico/digital Microchip
   MCP3002.

   Clase base: :class:`ADC`

   :param vref: tensión de referencia del conversor.
   :type vref: :class:`Number`
   :param data_link: enlace de datos para la comunicación con el conversor.
   :type data_link: :class:`piDA.links.DataLink`

Clase :class:`MCP3202`
----------------------
.. class:: MCP3202(vref, data_link)

   Clase para gestionar el convertidor analógico/digital Microchip
   MCP3202.

   Clase base: :class:`ADC`

   :param vref: tensión de referencia del conversor.
   :type vref: :class:`Number`
   :param data_link: enlace de datos para la comunicación con el conversor.
   :type data_link: :class:`piDA.links.DataLink`

Clase :class:`MCP4802`
----------------------
.. class:: MCP4802(vref, data_link)

   Clase para gestionar el convertidor digital/analógico Microchip
   MCP4802.

   Clase base: :class:`DAC`

   :param vref: tensión de referencia del conversor.
   :type vref: :class:`Number`
   :param data_link: enlace de datos para la comunicación con el conversor.
   :type data_link: :class:`piDA.links.DataLink`
