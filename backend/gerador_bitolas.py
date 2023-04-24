import boto3
import math
from decimal import Decimal
import json


def gerar_bitolas(phi_estribo, list_bws, cobrimento, phi_agregado):
    list_final = []
    list_phi = [0.63, 0.8, 1.0, 1.25, 1.6, 2.0, 2.5]
    for bw in list_bws:
        for phi in list_phi:
            n = 2
            while (((bw - 2 * cobrimento - 2 * phi_estribo - n * phi) / (n - 1)) > 2) and (
                    ((bw - 2 * cobrimento - 2 * phi_estribo - n * phi) / (n - 1)) > phi) and (
                    ((bw - 2 * cobrimento - 2 * phi_estribo - n * phi) / (
                            n - 1)) > 1.2 * phi_agregado):

                item_final = {'bw': 0, 'area': 0, 'list_bitolas_camadas': [], 'list_barras_por_camada': [],
                              'numero_camadas': 0, 'cg_armadura': []}

                barras_por_camada = [n, 0, 0]
                phi_camadas = [phi, 0, 0]
                area_list = list(map(lambda x: math.pi * (x ** 2 / 4), phi_camadas))
                area_final_list = [a * b for a, b in zip(area_list, barras_por_camada)]
                cg = cobrimento + 0.5 + phi / 2
                item_final['bw'] = bw
                item_final['list_barras_por_camada'] = barras_por_camada
                item_final['list_bitolas_camadas'] = phi_camadas
                item_final['area'] = sum(area_final_list)
                item_final['numero_camadas'] = 1
                item_final['cg_armadura'] = [cg, 0, 0]
                list_final.append(item_final)
                n += 1

            n_max_primeira_camada = n - 1

            for phi_segunda_camada in list_phi:
                n_segunda_camada = 2
                while (((bw - 2 * cobrimento - 2 * phi_estribo - n_segunda_camada * phi_segunda_camada) / (
                        n_segunda_camada - 1)) > 2) and (
                        ((bw - 2 * cobrimento - 2 * phi_estribo - n_segunda_camada * phi_segunda_camada) / (
                                n_segunda_camada - 1)) > phi_segunda_camada) and (
                        ((bw - 2 * cobrimento - 2 * phi_estribo - n_segunda_camada * phi_segunda_camada) / (
                                n_segunda_camada - 1)) > 1.2 * phi_agregado):

                    item_final = {'bw': 0, 'area': 0, 'list_bitolas_camadas': [],
                                  'list_barras_por_camada': [],
                                  'numero_camadas': 0}

                    barras_por_camada = [n_max_primeira_camada, n_segunda_camada, 0]
                    phi_camadas = [phi, phi_segunda_camada, 0]
                    area_list = list(map(lambda x: math.pi * (x ** 2 / 4), phi_camadas))
                    area_final_list = [a * b for a, b in zip(area_list, barras_por_camada)]
                    sv1 = max(2, phi, 0.5 * phi_agregado)
                    cg1 = cobrimento + 0.5 + phi / 2
                    cg2 = cobrimento + 0.5 + phi + sv1 + phi_segunda_camada / 2

                    item_final['bw'] = bw
                    item_final['list_barras_por_camada'] = barras_por_camada
                    item_final['list_bitolas_camadas'] = phi_camadas
                    item_final['area'] = sum(area_final_list)
                    item_final['numero_camadas'] = 2
                    item_final['cg_armadura'] = [cg1, cg2, 0]
                    list_final.append(item_final)
                    n_segunda_camada += 1
                    phi_max_segunda_camada = phi_segunda_camada

                n_max_segunda_camada = n_segunda_camada - 1

                for phi_teceira_camada in list_phi:
                    n_terceira_camada = 2
                    while (((bw - 2 * cobrimento - 2 * phi_estribo - n_terceira_camada * phi_teceira_camada) / (
                            n_terceira_camada - 1)) > 2) and (
                            ((
                                     bw - 2 * cobrimento - 2 * phi_estribo - n_terceira_camada * phi_teceira_camada) / (
                                     n_terceira_camada - 1)) > phi_teceira_camada) and (
                            ((
                                     bw - 2 * cobrimento - 2 * phi_estribo - n_terceira_camada * phi_teceira_camada) / (
                                     n_terceira_camada - 1)) > 1.2 * phi_agregado):

                        item_final = {'bw': 0, 'area': 0, 'list_bitolas_camadas': [],
                                      'list_barras_por_camada': [],
                                      'numero_camadas': 0}

                        barras_por_camada = [n_max_primeira_camada, n_max_segunda_camada, n_terceira_camada]
                        phi_camadas = [phi, phi_max_segunda_camada, phi_teceira_camada]
                        area_list = list(map(lambda x: math.pi * (x ** 2 / 4), phi_camadas))
                        area_final_list = [a * b for a, b in zip(area_list, barras_por_camada)]
                        sv1 = max(2, phi, 0.5 * phi_agregado)
                        sv2 = max(2, phi_max_segunda_camada, 0.5 * phi_agregado)
                        cg1 = cobrimento + 0.5 + phi / 2
                        cg2 = cobrimento + 0.5 + phi + sv1 + phi_max_segunda_camada / 2
                        cg3 = cobrimento + 0.5 + phi + sv1 + phi_max_segunda_camada + sv2 + phi_teceira_camada / 2
                        item_final['bw'] = bw
                        item_final['list_barras_por_camada'] = barras_por_camada
                        item_final['list_bitolas_camadas'] = phi_camadas
                        item_final['area'] = sum(area_final_list)
                        item_final['numero_camadas'] = 3
                        item_final['cg_armadura'] = [cg1, cg2, cg3]
                        list_final.append(item_final)
                        n_terceira_camada += 1

    return list_final


def insert_into_dynamodb(table_name, item):
    dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
    table = dynamodb.Table(table_name)
    changed_data = json.loads(json.dumps(item), parse_float=Decimal)
    table.put_item(Item=changed_data)


if __name__ == '__main__':
    list_bws = [*range(15, 65, 5)]
    bitolas_list = gerar_bitolas(phi_estribo=0.5, list_bws=list_bws, cobrimento=2.5, phi_agregado=2.28)
    for item in bitolas_list:
        insert_into_dynamodb('armadura_transversal', item)
    print(bitolas_list)
