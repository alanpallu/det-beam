import {HistoryContainer, HistoryList, Status, FiguresContainer} from "./styles";
import {useLocation} from "react-router-dom";
import Divider from "@mui/material/Divider";
import {Stage, Layer, Rect, Circle, Line, Text} from "react-konva";
import {useState, useEffect, useRef} from "react";
import {IconButton} from "@mui/material";
import DrawIcon from "@mui/icons-material/Draw";
import Tooltip from "@mui/material/Tooltip";

export function Results() {
    const location = useLocation();
    const [numBarsInEachRow, setNumBarsInEachRow] = useState([]);
    const [barDiameterInEachRow, setBarDiameterInEachRow] = useState([]);
    const [verticalPositionOfEachRow, setVerticalPositionOfEachRow] = useState([]);
    const [horizontalSpacingInEachRow, setHorizontalSpacingInEachRow] = useState([]);
    const [height, setHeight] = useState(0);
    const [width, setWidth] = useState(0);
    const [length, setLength] = useState(0);
    const [cobrimento, setCobrimento] = useState(0);
    const [supportPositions, setSupportPositions] = useState([]);
    const [pointPositions, setPointPositions] = useState([]);
    const [rowDetail, setRowDetail] = useState({});
    const [ponto, setPonto] = useState(0)
    const myRef = useRef(null);

    // @ts-ignore
    const estrutura = location.state ? location.state.prevState.structure : null;
    // @ts-ignore
    const momento = location.state ? location.state.prevState.moment : null;
    // @ts-ignore
    const cortante = location.state ? location.state.prevState.shear : null;
    // @ts-ignore
    const rows = location.state ? location.state.data.slice(0, -1) : [];
    // @ts-ignore
    const row_infos = location.state ? location.state.data.slice(-1) : [];

    console.log(rows)

    useEffect(() => {
        if (row_infos.length > 0) {
            setHeight(row_infos[0]["altura"]);
            setWidth(row_infos[0]["largura"]);
            setCobrimento(row_infos[0]["cobrimento"]);
            setSupportPositions(row_infos[0]["coordenadas_apoios_desenho"]);
            setPointPositions(row_infos[0]["coordenadas_desenho"]);
            setLength(row_infos[0]["comprimento"]);
        }
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }, []);

    const drawFigure = (row: any, ponto: any) => {
        setPonto(ponto+1)
        setRowDetail(row);
        setNumBarsInEachRow(row["detalhamento_tracao"].list_barras_por_camada);
        setBarDiameterInEachRow(row["detalhamento_tracao"].list_bitolas_camadas);
        setVerticalPositionOfEachRow(row["detalhamento_tracao"].cg_armadura);
        setHorizontalSpacingInEachRow(row["detalhamento_tracao"].espacamento_horizontal);
        executeScroll()
    };

    // @ts-ignore
    const executeScroll = () => myRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });

    const maxWidth = window.innerWidth;



