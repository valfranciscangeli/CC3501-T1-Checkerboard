# tarea01_graficas
tarea 1 para el curso CC3501
Por Valeria Vallejos Franciscangeli vvfranciscangeli@gmail.com
Repositorio con distintas implementaciones, enunciado e imagenes 
de referencia disponible en:
https://github.com/valfranciscangeli/Tablero_de_damas-Tarea1_CC3501.git

Para esta Tarea, me basé en el dibujo de muestra del enunciado 
para encontrar las coordenadas adecuadas.
Se puede ver un bosquejo de esto en el archivo 
"coordenadas_basicas_tablero.png".

Esta versión fue implementada utilizando vao y vbo. Optimización
respecto a primeras implementaciones: uso de ciclo for para dibujar
figuras de geometria recurrente y se crean funciones para simplificar
implementación del código.

Para implementar cambios de apariencia del tablero me basé en el 
tablero que se puede encontrar en el archivo "damas_inspo.png".
Los cambios fueron, básicamente, crear un marco al tablero y 
agregar por medio de figuras un efecto de luz y sombra en las 
damas. Además, se cambia color de fondo de la ventana.

Colores usados en RGB normalizado:
Marco tablero:
0.247, 0.074, 0.007
0.564, 0.490, 0.419
Tablero:
0.517, 0.247, 0.007
0.854, 0.749, 0.501
Luz damas:
0.980, 0.968, 0.929
Sombra damas:
0.329, 0.298, 0.231
Damas:
0.117, 0.333, 0.423
0.878, 0.219, 0.109
Fondo: 
0.145, 0.221, 0.113 (alfa= 1.0)

Comentarios dentro del código en español. Algunos se mantienen en
inglés, originales del código base "tarea1_v0.py".

Para ejecutar los códigos se deben intalar ciertas librerías. 
- Utilizando pip: pip install numpy scipy matplotlib pyopengl glfw ipython jupyter pillow imgui[glfw]
