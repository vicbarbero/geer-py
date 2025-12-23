# geer-py
GEEr es un Generador de Estadísticas de Evaluación para raíces. Es un programa desarrollado en python para línea de comandos que recibe como parámetro un fichero .csv de exportación de calificaciones de raíces y genera un fichero .PDF con distintas estadísticas de esos resultados:

- el alumnado con calificación positiva o negativa en cada materia
- la distribución del alumnado por número de materias suspensas
- media de calificaciones por materia
- media de suspensos por alumno o alumna
- desviación de porcentaje de suspensos de materia, módulo o ámbito respecto a la media de aprobados
- distribución de alumnado por media de calificaciones y
- alumnado con mejor calificación media.

También se le puede pasar por parámetro el nombre de una carpeta, que recorrerá recursivamente procesando los ficheros .csv que encuentre y generando los .PDF correspondientes.

Esta versión es una refactorización de GEEr (https://github.com/vicbarbero/GEEr) usando Gemini 3 Pro y modificaciones manuales del código generado. 

GEEr-py, como GEEr, no almacena ni envía por internet ningún dato que facilites.