// Choose the smaller scaling factor to ensure the entire drawing fits on the page


    const scale = 8; // Scaling factor
    const measurementLineLength = 15;
    const offset = 10;

    const beamLengthPixels = length;

    const scaleFactorWidth = maxWidth / beamLengthPixels;

    const scaleFactor = scaleFactorWidth * 0.7;

    const beamYPosition = 50; // Position on Y axis for the beam to draw
    const supportHeight = 20; // Define the height of the triangle support
    const pointRadius = 7; // Radius for the points
    const fontSize = 12; // Font size for the text

    const supportWidth = supportHeight * Math.sqrt(3) / 2;
    const padding = 20;

    return (
        <HistoryContainer>
            <h1>Resultados</h1>
            <HistoryList>
                <table>
                    <thead>
                    <tr>
                        <th>Ponto</th>
                        <th>Coord. (cm)</th>
                        <th>Msd (kN.cm)</th>
                        <th>Vsd (kN)</th>
                        <th>Ast (cm²)</th>
                        <th>nΦ</th>
                        <th>Ast Efe (cm²)</th>
                        <th>Armadura long.</th>
                        <th>Asc (cm²)</th>
                        <th>nΦ</th>
                        <th>Asc Efe (cm²)</th>
                        <th>Verificação Biela Comprimida</th>
                        <th>Estribos</th>
                        <th>ELS</th>
                        <th>Ação</th>
                    </tr>
                    </thead>
                    <tbody>
                    {rows.map((row: any, index: number) => (
                        <tr>
                            <td>{index + 1}</td>
                            <td>{row.coord}</td>
                            <td>{row.Msd}</td>
                            <td>{row.Vsd}</td>
                            <td>{row.Ast}</td>
                            <td>{row.mensagem_detalhamento_tracao}</td>
                            <td>{row.Ast_efe}</td>
                            <td>{row.armaduraDupla ? "Dupla" : "Simples"}</td>
                            <td>{row.Asc ? row.Asc : "-"}</td>
                            <td>{row.mensagem_detalhamento_compressao ? row.mensagem_detalhamento_compressao : "-"}</td>
                            <td>{row.Asc_efe ? row.Asc_efe : "-"}</td>
                            <td>{row.biela_comprimida ? <Status statusColor="red">Não passou</Status> : <Status statusColor="green">Passou</Status>}</td>
                            <td>{row.mensagem_estribo}</td>
                            <td>
                                <Status statusColor="red">Não passou</Status>
                            </td>
                            <td>
                                <Tooltip title="Detalhar">
                                    <IconButton aria-label="delete" onClick={() => drawFigure(row, index)}>
                                        <DrawIcon sx={{color: "#00875F"}}/>
                                    </IconButton>
                                </Tooltip></td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </HistoryList>
            <br/><br/>

            {row_infos.length > 0 ? (
                <div style={{
                    width: "100%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexDirection: "column",
                    gap: "1rem"
                }} ref={myRef}>
                    <h2>Esquema dos Pontos na Viga</h2>
                    <Stage width={(length + 2 * supportWidth + 2 * padding) * scaleFactor}
                           height={beamYPosition + supportHeight * scaleFactor * 2}>
                        <Layer>
                            {/* Draw the beam */}
                            <Line
                                points={[(supportWidth + padding) * scaleFactor, beamYPosition, (length + supportWidth + padding) * scaleFactor, beamYPosition]}
                                stroke="white"
                                strokeWidth={5 * scaleFactor} // Scale the stroke width as well
                            />

                            {/* Draw the supports */}
                            {supportPositions.map((supportPosition: any, index: any) => (
                                <Line
                                    key={index}  // Unique key for each support
                                    points={[
                                        (supportPosition + supportWidth + padding) * scaleFactor, beamYPosition,
                                        ((supportPosition + supportWidth + padding) * scaleFactor) - (supportHeight * scaleFactor), beamYPosition + supportHeight * scaleFactor,
                                        ((supportPosition + supportWidth + padding) * scaleFactor) + (supportHeight * scaleFactor), beamYPosition + supportHeight * scaleFactor,
                                    ]}
                                    closed
                                    stroke="white"
                                    fill="white"
                                />
                            ))}

                            {/* Draw the points */}
                            {pointPositions.map((pointPosition: any, index: any) => {
                                const text = `${index + 1}`;
                                const textWidth = fontSize * text.length; // estimate the text width

                                return (
                                    <>
                                        <Circle
                                            key={index}  // Unique key for each point
                                            radius={pointRadius}
                                            fill="white"
                                            x={(pointPosition + supportWidth + padding) * scaleFactor}
                                            y={beamYPosition}
                                        />
                                        <Text
                                            text={text}
                                            fontSize={fontSize}
                                            fill="black"
                                            x={(pointPosition + supportWidth + padding) * scaleFactor - textWidth / 4}
                                            y={beamYPosition - fontSize / 2}
                                        />
                                    </>
                                );
                            })}
                        </Layer>
                    </Stage>
                    <Divider
                        variant="middle"
                        color={"#7C7C8A"}
                        sx={{width: "100%", marginTop: "1rem", marginBottom: "1rem"}}
                    />
                </div>) : <div></div>
            }

            <br/><br/>
            {Object.keys(rowDetail).length != 0 ?
                <div style={{
                    width: "100%",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexDirection: "column",
                    gap: "2rem"
                }}>
                    <h2>Detalhamento da Armadura na Seção {ponto}</h2>
                    <Stage width={width * scale * 1.2} height={height * scale * 1.2}>
                        <Layer>

                            <Rect
                                width={width * scale}
                                height={height * scale}
                                fill="gray"
                                stroke="white"
                                strokeWidth={2} // Scale the stroke width as well
                            />
                            <Line
                                points={[0, 0, width * scale, 0]}
                                stroke='#00B37E'
                                strokeWidth={2}
                                y={(height) * scale + offset}
                            />
                            <Text
                                text={`${width}`}
                                fill='#00B37E'
                                x={width * scale / 2}
                                y={(height) * scale + 5 + offset}
                            />

                            <Line
                                points={[0, height * scale, 0, 0]}
                                stroke='#00B37E'
                                strokeWidth={2}
                                y={0}
                                x={(width) * scale + offset}
                            />
                            <Text
                                text={`${height}`}
                                fill='#00B37E'
                                x={width * scale + offset + 5}
                                y={(height) * scale / 2}
                            />

                            <Rect
                                x={(cobrimento)*scale}
                                y={(cobrimento)*scale}
                                width={(width-2*cobrimento)*scale}
                                height={(height-2*cobrimento)*scale}
                                stroke="white"
                                strokeWidth={0.5*scale}
                            />
                            {numBarsInEachRow.map((numBars: any, rowIndex: any) => {
                                let position = (cobrimento + 0.5) * scale;  // Initialize position for the first bar in the row
                                const barDiameter = barDiameterInEachRow[rowIndex] * scale; // Scale the bar diameter
                                const verticalPosition = verticalPositionOfEachRow[rowIndex] * scale;
                                const horizontalSpacing = horizontalSpacingInEachRow[rowIndex] * scale; // Scale the horizontal spacing

                                return (
                                    [...Array(numBars)].map((_, barIndex) => {
                                        // Calculate position of the bar
                                        const barPosition = position;
                                        // Update position for the next bar
                                        position += barDiameter + horizontalSpacing;

                                        return (
                                            <Circle
                                                key={`${rowIndex}-${barIndex}`}  // Unique key for each bar
                                                radius={barDiameter / 2}
                                                fill="white"
                                                x={barPosition + barDiameter / 2}
                                                y={verticalPosition}
                                            />
                                        );
                                    })
                                );
                            })}
                            {numBarsInEachRow.map((numBars: any, rowIndex: any) => {
                                let position = (cobrimento + 0.5) * scale;  // Initialize position for the first bar in the row
                                const barDiameter = barDiameterInEachRow[rowIndex] * scale; // Scale the bar diameter
                                const verticalPosition = verticalPositionOfEachRow[rowIndex] * scale;
                                const horizontalSpacing = horizontalSpacingInEachRow[rowIndex] * scale; // Scale the horizontal spacing

                                // return (
                                //     <div>
                                //         <Line
                                //             points={[0, height * scale, 0, 0]}
                                //             stroke='white'
                                //             strokeWidth={2}
                                //             y={0}
                                //             x={(width) * scale + offset}
                                //         />
                                //         <Text
                                //             text={`${height}`}
                                //             fill='white'
                                //             x={width * scale + offset + 5}
                                //             y={(height) * scale / 2}
                                //         />
                                //     </div>
                                // );
                            })}
                        </Layer>
                    </Stage>
                    <Divider
                        variant="middle"
                        color={"#7C7C8A"}
                        sx={{width: "100%", marginTop: "1rem", marginBottom: "1rem"}}
                    />
                </div>
                : <div></div>}

            <br/><br/>
            <br/><br/>

            <FiguresContainer>

                {estrutura &&
                    <div className="figure-div">
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
                    <div className="figure-div">
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
                    <div className="figure-div">
                        <h2>Diagrama de Força Cortante:</h2>
                        <br/>
                        <img src={cortante} alt="Shear Force Plot"/>
                    </div>
                }
            </FiguresContainer>
        </HistoryContainer>
    );
}
