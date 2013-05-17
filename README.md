Interpretador GNU PLOT
=======================

Proyecto de Traductores e Interpretadores
-----------------------------------------
El proyecto consiste en generar un interpretador para un Graficador (GNUplot), la especificacion del lenguaje esta en el Enunciado.pdf

La Parte I, Construye el Interpretador que verificara la sintaxys del Lenguaje y Construira el AST (Abstract syntax tree)

La Parte II, Agrega la parte Semantica generando asi, mediante el GNUplot, Graficas

Desarrollo
----------
Todo fue Realizado con Python

Librerias: [PLY](http://www.dabeaz.com/ply/) y [GNUplot](http://www.gnuplot.info/)

Sintaxys de Llamada
-------------------
(Linux)

./mygnuplot.sh <entrada>

entrada es un archivo de texto plano con lo que se va a Graficar/Interpretar

En la carpeta se Generara un PDF de nombre <entrada>.pdf que contendra la Grafica

(Windows)

./fun.py <entrada>
entrada es un archivo de texto plano con lo que se va a Graficar/Interpretar

./gnuplot entrada.pl
En la carpeta se Generara un PDF de nombre <entrada>.pdf que contendra la Grafica

Integrantes
------------
	Jesus Torres
	Gabrielle Sparano