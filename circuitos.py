#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 12:43:15 2018

Trabalho computacional para a matéria Circuitos Elétricos I
Engenharia de Computação, Universidade Católica de Petrópolis

@author: arthurbaldner
"""

import math
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# sistema para solução da equação diferencial
def model(x, t, b, c, d):
    y, dy = x[0], x[1]
    system = [dy, - b * dy - c * y + d]
    return system

# Garante que o usuário digitou um número, e nâo interrompe o programa inteiro em caso de erro
def ErrorHandle(l,n):   
    while n is None:
        try:
            n = float(input(l+': '))
        except ValueError:
            print('Digitar um número, usando ponto para separar sua parte inteira da decimal.')
    return n


def main():

    # garantia que o usuário fornecerá entradas válidas    
    tipo = input('Circuito série ou paralelo? ')
    while tipo != 'série' and tipo != 'paralelo':
        print('Favor digitar corretamente.')
        tipo = input('Circuito série ou paralelo? ')
    
    
    ######## Parâmetros ########
        
    parametros = input('Parâmetros de circuito ou de oscilação? ')
    while parametros != 'circuito' and parametros != 'oscilação':
        print('Favor digitar corretamente.')
        parametros = input('Parâmetros de circuito ou de oscilação? ')
        
    R, L, C = None, None, None
    
    # usuário optou por fornecer os parâmetros do circuito - R, L, C
    if parametros == 'circuito':
        print('Informe os valores de R ['+chr(937)+'], C [F] e L [H].')
        R = ErrorHandle('R',R)
        L = ErrorHandle('L',L)
        C = ErrorHandle('C',C)
        
        # Calculo dos parâmetros de oscilação
        if tipo == 'série':
            alfa = R/(2*L)
        elif tipo == 'paralelo': # uso do elif para garantir claridade quanto ao tipo de circuito
            alfa = 1/math.sqrt(2*R*C)
        
        w0 = 1/math.sqrt(L*C)
        
        # cálculo da frequência amortecida, caso ela nâo seja 0
        if w0 > alfa:
            wd = math.sqrt(w0**2 - alfa**2)
        else:
            wd = 0
            
            
    # usuário optou por fornecer os parâmetros de oscilação - Frequência natural, Amortecimento e Frequência Amortecida - caso exista 
    elif parametros == 'oscilação':
        w0, alfa = None, None
        print('Informe os valores da frequência natural [rad/s], amortecimento [Hz].')
        w0 = ErrorHandle(chr(969)+chr(8320),w0)
        alfa = ErrorHandle(chr(945),alfa)
        
        # cálculo da frequência amortecida, caso ela nâo seja 0
        if w0 > alfa:
            wd = math.sqrt(w0**2 - alfa**2)
        else:
            wd = 0
            
        # Cálculo dos parâmetros do circuito
        print('Forneça um valor adicional do circuito.')
        
        # É necessário conhecer um dos valores do circuito - R, L ou C - para poder realizar o cálculo dos outros parâmetros
        var = input('Digite R para fornecer o valor da resistência ['+chr(937)+'], L para fornecer o valor da indutância [H] ou C para fornecer o valor da capacitância [F]: ')
        while var != 'R' and var != 'L' and var != 'C':
            print('Favor digitar corretamente.')
            var = input('Digite R para fornecer o valor da resistência ['+chr(937)+'], L para fornecer o valor da indutância [H] ou C para fornecer o valor da capacitância [F]: ')
               
        # usuário fornece R - L e C sâo calculados
        if var == 'R':
            R = ErrorHandle('R',R)
            if tipo == 'série':
                L = R/(2*alfa)
                C = 1/((w0**2)*L)
            elif tipo == 'paralelo':
                C = 1/(2*R*alfa)
                L = 1/((w0**2)*C)
    
        # usuário fornece L - R e C sâo calculados            
        elif var == 'L':
            L = ErrorHandle('L',L)
            C = 1/((w0**2)*L)
            if tipo == 'série':
                R = alfa*2*L
            elif tipo == 'paralelo':
                R = 1/(2*C*alfa)
                
        # usuário forenece C - R e L sâo calculados
        else:
            C = ErrorHandle('C',C)
            L = 1/((w0**2)*C)
            if tipo == 'série':
                R = 2*alfa*L
            elif tipo == 'paralelo':
                R = 1/(2*C*alfa)
        
    # todos os parâmetros sâo exibidos na tela
    print('\n\nValores dos parâmetros:')
    print('R = '+str(R)+'; L = '+str(L)+'; C = '+str(C))
    print(chr(969)+chr(8320)+'= '+str(w0)+'; '+chr(945)+' = '+str(alfa)+'; '+chr(969)+chr(8340)+' = '+str(wd)+'\n\n')    
    
    
    
    ######## Gráfico ########
    
    # Condições iniciais do circuito
    I0, V0 = None, None
    print('Qual o valor da corrente inicial I0 [A] no indutor e da tensão inicial V0 [V] no capacitor?')
    I0 = ErrorHandle('I0',I0)
    V0 = ErrorHandle('V0',V0)

    # tempo inicial tempo final, quantidade de samples
    t = np.linspace(0,10,100)
 

    # Usuário pode escolher o gráfico desejado
    If, Vf = None, None
    
    if tipo == 'série':
        print('Escolha o gráfico desejado.')
        escolha = input('Digite "corrente" para obter o gráfico da corrente pelo circuito ou "tensâo" para obter o gráfico da tensâo no capacitor: ')
        while escolha != 'corrente' and escolha != 'tensão':
            print('Favor digitar corretamente.')
            escolha = input('Digite "corrente" para obter o gráfico da corrente pelo circuito ou "tensâo" para obter o gráfico da tensâo no capacitor: ')
        
        if escolha == 'corrente':
            print('Qual o valor da função de forçamento If [A] desse circuito?')
            If = ErrorHandle('If',If)
            z = odeint(model, [I0-If,(V0/L)], t, args=(2*alfa,w0**2,If))
            plt.ylabel('i(t)')
            
        elif escolha == 'tensão':
            print('Qual o valor da função de forçamento Vf [V] desse circuito?')
            Vf = ErrorHandle('Vf',Vf)
            z = odeint(model, [V0-Vf,(I0/C)], t, args=(2*alfa,w0**2,Vf))
            plt.ylabel('v(t)')

    elif tipo == 'paralelo':
        print('Escolha o gráfico desejado.')
        escolha = input('Digite "tensâo" para obter o gráfico da tensâo do circuito ou "corrente" para obter o gráfico da corrente no indutor: ')
        while escolha != 'corrente' and escolha != 'tensão':
            print('Favor digitar corretamente.')
            escolha = input('Digite "tensão" para obter o gráfico da tensâo do circuito ou "corrente" para obter o gráfico da corrente no indutor: ')
        
        if escolha == 'tensão':
            print('Qual o valor da função de forçamento Vf [V] desse circuito?')
            Vf = ErrorHandle('Vf',Vf)
            z = odeint(model, [V0-Vf,(I0/C)], t, args=(2*alfa,w0**2,Vf))
            plt.ylabel('v(t)')
            
        elif escolha == 'corrente':
            print('Qual o valor da função de forçamento If [A] desse circuito?')
            If = ErrorHandle('If',If)
            z = odeint(model, [I0-If,(V0/L)], t, args=(2*alfa,w0**2,If))
            plt.ylabel('i(t)')
            
            
    # Plotagem do gráfico  
    plt.plot(t,z[:,0],'b')
    plt.xlabel('Time')
    plt.show()        
    
    
if __name__ == "__main__":
    main()