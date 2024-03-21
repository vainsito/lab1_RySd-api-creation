# Introducción 
## Problema 
    Me gustaría poder utilizar los siguientes tipos de URL: - http: //中文.tw/ - https: //💩.la2 Sin embargo, los siguientes tipos El número de URL que se pueden utilizar es un carácter ASCII.
 ## Solución 
 Necesitamos poder encontrar una manera de mostrar caracteres que no sean ASCII.
 Esto utiliza **codificación de URL**.
 # Codificación URL 
 La codificación URL reemplaza caracteres que no son ASCII o caracteres que pueden causar problemas al usar ciertas codificaciones.
 Esto se hace utilizando "codificación porcentual".
 ## Codificación porcentual 
 La codificación porcentual representa un octeto de datos en un componente cuando el carácter correspondiente a ese octeto está fuera del conjunto de caracteres permitido o es un carácter utilizado para otros fines.
 Si son confusos, es necesario codificarlos.
 Un octeto codificado con codificación porcentual se codifica como un conjunto de caracteres que consta de un signo de porcentaje '%' seguido de  dos dígitos hexadecimales que representan el valor numérico del octeto.
 Por ejemplo, " " es el porcentaje de codificación del octeto binario "00100000", que  corresponde al carácter de espacio US-ASCII (SP).
 Fuente: https://www.rfc-editor.org/rfc/rfc3986#section-2.
1) ### Caracteres UTF-8 
 Codificar caracteres UTF-8 con codificación porcentual 1.
 Convierte una cadena  en una secuencia de bytes utilizando  codificación UTF-8.
 2.
 Convierta cada byte que no sea una letra o número ASCII al formato %HH.
 HH es el valor hexadecimal de bytes.
 ## Tipos de caracteres en las URL 
 Hay diferentes tipos de caracteres en las URL, que se explican a continuación.
 ### Caracteres seguros: 
 Son  caracteres alfanuméricos, es decir 0-9, a-z y A-Z, caracteres especiales $, -, _, . , +, ! , *, ', (, ) son carácteres reservados con una función específica.
 No es necesario codificar estos caracteres.
 ### Caracteres de control ASCII: 
 Contiene caracteres en el rango hexadecimal 00-1F  (0-31 decimal) y 7F (127 decimal).
 Estos caracteres se tienen que codificar.
 ### Caracteres de control no ASCII: 
 Contiene 80 a FF hexadecimal (128 a 255 decimal).
 Estos caracteres se tienen que codificar.
 ### Caracteres reservados: 
 Estos caracteres se utilizan para fines especiales y requieren codificación.
 ### Caracteres no seguros: 
 Estos caracteres pueden malinterpretarse en las URL por varias razones.
 Estos caracteres se tienen que codificar.
 #### Ejemplo 
 Caracteres utilizados como delimitadores antes y después de las URL en texto libre < y >
