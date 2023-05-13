import {Pencil} from "phosphor-react";
import {useForm, useFieldArray} from "react-hook-form";
import {zodResolver} from "@hookform/resolvers/zod";
import axios from "axios";
import * as zod from "zod";
import {useState} from "react";
import Divider from '@mui/material/Divider';

import {
    FormContainer,
    HomeContainer,
    CalculateButton,
    BasicInput, TramosButton,
} from "./styles";

const newCycleFormValidationSchema = zod.object({
    comprimento: zod.string().min(0, "Informe o comprimento total da viga"),
    largura: zod.string().min(0, "Informe a largura da viga"),
    altura: zod.string().min(0, "Informe a altura da viga"),
    classeConcreto: zod.string().min(2, "Selecione a classe do concreto"),
    classeAgressividade: zod.string().min(2, "Selecione a classe de agressividade ambiental"),
    combAcoes: zod.string().min(2, "Selecione o tipo de combinação das ações"),
    tramos: zod.array(zod.object({
        numero: zod.string().min(1, "Número do tramo obrigatório"),
        comprimento: zod.string().min(1, "Comprimento do tramo obrigatório")
    })),
    cargas: zod.array(zod.object({
        tipo: zod.string().min(1, "Tipo da carga obrigatório"),
        intensidade: zod.string().min(1, "Intensidade da carga obrigatória"),
        posiInicial: zod.string().min(1, "Posição inicial da carga obrigatória"),
        posiFinal: zod.optional(zod.string())
    })),
});

type NewCycleFormData = zod.infer<typeof newCycleFormValidationSchema>

