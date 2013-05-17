#!/bin/bash

if [ $# -lt 1 ]
  then 
    echo "Error. Numero de Argumentos invalido"
else
    ./fun.py $1
	if [ -f entrada.pl ]
		then gnuplot entrada.pl
	else
		echo "No hay nada a graficar"
	fi
fi
