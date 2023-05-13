from typing import Optional
from models.calculation_model import FormInput
import pandas as pd
from helpers.esforcos_solicitantes import get_esforcos


class CalculatorControl:

    @classmethod
    def perform_calculations(cls, dados: FormInput) -> str:
        comprimento = float(dados.comprimento)
        largura = float(dados.largura)
        altura = float(dados.altura)
        classeConcreto = dados.classeConcreto
        classeAgressividade = dados.classeAgressividade
        combAcoes = dados.combAcoes
        tramos = dados.tramos
        cargas = dados.cargas

        esforcos, momentos, cortantes = cls.esforcos_solicitantes(cargas=cargas, tramos=tramos, h=altura, b=largura,
                                                                  concreto=classeConcreto)

        return None

    @classmethod
    def esforcos_solicitantes(cls, cargas, tramos, h, b, concreto):
        nos_list = []
        coordenadas_list = []
        last_coordenada = 0
        for tramo in tramos:
            coordenadas_list.append([last_coordenada, 0])
            nos_list.append(last_coordenada)
            last_coordenada += float(tramo['comprimento'])
            if int(tramo['numero']) == 1:
                coordenadas_list.append([last_coordenada, 0])
                nos_list.append(last_coordenada)
                last_coordenada += float(tramo['comprimento'])

        node_ids_fixed = nos_list

        cargas_dist_list = []
        cargas_conc_list = []
        for carga in cargas:
            posicao_inicial = float(carga['posiInicial'])
            if posicao_inicial not in nos_list:
                coordenadas_list.append([posicao_inicial, 0])
                coordenadas_list = sorted(coordenadas_list, key=lambda x: x[0])
            if carga['tipo'] == 'Distribuída':
                posicao_final = float(carga['posiFinal'])
                if posicao_final not in nos_list:
                    coordenadas_list.append([posicao_final, 0])
                    coordenadas_list = sorted(coordenadas_list, key=lambda x: x[0])
                elemento_id = coordenadas_list.index([posicao_inicial, 0]) + 1
                cargas_dist_list.append([elemento_id, carga['intensidade']])
            elif carga['tipo'] == 'Concentrada':
                node_id = coordenadas_list.index([posicao_inicial, 0]) + 1
                cargas_conc_list.append([node_id, carga['intensidade']])

        results, moment_list, shear_list = get_esforcos(h, b, concreto, coordenadas_list, node_ids_fixed,
                                                        cargas_conc_list, cargas_dist_list)

        return results, moment_list, shear_list
