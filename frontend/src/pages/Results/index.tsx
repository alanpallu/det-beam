import {HistoryContainer, HistoryList, Status, FiguresContainer} from "./styles";
import {useLocation} from "react-router-dom";
import Divider from "@mui/material/Divider";

export function Results() {
    const location = useLocation();

    // @ts-ignore
    const estrutura = location.state ? location.state.structure : null;
    // @ts-ignore
    const momento = location.state ? location.state.moment : null;
    // @ts-ignore
    const cortante = location.state ? location.state.shear : null;


    return (
        <HistoryContainer>
            <h1>Resultados</h1>

            <HistoryList>
                <table>
                    <thead>
                    <tr>
                        <th>Coordenada</th>
                        <th>Aréa de aço armadura longitudinal</th>
                        <th>Detalhamento</th>
                        <th>ELS</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>0</td>
                        <td>2,5</td>
                        <td></td>
                        <td>
                            <Status statusColor="green">Passou</Status>
                        </td>
                    </tr>
                    <tr>
                        <td>1</td>
                        <td>5</td>
                        <td></td>
                        <td>
                            <Status statusColor="red">Não passou</Status>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </HistoryList>
            <br/><br/>
            <FiguresContainer>

                {estrutura &&
                    <div>
                        <h2>Estrutura e Carregamentos:</h2>
                        <br/>
                        <img src={estrutura} alt="Structure Plot"/>
                        <Divider
                            variant="middle"
                            color={"#7C7C8A"}
                            sx={{width: "100%", marginTop: "1rem", marginBottom: "1rem"}}
                        />
                    </div>
                }

                {momento &&
                    <div>
                        <h2>Diagrama de Momento Fletor:</h2>
                        <br/>
                        <img src={momento} alt="Bending Moment Plot"/>
                        <Divider
                            variant="middle"
                            color={"#7C7C8A"}
                            sx={{width: "100%", marginTop: "1rem", marginBottom: "1rem"}}
                        />
                    </div>
                }

                {cortante &&
                    <div>
                        <h2>Diagrama de Força Cortante:</h2>
                        <br/>
                        <img src={cortante} alt="Shear Force Plot"/>
                    </div>
                }
            </FiguresContainer>
        </HistoryContainer>
    );
}
