@echo off svm-train -s 0 -c 5 -t 0 -g 0.5 -e 0.1  -w-1 0.1 -w1 10 a1a a1.model
@echo off svm-train -s 0 -c 5 -t 0 -g 0.5 -e 0.1  -w-1 0.2 -w1 20 a1a a2.model
svm-train -s 0 -c 5 -w-1 0.2 -w1 20 tr1.txt tr1.model
pause