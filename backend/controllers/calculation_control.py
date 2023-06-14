from models.calculation_model import FormInput
import pandas as pd
from helpers.esforcos_solicitantes import get_esforcos
from helpers.tabelas_kc_ks import select_all
from helpers.gerador_armaduras import gerador_armaduras
import numpy as np
import json
import math


class CalculatorControl:

    @classmethod
    def perform_calculations(cls, dados: FormInput, tipo_resultado='esforcos', tipo_plot='') -> str:
        dict_fck = {'C20': 20, 'C25': 25, 'C30': 30, 'C35': 35, 'C40': 40, 'C45': 45, 'C50': 50}
        dict_combinacoes = {'Normais': 1.4, 'Especiais ou de Construção': 1.3, 'Excepcionais': 1.2}
        dict_cobrimento = {'I': 2.5, 'II': 3, 'III': 4, 'IV': 5}

        comprimento = float(dados.comprimento)
        largura = float(dados.largura)
        altura = float(dados.altura)
        classeConcreto = dados.classeConcreto
        fck = dict_fck[classeConcreto]
        classeAgressividade = dados.classeAgressividade
        combAcoes = dados.combAcoes
        gama_f = dict_combinacoes[combAcoes]

        tramos = dados.tramos
        tramos = sorted(tramos, key=lambda x: int(x['numero']))

        cargas = dados.cargas
        constante_mola_esq = dados.constanteMolaEsq
        constante_mola_dir = dados.constanteMolaDir

        if constante_mola_dir == '':
            constante_mola_dir = 0
        else:
            constante_mola_dir = float(constante_mola_dir)

        if constante_mola_esq == '':
            constante_mola_esq = 0
        else:
            constante_mola_esq = float(constante_mola_esq)

        inercia = (largura * altura ** 3) / 12
        W_0 = inercia / (altura / 2)
        f_ctk_sup = (1.3 * 0.3 * fck ** (2 / 3)) / 10  # em kN/cm²

        tabela_kc_ks = select_all()

        cobrimento = dict_cobrimento[classeAgressividade]
        d_linha = cobrimento + 0.63 + 0.8
        d = round(altura - d_linha, 0)

        if tipo_resultado == 'plot':
            results = cls.__esforcos_solicitantes(cargas=cargas, tramos=tramos, h=altura, b=largura,
                                                  concreto=classeConcreto, constante_mola_esq=constante_mola_esq,
                                                  constante_mola_dir=constante_mola_dir,
                                                  tipo_resultado=tipo_resultado, tipo_plot=tipo_plot)
            return results

        esforcos, coordenadas_list = cls.__esforcos_solicitantes(cargas=cargas, tramos=tramos, h=altura, b=largura,
                                                                 concreto=classeConcreto,
                                                                 constante_mola_esq=constante_mola_esq,
                                                                 constante_mola_dir=constante_mola_dir)

        momento_limite = cls.__momento_limite(d=d, classe_concreto=classeConcreto,
                                              b=largura, tabela_kc_ks=tabela_kc_ks)

        momento_minimo = 0.8 * W_0 * f_ctk_sup

        armadura_df = cls.__armaduras(esforcos=esforcos, gama_f=gama_f, largura=largura, d=d, d_linha=d_linha,
                                      tabela_kc_ks=tabela_kc_ks,
                                      momento_limite=momento_limite, momento_minimo=momento_minimo,
                                      classe_concreto=classeConcreto, altura=altura, coordenadas=coordenadas_list)

        armadura_df = cls.__estribos(armadura_df=armadura_df, largura=largura, d=d, fck=fck, tipoCombinacao=combAcoes)

        armadura_com_bitolas = cls.__calcula_bitolas(armadura_df=armadura_df, largura=float(largura),
                                                     cobrimento=float(cobrimento), altura=float(altura))

        armadura_com_bitolas['detalhamento_tracao'] = armadura_com_bitolas['detalhamento_tracao'].apply(
            lambda x: json.loads(x) if isinstance(x, str) and x.strip().startswith('{') else x)

        armadura_com_bitolas['detalhamento_compressao'] = armadura_com_bitolas['detalhamento_compressao'].apply(
            lambda x: json.loads(x) if isinstance(x, str) and x.strip().startswith('{') else x)

        coordenadas_desenho = armadura_com_bitolas['coord'].tolist()
        coordenadas_apoios_desenho = [0]
        inicio = 0
        for item in tramos:
            coord_final_tramo = inicio + float(item['comprimento'])
            coordenadas_apoios_desenho.append(coord_final_tramo)
            inicio += float(item['comprimento'])

        armadura_com_bitolas['coord'] = armadura_com_bitolas['coord'].apply(
            lambda x: str(round(x, 2)).replace('.', ','))

        #armadura_com_bitolas['Ast_efe'] = armadura_com_bitolas['Ast_efe'].apply(lambda x: str(round(x, 2)).replace('.', ','))

        if 'Asc' in armadura_com_bitolas.columns:
            armadura_com_bitolas['Asc'] = armadura_com_bitolas['Asc'].apply(lambda x: str(round(x, 2)).replace('.', ','))
            #armadura_com_bitolas['Asc_efe'] = armadura_com_bitolas['Asc_efe'].apply(lambda x: str(round(x, 2)).replace('.', ','))

        armadura_com_bitolas['Ast'] = armadura_com_bitolas['Ast'].apply(lambda x: str(round(x, 2)).replace('.', ','))
        armadura_com_bitolas['Msk'] = armadura_com_bitolas['Msk'].apply(lambda x: str(round(x, 2)).replace('.', ','))
        armadura_com_bitolas['Msd'] = armadura_com_bitolas['Msd'].apply(lambda x: str(round(x, 2)).replace('.', ','))
        armadura_com_bitolas['Vsk'] = armadura_com_bitolas['Vsk'].apply(lambda x: str(round(x, 2)).replace('.', ','))
        armadura_com_bitolas['Vsd'] = armadura_com_bitolas['Vsd'].apply(lambda x: str(round(x, 2)).replace('.', ','))

        armadura_com_bitolas_list = json.loads(armadura_com_bitolas.to_json(orient='records'))
        dict_props_viga = {'largura': largura, 'altura': altura, 'cobrimento': cobrimento, 'comprimento': comprimento, 'coordenadas_desenho': coordenadas_desenho, 'coordenadas_apoios_desenho': coordenadas_apoios_desenho}
        armadura_com_bitolas_list.append(dict_props_viga)

        return armadura_com_bitolas_list

    @classmethod
    def __esforcos_solicitantes(cls, cargas, tramos, h, b, concreto, constante_mola_esq, constante_mola_dir,
                                tipo_resultado='esforcos',
                                tipo_plot=''):
        nos_list = []
        coordenadas_list = []
        last_coordenada = 0
        for tramo in tramos:
            if int(tramo['numero']) == 1:
                coordenadas_list.append([0, 0])
                nos_list.append(0)
            last_coordenada += float(tramo['comprimento'])
            coordenadas_list.append([last_coordenada, 0])
            nos_list.append(last_coordenada)

        node_ids_fixed = nos_list

        cargas = sorted(cargas, key=lambda x: x['tipo'])

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
                elemento_id_inicial = coordenadas_list.index([posicao_inicial, 0]) + 1
                elemento_id_final = coordenadas_list.index([posicao_final, 0])
                cargas_dist_list.append([elemento_id_inicial, carga['intensidade']])
                if elemento_id_final != elemento_id_inicial:
                    cargas_dist_list.append([elemento_id_final, carga['intensidade']])
                dif = elemento_id_final - elemento_id_inicial
                if dif > 1:
                    for i in range(dif):
                        elemento_id = elemento_id_inicial + i
                        cargas_dist_list.append([elemento_id, carga['intensidade']])
            elif carga['tipo'] == 'Concentrada':
                node_id = coordenadas_list.index([posicao_inicial, 0]) + 1
                cargas_conc_list.append([node_id, carga['intensidade']])

        if tipo_resultado == 'esforcos':
            results = get_esforcos(h, b, concreto, coordenadas_list, node_ids_fixed,
                                   cargas_conc_list, cargas_dist_list, constante_mola_esq, constante_mola_dir)
            return results, coordenadas_list
        elif tipo_resultado == 'plot':
            results = get_esforcos(h, b, concreto, coordenadas_list, node_ids_fixed,
                                   cargas_conc_list, cargas_dist_list, constante_mola_esq, constante_mola_dir,
                                   tipo_resultado=tipo_resultado,
                                   tipo_plot=tipo_plot)
            return results

    @classmethod
    def __momento_limite(cls, b, d, classe_concreto, tabela_kc_ks):
        kc_lim = tabela_kc_ks.loc[0.45, classe_concreto]

        momento_limite = b * d ** 2 / kc_lim
        return momento_limite

    @classmethod
    def __armaduras(cls, esforcos, gama_f, largura, d, tabela_kc_ks, momento_limite, momento_minimo, classe_concreto,
                    d_linha, altura, coordenadas):
        armadura_df = pd.DataFrame(
            columns=['Msk', 'Msd', 'Bx_lim'])

        ksc_dict = {
            0.05: 0.023,
            0.1: 0.023,
            0.15: 0.023,
            0.2: 0.031,
            0.25: 0.052
        }

        taxa_armadura_minima = {'C20': 0.0015, 'C25': 0.0015, 'C30': 0.0015, 'C35': 0.00164, 'C40': 0.00179,
                                'C45': 0.00194, 'C50': 0.00208}
        area_concreto = largura * altura
        armadura_minima = taxa_armadura_minima[classe_concreto] * area_concreto

        for item in esforcos:
            list_momentos = []
            incremento_dist = item['length'] / 50
            momentos = item['M']
            cortantes = item['Q']
            for i in range(0, 60, 10):
                if i != 0:
                    momento_dict = {'momento': -momentos[i - 1],
                                    'coordenada': coordenadas[item['id'] - 1][0] + incremento_dist * (i), 'cortante': -cortantes[i - 1]}
                else:
                    momento_dict = {'momento': -momentos[i], 'coordenada': coordenadas[item['id'] - 1][0], 'cortante': -cortantes[i]}
                list_momentos.append(momento_dict)

            momento_min = -item['Mmax']
            posicao_lista_min = np.where(momentos == -momento_min)[0][0]
            cortante_posicao_lista_min = -cortantes[posicao_lista_min]

            if posicao_lista_min != 0:
                posicao_lista_min += 1

            list_momentos.append({'momento': momento_min,
                                  'coordenada': coordenadas[item['id'] - 1][0] + incremento_dist * posicao_lista_min, 'cortante': cortante_posicao_lista_min})

            momento_max = -item['Mmin']
            posicao_lista_max = np.where(momentos == -momento_max)[0][0]
            cortante_posicao_lista_max = -cortantes[posicao_lista_max]

            if posicao_lista_max != 0:
                posicao_lista_max += 1

            list_momentos.append({'momento': momento_max,
                                  'coordenada': coordenadas[item['id'] - 1][0] + incremento_dist * posicao_lista_max, 'cortante': cortante_posicao_lista_max})

            for momento in list_momentos:
                line = pd.DataFrame({'coord': momento['coordenada'], 'Msk': [round(momento['momento'], 6)],
                                     'Msd': [momento['momento'] * gama_f], 'Vsk': [round(momento['cortante'], 6)], 'Vsd': [momento['cortante'] * gama_f], 'Bx_lim': [0.45]})

                armadura_df = pd.concat([armadura_df, line], ignore_index=True)

        armadura_df = armadura_df.groupby(['coord']).agg(
            {'Msk': 'first', 'Msd': 'first', 'Vsk': 'first', 'Vsd': 'first', 'Bx_lim': 'first'}).reset_index()
        for index, row in armadura_df.iterrows():
            if abs(row['Msd']) > momento_limite:
                armadura_df.loc[index, 'armaduraDupla'] = True
                Msd_1 = momento_limite
                ks_lim = tabela_kc_ks.loc[0.45, 'CA50']
                Ast_1 = ks_lim * Msd_1 / d
                Msd_2 = abs(row['Msd']) - Msd_1
                Ast_2 = 0.023 * Msd_2 / (d - d_linha)
                d_linha_h = d_linha / altura
                ksc_key = min(ksc_dict.keys(), key=lambda x: abs(x - d_linha_h))
                ksc = ksc_dict[ksc_key]
                Asc = ksc * Msd_2 / (d - d_linha)
                Ast = Ast_1 + Ast_2
                armadura_df.loc[index, 'Ast'] = Ast
                armadura_df.loc[index, 'Asc'] = Asc
            else:
                armadura_df.loc[index, 'armaduraDupla'] = False
                Msd = abs(row['Msd'])
                if Msd < momento_minimo:
                    Msd = momento_minimo
                kc = largura * d ** 2 / Msd
                armadura_df.loc[index, 'kc'] = kc
                Bx = (tabela_kc_ks[classe_concreto] - kc).abs().idxmin()
                armadura_df.loc[index, 'Bx'] = Bx
                ks = tabela_kc_ks.loc[Bx, 'CA50']
                armadura_df.loc[index, 'ks'] = ks
                Ast = abs(Msd) * ks / d
                if Ast < armadura_minima:
                    Ast = armadura_minima
                armadura_df.loc[index, 'Ast'] = Ast

        if altura >= 60:  # tem armadura de pele
            Ac = largura * altura
            A_pele_min = 0.001 * Ac
            armadura_df['A_pele_min'] = A_pele_min
            armadura_df['A_pele_espac_min'] = min(20, int(d / 3), int(15 * 1.6))

        return armadura_df

    @classmethod
    def __estribos(cls, armadura_df, largura, d, fck, tipoCombinacao):
        dict_taxa_armadura_min = {20: 0.088, 25: 0.103, 30: 0.116, 35: 0.128, 40: 0.140, 45: 0.152, 50: 0.163}
        dict_ghama_c = {'Normais': 1.4, 'Especiais ou de Construção': 1.2, 'Excepcionais': 1.2}
        list_estribos = [0.5, 0.63, 0.8, 1, 1.25]

        ghama_c = dict_ghama_c[tipoCombinacao]

        Vrd_u = 0.27*(1-(fck/250))*(fck/(ghama_c*10))*largura*d
        taxa_armadura_min = dict_taxa_armadura_min[fck]
        armadura_min = taxa_armadura_min * largura / 2 # divide por 2 pois o estribo tem 2 ramos
        area_estribo_min = math.pi*(0.25**2)
        espacamento_armadura_min = math.floor((area_estribo_min / armadura_min) * 100)

        Vc = 0.6*(0.7*0.3*fck**(2/3))*largura*d/(ghama_c*10)
        Vsw_min = armadura_min*2/100 * 0.9 * 43.5 * d
        Vrd_min = Vc + Vsw_min

        for index, row in armadura_df.iterrows():
            Vsd = abs(row['Vsd'])
            if Vsd < Vrd_min:
                if Vsd <= 0.67*Vrd_u:
                    espacamento_max = min(0.6*d, 30)
                else:
                    espacamento_max = min(0.6*d, 20)
                if espacamento_armadura_min > espacamento_max:
                    espacamento_armadura_min = espacamento_max

                mensagem_estribo_min = '1\u03A65mm c/ {}cm'.format(espacamento_armadura_min)
                armadura_df.loc[index, 'espacamento_estribo'] = espacamento_armadura_min
                armadura_df.loc[index, 'mensagem_estribo'] = mensagem_estribo_min
                armadura_df.loc[index, 'phi_estribo'] = 0.5
            else:
                #colocar aqui a iteracao de diametros de estribos
                for phi_estribo in list_estribos:
                    armadura = (Vsd - Vc)*100/(0.9*43.5*d)
                    armadura = armadura/2
                    area_estribo = math.pi*(phi_estribo/2)**2
                    espacamento = math.floor((area_estribo / armadura) * 100)
                    if espacamento < 10:
                        continue

                    if Vsd <= 0.67 * Vrd_u:
                            espacamento_max = min(0.6 * d, 30)
                    else:
                            espacamento_max = min(0.6 * d, 20)

                    if espacamento > espacamento_max:
                        espacamento = espacamento_max

                    mensagem_estribo = '1\u03A6{}mm c/ {}cm'.format(str(phi_estribo*10).replace('.', ','), espacamento)
                    armadura_df.loc[index, 'espacamento_estribo'] = espacamento
                    armadura_df.loc[index, 'mensagem_estribo'] = mensagem_estribo
                    armadura_df.loc[index, 'phi_estribo'] = phi_estribo
                    break

            if Vsd > Vrd_u:
                armadura_df.loc[index, 'biela_comprimida'] = True
            else:
                armadura_df.loc[index, 'biela_comprimida'] = False

        return armadura_df

    @classmethod
    def __estados_limites_servico(cls, armadura_df, largura, altura, fck, inercia, d, tipoCombinacao, classeAgressividade):
        dict_limite_fissuras = {'I': 0.04, 'II': 0.03, 'III': 0.03, 'IV': 0.02}

        fctm = 0.3*fck**(2/3)
        fctk_inf = 0.7 * fctm

        momento_formacao_fissuras = (1.5*fctk_inf*inercia)/(altura/2)
        momento_deformacao_excessiva = (1.5 * fctm * inercia) / (altura / 2)



        return None

    @classmethod
    def __calcula_bitolas(cls, armadura_df, largura, cobrimento, altura):
        armadura_df['detalhamento_tracao'] = None
        armadura_df['detalhamento_compressao'] = None

        for index, row in armadura_df.iterrows():
            phi_estribo = row['phi_estribo']
            list_bitolas = gerador_armaduras(phi_estribo=phi_estribo, list_bws=[largura], cobrimento=cobrimento,
                                             phi_agregado=2.28)
            df_bitolas = pd.DataFrame(list_bitolas)
            if not row['armaduraDupla']:
                area_necessaria = row['Ast']
                opcoes = df_bitolas[df_bitolas['area'] >= area_necessaria]
                opcoes.sort_values(['numero_camadas', 'area'], inplace=True)
                opcoes.drop(['bw'], axis=1, inplace=True)
                opcoes.reset_index(inplace=True)
                opcoes = opcoes.head()
                list_detalhamento_tracao = []
                for index_aux, opcao in opcoes.iterrows():

                    list_bitolas = opcao['list_bitolas_camadas']
                    list_barras = opcao['list_barras_por_camada']

                    espacamento_horizontal = []

                    for bitola, barra in zip(list_bitolas, list_barras):
                        if barra == 0:
                            espacamento_horizontal.append(0)
                        else:
                            espacamento = (largura - 2 * cobrimento - 2 * 0.5 - barra * bitola) / (barra - 1)
                            espacamento_horizontal.append(espacamento)

                    cg_armadura_tracao = opcao['cg_armadura']
                    if row['Msd'] > 0:
                        cg_armadura_tracao = [altura - i if i != 0 else 0 for i in cg_armadura_tracao]

                    mensagens = []
                    for barra, diametro in zip(opcao['list_barras_por_camada'],
                                               opcao['list_bitolas_camadas']):
                        if barra == 0 or diametro == 0:
                            continue
                        else:
                            mensagem = '{}\u03A6'.format(barra)
                            mensagem += ' {:s} mm'.format(str(diametro * 10).replace('.', ','))
                            mensagens.append(mensagem)

                    mensagem_detalhamento_tracao = ' + '.join(mensagens)

                    Ast_efe = str(round(opcao['area'], 2)).replace('.', ',')

                    detalhamento_tracao = {'id': index_aux, 'Ast_efe': Ast_efe,'list_bitolas_camadas': list_bitolas,
                                           'list_barras_por_camada': list_barras,
                                           'numero_camadas': opcao['numero_camadas'],
                                           'cg_armadura': cg_armadura_tracao,
                                           'espacamento_horizontal': espacamento_horizontal,
                                           'mensagem_detalhamento_tracao': mensagem_detalhamento_tracao}

                    list_detalhamento_tracao.append(detalhamento_tracao)

                #armadura_df.loc[index, 'detalhamento_tracao'] = json.dumps(detalhamento_tracao,
                #                                                          default=lambda o: int(o) if isinstance(o,
                #                                                                                                  np.int64) else o)

                armadura_df.at[index, 'detalhamento_tracao'] = list_detalhamento_tracao

            else:
                area_necessaria_tracao = row['Ast']
                area_necessaria_compressao = row['Asc']

                opcoes_tracao = df_bitolas[df_bitolas['area'] >= area_necessaria_tracao]
                opcoes_tracao.sort_values(['numero_camadas', 'area'], inplace=True)
                opcoes_tracao.drop(['bw'], axis=1, inplace=True)
                opcoes_tracao.reset_index(inplace=True)
                opcoes_tracao = opcoes_tracao.head()

                list_detalhamento_tracao = []
                for index_aux, opcao_tracao_dupla in opcoes_tracao.iterrows():

                    list_bitolas_tracao = opcao_tracao_dupla['list_bitolas_camadas']
                    list_barras_tracao = opcao_tracao_dupla['list_barras_por_camada']

                    espacamento_horizontal_tracao = []

                    for bitola, barra in zip(list_bitolas_tracao, list_barras_tracao):
                        if barra == 0:
                            espacamento_horizontal_tracao.append(0)
                        else:
                            espacamento = (largura - 2 * cobrimento - 2 * phi_estribo - barra * bitola) / (barra - 1)
                            espacamento_horizontal_tracao.append(espacamento)

                    cg_armadura_tracao = opcao_tracao_dupla.loc['cg_armadura']
                    if row['Msd'] > 0:
                        cg_armadura_tracao = [altura - i if i != 0 else 0 for i in cg_armadura_tracao]

                    #armadura_df.loc[index, 'detalhamento_tracao'] = json.dumps(detalhamento_tracao,
                     #                                                          default=lambda o: int(o) if isinstance(o,
                      #                                                                                                np.int64) else o)

                    mensagens = []
                    for barra, diametro in zip(opcao_tracao_dupla['list_barras_por_camada'],
                                               opcao_tracao_dupla['list_bitolas_camadas']):
                        if barra == 0 or diametro == 0:
                            continue
                        else:
                            mensagem = '{}\u03A6'.format(barra)
                            mensagem += ' {:s} mm'.format(str(diametro * 10).replace('.', ','))
                            mensagens.append(mensagem)
                    mensagem_detalhamento_tracao = ' + '.join(mensagens)

                    Ast_efe = str(round(opcao_tracao_dupla['area'], 2)).replace('.', ',')

                    detalhamento_tracao = {'id': index_aux, 'Ast_efe': Ast_efe,
                                           'list_bitolas_camadas': list_bitolas_tracao,
                                           'list_barras_por_camada': list_barras_tracao,
                                           'numero_camadas': opcao_tracao_dupla['numero_camadas'],
                                           'cg_armadura': cg_armadura_tracao,
                                           'espacamento_horizontal': espacamento_horizontal_tracao,
                                           'mensagem_detalhamento_tracao': mensagem_detalhamento_tracao}

                    list_detalhamento_tracao.append(detalhamento_tracao)

                armadura_df.at[index, 'detalhamento_tracao'] = list_detalhamento_tracao

                opcoes_compressao = df_bitolas[df_bitolas['area'] >= area_necessaria_compressao]
                opcoes_compressao.sort_values(['numero_camadas', 'area'], inplace=True)
                opcoes_compressao.drop(['bw'], axis=1, inplace=True)
                opcoes_compressao.reset_index(inplace=True)
                opcoes_compressao = opcoes_compressao.head()

                list_detalhamento_compressao = []
                for index_aux, opcao_compressao in opcoes_compressao.iterrows():

                    list_bitolas_compressao = opcao_compressao['list_bitolas_camadas']
                    list_barras_compressao = opcao_compressao['list_barras_por_camada']

                    espacamento_horizontal_compressao = []

                    for bitola, barra in zip(list_bitolas_compressao, list_barras_compressao):
                        if barra == 0:
                            espacamento_horizontal_compressao.append(0)
                        else:
                            espacamento = (largura - 2 * cobrimento - 2 * phi_estribo - barra * bitola) / (barra - 1)
                            espacamento_horizontal_compressao.append(espacamento)

                    cg_armadura_compressao = opcao_compressao['cg_armadura']
                    if row['Msd'] < 0:
                        cg_armadura_compressao = [altura - i if i != 0 else 0 for i in cg_armadura_compressao]

                    mensagens = []
                    for barra, diametro in zip(opcao_compressao['list_barras_por_camada'],
                                               opcao_compressao['list_bitolas_camadas']):
                        if barra == 0 or diametro == 0:
                            continue
                        else:
                            mensagem = '{}\u03A6'.format(barra)
                            mensagem += ' {:s} mm'.format(str(diametro * 10).replace('.', ','))
                            mensagens.append(mensagem)
                    mensagem_detalhamento_compressao = ' + '.join(mensagens)

                    Asc_efe = str(round(opcao_compressao['area'], 2)).replace('.', ',')


                    detalhamento_compressao = {'id': index_aux, 'Asc_efe': Asc_efe,
                                           'list_bitolas_camadas': list_bitolas_compressao,
                                           'list_barras_por_camada': list_barras_compressao,
                                           'numero_camadas': opcao_compressao['numero_camadas'],
                                           'cg_armadura': cg_armadura_compressao,
                                           'espacamento_horizontal': espacamento_horizontal_compressao,
                                           'mensagem_detalhamento_compressao': mensagem_detalhamento_compressao}

                    list_detalhamento_compressao.append(detalhamento_compressao)

                armadura_df.at[index, 'detalhamento_compressao'] = list_detalhamento_compressao

                    #armadura_df.loc[index, 'Asc_efe'] = opcao_compressao.loc[0, 'area']
                    # armadura_df.loc[index, 'detalhamento_compressao'] = json.dumps(detalhamento_compressao,
                    #                                                              default=lambda o: int(o) if isinstance(o,
                    #                                                                                                      np.int64) else o)
                    #
                    #armadura_df.loc[index, 'mensagem_detalhamento_tracao'] = mensagem_detalhamento_tracao
                    #armadura_df.loc[index, 'mensagem_detalhamento_compressao'] = mensagem_detalhamento_compressao


        return armadura_df
