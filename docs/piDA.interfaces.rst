=============================
Módulo :mod:`piDA.interfaces`
=============================
.. module:: piDA.interfaces

Este módulo incluye clases para gestionar interfaces de adquisición de
datos.

Clase :class:`Channel`
----------------------
.. class:: Channel(identifier, description, converter, converter_channel)
	   
   Clase base para la gestión de un canal de una interfaz de adquisición de datos.

   Es una clase abstracta.

   Clase base: :class:`object`.

   :param identifier: identificador del canal.
   :type identifier: :class:`String`
   :param description: descripción del canal.
   :type description: :class:`String`
   :param converter: conversor de datos asociado al canal.
   :type converter: :class:`piDA.converters.Converter`
   :param converter_channel: canal del conversor de datos asociado al canal.
   :type converter_channel: :class:`Integer`

   .. method:: close()

      Cierra el canal.

   .. attribute:: converter

      Conversor de datos asociado al canal.

      Es una propiedad de sólo lectura.

   .. attribute:: converter_channel

      Canal del conversor de datos asociado al canal.

      Es una propiedad de sólo lectura.

   .. attribute:: description

      Descripción del canal.

      Es una propiedad de sólo lectura.

   .. attribute:: identifier

      Identificador del canal.

      Es una propiedad de sólo lectura.

   .. method:: open()

      Abre el canal. Es necesario invocar este método antes de
      realizar la primera escritura/lectura del canal.

Clase :class:`OutputChannel`
----------------------------
.. class:: OutputChannel(identifier, description, converter, converter_channel)

   Clase para la gestión de un canal de salida de una interfaz de
   adquisición de datos.

   Clase base: :class:`Channel`.
   
   :param identifier: identificador del canal.
   :type identifier: :class:`String`
   :param description: descripción del canal.
   :type description: :class:`String`
   :param converter: conversor de datos asociado al canal.
   :type converter: :class:`piDA.converters.Converter`
   :param converter_channel: canal del conversor de datos asociado al canal.
   :type converter_channel: :class:`Integer`

   .. method:: write(value)

      Escribre un valor en voltios en el canal.

Clase :class:`InputChannel`
---------------------------
.. class:: InputChannel(identifier, description, converter, converter_channel)

   Clase para la gestión de un canal de entrada de una interfaz de
   adquisición de datos.

   Clase base: :class:`Channel`.

   :param identifier: identificador del canal.
   :type identifier: :class:`String`
   :param description: descripción del canal.
   :type description: :class:`String`
   :param converter: conversor de datos asociado al canal.
   :type converter: :class:`piDA.converters.Converter`
   :param converter_channel: canal del conversor de datos asociado al canal.
   :type converter_channel: :class:`Integer`

   .. method:: read()

      Lee un valor en voltios en el canal.

Clase :class:`Interface`
------------------------
.. class:: Interface(identifier, description, channel_list)

   Clase base para la definición de interfaces de adquisición de
   datos.

   Es una clase abstracta.

   Clase base: :class:`object`.

Clase :class:`Gertboard`
------------------------
.. class:: Gertboard()

   Clase base: :class:`Interface`

Clase :class:`piDAInterface0`
-----------------------------
.. class:: piDAInterface0()

   Clase base: :class:`Interface`

Clase :class:`piDAInterface`
----------------------------
.. class:: piDAInterface()

   Clase base: :class:`Interface`
