# Practica 1: Web Scraping.
## Descripción.
Proyecto realizado bajo el contexto de la primera práctica de la asignatura Tipología y ciclo de vida de los datos en el curso 2020-2021. El objetivo de este proyecto es extraer, 
mediante técnicas de Web Scraping, un conjunto de datos a partir de la información disponible en la página web http://www.webometrics.info/en.

## Componentes del grupo.
Esta actividad práctica se ha llevado a cabo de manera individual siendo el único autor de la misma Carlos Herrera Carballo.

## Descripción de los archivos.
En este repositorio se encuentran cuatro carpetas de archivos que listamos a continuación:

  - **Archivos csv**: esta carpeta contiene todos los archivos csv con los conjuntos de datos generados por el scraper implentado en esta práctica. Además, estos se dividen en dos
                  subcarpetas, Ranking Webometrics 2012-2020 y Ranking Webometrics 2021, que contienen los csv generados para la edición actual del ranking y el registro histórico 
                  de datos publicados en el ranking desde 2012 hasta 2020 respectivamente.
                  
  - **Arcchivos pdf**: esta carpeta contiene el pdf con las respuestas propuestas para esta primera práctica.
  
  - **Codigo Scraper**: en esta carpeta se encuentra el archivo python del scraper implementado (*Scraper_Webometrics.py*). Se trata de un script que solicita al usuario la entrada de dos 
  parámetros iniciales: tipo de información que desea extraer (ranking de universidades de Webometrics en su primera versión del año 2021 o registro histórico de los datos publicados 
  en dicho ranking entre los años 2012 y 2020) y región de la que se desea obtener la información (las opciones disponibles comprenden los cinco continentes).
  
  - **DOI**: esta carpeta contiene un fichero de texto plano con las diferentes versiones del DOI obtenido para el conjunto de datos publicado en https://zenodo.org/.
