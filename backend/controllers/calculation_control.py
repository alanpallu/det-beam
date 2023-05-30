from models.calculation_model import FormInput
import pandas as pd
from helpers.esforcos_solicitantes import get_esforcos
from helpers.tabelas_kc_ks import select_all
from helpers.gerador_armaduras import gerador_armaduras


class CalculatorControl:

    @classmethod
    def perform_calculations(cls, dados: FormInput) -> str:
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
        cargas = dados.cargas

        tabela_kc_ks = select_all()

        cobrimento = dict_cobrimento[classeAgressividade]
        d_linha = cobrimento - 0.63 - 0.8
        d = round(altura - d_linha, 0)

        esforcos, momentos, cortantes = cls.__esforcos_solicitantes(cargas=cargas, tramos=tramos, h=altura, b=largura,
                                                                    concreto=classeConcreto)

        momento_limite = cls.__momento_limite(d=d, classe_concreto=classeConcreto,
                                              b=largura, tabela_kc_ks=tabela_kc_ks)

        momento_minimo = 0.8 * (largura * altura ** 2) / 6 * (1.3 * (0.3 * fck ** (2 / 3)) / 10)

        armadura_df = cls.__armaduras(esforcos=esforcos, gama_f=gama_f, largura=largura, d=d, d_linha=d_linha, tabela_kc_ks=tabela_kc_ks,
                                      momento_limite=momento_limite, classe_concreto=classeConcreto, altura=altura)

        armadura_com_bitolas = cls.__calcula_bitolas(armadura_df=armadura_df, largura=float(largura), cobrimento=float(cobrimento), altura=float(altura))

        return armadura_df.to_json(orient='records')

    @classmethod
    def __esforcos_solicitantes(cls, cargas, tramos, h, b, concreto):
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
                if elemento_id_final != elemento_id_inicial:  # todo checar essa logica para muitos tramos
                    cargas_dist_list.append([elemento_id_final, carga['intensidade']])
                dif = elemento_id_final - elemento_id_inicial
                if dif > 1:
                    for i in range(dif):
                        elemento_id = elemento_id_inicial + i
                        cargas_dist_list.append([elemento_id, carga['intensidade']])
            elif carga['tipo'] == 'Concentrada':
                node_id = coordenadas_list.index([posicao_inicial, 0]) + 1
                cargas_conc_list.append([node_id, carga['intensidade']])

        results, moment_list, shear_list = get_esforcos(h, b, concreto, coordenadas_list, node_ids_fixed,
                                                        cargas_conc_list, cargas_dist_list)

        return results, moment_list, shear_list

    @classmethod
    def __momento_limite(cls, b, d, classe_concreto, tabela_kc_ks):
        kc_lim = tabela_kc_ks.loc[0.45, classe_concreto]

        momento_limite = b * d ** 2 / kc_lim
        return momento_limite

    @classmethod
    def __armaduras(cls, esforcos, gama_f, largura, d, tabela_kc_ks, momento_limite, classe_concreto, d_linha, altura):
        armadura_df = pd.DataFrame(
            columns=['Msk', 'Msd', 'Bx_lim'])  # , 'kc', 'Bx', 'ks', 'Ast', 'armadura', 'Ast_efe'])

        ksc_dict = {
            0.05: 0.023,
            0.1: 0.023,
            0.15: 0.023,
            0.2: 0.031,
            0.25: 0.052
        }

        for item in esforcos:
            momentos = item['M']
            momento_inicial = -momentos[0]
            momento_final = -momentos[-1]
            momento_min = -item['Mmax']
            momento_max = -item['Mmin']

            if momento_inicial > 1e-10 or momento_inicial < -1e-10:
                line_1 = pd.DataFrame({'Msk': [round(momento_inicial, 6)], 'Msd': [momento_inicial * gama_f], 'Bx_lim': [0.45]})
                armadura_df = pd.concat([armadura_df, line_1], ignore_index=True)

            if momento_final > 1e-10 or momento_final < -1e-10:
                line_2 = pd.DataFrame({'Msk': [round(momento_final, 6)], 'Msd': [momento_final * gama_f], 'Bx_lim': [0.45]})
                armadura_df = pd.concat([armadura_df, line_2], ignore_index=True)

            if momento_min > 1e-10 or momento_min < -1e-10:
                line_3 = pd.DataFrame({'Msk': [round(momento_min, 6)], 'Msd': [momento_min * gama_f], 'Bx_lim': [0.45]})
                armadura_df = pd.concat([armadura_df, line_3], ignore_index=True)

            if momento_max > 1e-10 or momento_max < -1e-10:
                line_4 = pd.DataFrame({'Msk': [round(momento_max, 6)], 'Msd': [momento_max * gama_f], 'Bx_lim': [0.45]})
                armadura_df = pd.concat([armadura_df, line_4], ignore_index=True)

        armadura_df = armadura_df.groupby(['Msk']).agg({'Msd': 'first', 'Bx_lim': 'first'}).reset_index()
        for index, row in armadura_df.iterrows():
            if row['Msd'] > momento_limite:
                armadura_df.loc[index, 'armaduraDupla'] = True
                Msd_1 = momento_limite
                ks_lim = tabela_kc_ks.loc[0.45, 'CA50']
                Ast_1 = ks_lim * Msd_1 / d
                Msd_2 = row['Msd'] - Msd_1
                Ast_2 = 0.023 * Msd_2 / (d - d_linha)
                d_linha_h = d_linha / altura
                ksc = min(ksc_dict, key=lambda x: abs(ksc_dict[x] - d_linha_h))
                Asc = ksc * Msd_2 / (d - d_linha)
                armadura_df.loc[index, 'Ast_1'] = Ast_1
                armadura_df.loc[index, 'Ast_2'] = Ast_2
                armadura_df.loc[index, 'Asc'] = Asc
            else:
                armadura_df.loc[index, 'armaduraDupla'] = False
                kc = largura * d**2 / row['Msd']
                armadura_df.loc[index, 'kc'] = kc
                Bx = (tabela_kc_ks[classe_concreto] - kc).abs().idxmin()
                armadura_df.loc[index, 'Bx'] = Bx
                ks = tabela_kc_ks.loc[Bx, 'CA50']
                armadura_df.loc[index, 'ks'] = ks
                armadura_df.loc[index, 'Ast'] = row['Msd'] * ks / d

        if altura > 60: #tem armadura de pele
            Ac = largura * altura
            A_pele_min = 0.001 * Ac
            armadura_df['A_pele_min'] = A_pele_min
            armadura_df['A_pele_espac_min'] = min(20, int(d/3), int(15 * 1.6))

        return armadura_df

    @classmethod
    def __calcula_bitolas(cls, armadura_df, largura, cobrimento, altura):
        list_bitolas = gerador_armaduras(phi_estribo=0.5, list_bws=[largura], cobrimento=cobrimento, phi_agregado=2.28)
        df_bitolas = pd.DataFrame(list_bitolas)
        for index, row in armadura_df.iterrows():
            print("faz algo")

        return None


if __name__ == '__main__':
    res = CalculatorControl.__momento_limite(20, 60, 'I', 'C30')
    print(res)