export function Home() {
    const {register, handleSubmit, watch, reset, setValue, control} = useForm<NewCycleFormData>({
        resolver: zodResolver(newCycleFormValidationSchema),
        defaultValues: {
            comprimento: '',
            largura: '',
            altura: '',
            classeConcreto: "",
            classeAgressividade: "",
            tramos: [{numero: "", comprimento: ""}],
            cargas: [{tipo: "", intensidade: "", posiInicial: "", posiFinal: ""}],
        },
    });
    const [open, setOpen] = useState(false);
    const [tipoCargaAtual, setTipoCargaAtual] = useState(["Concentrada"])
    const handleOpen = () => setOpen(true);
    const handleClose = () => setOpen(false);

    const {fields: fieldsTramos, append: appendTramos, remove: removeTramos} = useFieldArray({
        control,
        name: "tramos",
    });

    const {fields: fieldsCargas, append: appendCargas, remove: removeCargas} = useFieldArray({
        control,
        name: "cargas",
    });

    function handleSendNewCalculation(data: NewCycleFormData) {
        console.log(data);
        reset();
    }

    function addNewTramo() {
        appendTramos({numero: "", comprimento: ""});
    }

    function addNewCarga() {
        appendCargas({tipo: "", intensidade: "", posiInicial: "", posiFinal: ""});
        setTipoCargaAtual([...tipoCargaAtual, "Concentrada"])
    }

    function handleTipoCargaAtual(event: any, index: number) {
        const newCargaAtual = tipoCargaAtual.map((c, i) => {
            if (i === index) {
                return event.target.value;
            } else {
                return c;
            }
        });
        setTipoCargaAtual(newCargaAtual);
    }

    const classeConcretoArray = ["C20", "C25", "C30", "C35", "C40", "C45", "C50"];
    const combinacaoAcoesArray = ["Normais", "Especiais ou de Construção", "Excepcionais"];
    const agressividadeAmbArray = ["I", "II", "III", "IV"];

    const handleCreateNewRequest = async (data: NewCycleFormData) => {
        console.log('entrou')
        axios.defaults.baseURL = 'http://0.0.0.0:8999';
        const response = await axios
            .post("/api/calculate/", data)
            .then(() => {
                reset();
                console.log("Sucesso")
            })
            .catch((err: any) => {
                console.log(err)
            })
    }

    return (
        <HomeContainer>
            <form onSubmit={handleSubmit(handleSendNewCalculation)}>
                <FormContainer>
                    <div className={"div-1"}>
                        <div className={"div-2"}>
                            <label htmlFor="comprimento">Comprimento Total da Viga (cm):</label>
                            <BasicInput
                                id="comprimento"
                                type="number"
                                title="Comprimento da viga"
                                alt="Comprimento da viga"
                                placeholder="Digite o comprimento total da viga"
                                {...register("comprimento")}
                            />
                        </div>

                        <div className={"div-2"}>
                            <label htmlFor="comb-acoes">Tipo de Combinação das Ações:</label>
                            <BasicInput
                                id="comb-acoes"
                                type="text"
                                list="combinacao-acoes"
                                placeholder="Selecione o tipo de combinação das ações"
                                {...register("combAcoes")}
                            />
                            <datalist id="combinacao-acoes">
                                {combinacaoAcoesArray.map((comp) => <option key={comp} value={comp}/>)}
                            </datalist>
                        </div>

                    </div>

                    <div className={"div-1"}>
                        <div className={"div-2"}>
                            <label htmlFor="largura">Largura da Viga (cm): </label>
                            <BasicInput
                                id="largura"
                                type="number"
                                placeholder="Digite a largura da viga"
                                {...register("largura")}
                            />
                        </div>
                        <div className={"div-2"}>
                            <label htmlFor="altura">Altura da Viga (cm): </label>
                            <BasicInput
                                id="altura"
                                type="number"
                                placeholder="Digite a altura da viga"
                                {...register("altura")}
                            />
                        </div>
                    </div>

                    <div className={"div-1"}>
                        <div className={"div-2"}>
                            <label htmlFor="classeConcreto">Classe do Concreto:</label>
                            <BasicInput
                                id="classeConcreto"
                                type="text"
                                placeholder="Selecione a classe do concreto"
                                list="classe-concreto"
                                {...register("classeConcreto")}
                            />
                            <datalist id="classe-concreto">
                                {classeConcretoArray.map((classe) => <option value={classe}/>)}
                            </datalist>
                        </div>
                        <div className={"div-2"}>
                            <label htmlFor="classeAgressividade">Classe de Agressividade Ambiental:</label>
                            <BasicInput
                                id="classeAgressividade"
                                type="text"
                                placeholder="Selecione a classe de agressividade ambiental"
                                list="agressividade-amb"
                                {...register("classeAgressividade")}
                            />
                            <datalist id="agressividade-amb">
                                {agressividadeAmbArray.map((agressividade) => <option key={agressividade}
                                                                                      value={agressividade}/>)}
                            </datalist>
                        </div>
                    </div>

                    <div className={"div-1 start"}>
                        <div className={"div-2 inicial"}>
                            <div className={"div-1"}>
                                <label htmlFor="" className={"tramos-label"}>
                                    Tramos:
                                </label>
                                <TramosButton onClick={addNewTramo} type="button">
                                    Adicionar
                                </TramosButton>
                            </div>
                            {fieldsTramos.map((field, index) => {
                                    return (
                                        <div>
                                            <div className={"div-1"} key={field.id}>
                                                <BasicInput
                                                    type="text"
                                                    placeholder="Número do tramo"
                                                    {...register(`tramos.${index}.numero`)}
                                                />

                                                <BasicInput
                                                    type="text"
                                                    placeholder="Comprimento em cm"
                                                    {...register(`tramos.${index}.comprimento`)}
                                                />
                                            </div>
                                            {(fieldsTramos.length > 1 && index < (fieldsTramos.length - 1)) &&
                                                <Divider variant="middle" color={'#7C7C8A'}
                                                         sx={{marginTop: "1rem", marginBottom: "1rem"}}/>}
                                        </div>
                                    );
                                }
                            )
                            }
                        </div>

                        <div className={"div-2"}>
                            <div className={"div-1"}>
                                <label htmlFor="" className={"cargas-label"}>
                                    Cargas:
                                </label>
                                <TramosButton onClick={addNewCarga} type="button">
                                    Adicionar
                                </TramosButton>
                            </div>
                            {fieldsCargas.map((field, index) => {
                                    return (
                                        <div>
                                            <div className={"div-1"} key={field.id}>
                                                <BasicInput
                                                    type="text"
                                                    placeholder="Tipo"
                                                    list="tipo-carga"
                                                    title="Tipo da carga"
                                                    alt="Tipo da carga"
                                                    {...register(`cargas.${index}.tipo`)}
                                                    onChange={(event) => handleTipoCargaAtual(event, index)}
                                                />
                                                <datalist id="tipo-carga">
                                                    <option value={"Concentrada"}/>
                                                    <option value={"Distribuída"}/>
                                                </datalist>
                                                <BasicInput
                                                    type="text"
                                                    placeholder="Intensidade"
                                                    title="Valores em kN ou kN/cm"
                                                    alt="Valores em kN ou kN/cm"
                                                    {...register(`cargas.${index}.intensidade`)}
                                                />
                                            </div>
                                            <div className={"div-1"} key={field.intensidade}>
                                                <BasicInput
                                                    type="text"
                                                    placeholder="Posição inicial em cm"
                                                    title="Posição inicial da carga"
                                                    alt="Posição inicial da carga"
                                                    {...register(`cargas.${index}.posiInicial`)}
                                                />
                                                {(tipoCargaAtual[index] == "Distribuída") && (
                                                    <BasicInput
                                                        type="text"
                                                        placeholder="Posição final em cm"
                                                        title="Posição final da carga"
                                                        alt="Posição final da carga"
                                                        {...register(`cargas.${index}.posiFinal`)}
                                                    />
                                                )}
                                            </div>
                                            {(fieldsCargas.length > 1 && index < (fieldsCargas.length - 1)) &&
                                                <Divider variant="middle" color={'#7C7C8A'}
                                                         sx={{marginTop: "1rem", marginBottom: "1rem"}}/>}

                                        </div>
                                    )
                                }
                            )
                            }
                        </div>
                    </div>

                </FormContainer>

                <CalculateButton type="submit" onClick={handleSubmit(handleCreateNewRequest)}>
                    <Pencil size={24}/>
                    Dimensionar e Detalhar
                </CalculateButton>
            </form>
        </HomeContainer>

    );
}
