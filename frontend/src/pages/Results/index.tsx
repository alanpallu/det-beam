import {HistoryContainer, HistoryList, Status, FiguresContainer} from "./styles";
import {useLocation} from "react-router-dom";
import Divider from "@mui/material/Divider";
import {Stage, Layer, Rect, Circle, Line, Text} from "react-konva";
import {useState, useEffect, useRef} from "react";
import {IconButton} from "@mui/material";
import DrawIcon from "@mui/icons-material/Draw";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";

export function Results() {
    const location = useLocation();
    const [numBarsInEachRow, setNumBarsInEachRow] = useState([]);
    const [barDiameterInEachRow, setBarDiameterInEachRow] = useState([]);
    const [verticalPositionOfEachRow, setVerticalPositionOfEachRow] = useState([]);
    const [horizontalSpacingInEachRow, setHorizontalSpacingInEachRow] = useState([]);

    const [numBarsInEachRowCompressao, setNumBarsInEachRowCompressao] = useState([]);
    const [barDiameterInEachRowCompressao, setBarDiameterInEachRowCompressao] = useState([]);
    const [verticalPositionOfEachRowCompressao, setVerticalPositionOfEachRowCompressao] = useState([]);
    const [horizontalSpacingInEachRowCompressao, setHorizontalSpacingInEachRowCompressao] = useState([]);

    const [height, setHeight] = useState(0);
    const [width, setWidth] = useState(0);
    const [length, setLength] = useState(0);
    const [cobrimento, setCobrimento] = useState(0);
    const [supportPositions, setSupportPositions] = useState([]);
    const [pointPositions, setPointPositions] = useState([]);
    const [rowDetail, setRowDetail] = useState({});
    const [rowDetailCompressao, setRowDetailCompressao] = useState({});
    const [ponto, setPonto] = useState(0);
    const [opcoesDetalhamentoTracao, setOpcoesDetalhamentoTracao] = useState([])
    const [opcoesDetalhamentoCompressao, setOpcoesDetalhamentoCompressao] = useState([]);
    const [diametroEstribo, setDiametroEstribo] = useState(0);

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

    useEffect(() => {
        if (row_infos.length > 0) {
            setHeight(row_infos[0]["altura"]);
            setWidth(row_infos[0]["largura"]);
            setCobrimento(row_infos[0]["cobrimento"]);
            setSupportPositions(row_infos[0]["coordenadas_apoios_desenho"]);
            setPointPositions(row_infos[0]["coordenadas_desenho"]);
            setLength(row_infos[0]["comprimento"]);
        }

        // @ts-ignore
        let arrayTracao = []
        // @ts-ignore
        let arrayCompressao = []
        rows.map((row: any) => {
            arrayTracao.push(row['detalhamento_tracao'][0])
        })
        // @ts-ignore

        setOpcoesDetalhamentoTracao(arrayTracao)

        if (rows.length > 0) {
            rows.map((row: any) => {
                // @ts-ignore
                if (row.detalhamento_compressao !== null && rows.some(dict => dict.hasOwnProperty('detalhamento_compressao'))) {
                    arrayCompressao.push(row['detalhamento_compressao'][0])
                } else {
                    arrayCompressao.push({})
                }
            })
            // @ts-ignore
            setOpcoesDetalhamentoCompressao(arrayCompressao)

        }

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }, []);

    const drawFigure = (index: any) => {
        setPonto(index + 1);
        setDiametroEstribo(rows[index]['phi_estribo'])
        let row = opcoesDetalhamentoTracao[index]
        setRowDetail(row);
        setNumBarsInEachRow(row['list_barras_por_camada']);
        setBarDiameterInEachRow(row['list_bitolas_camadas']);
        setVerticalPositionOfEachRow(row['cg_armadura']);
        setHorizontalSpacingInEachRow(row['espacamento_horizontal']);

        if (opcoesDetalhamentoTracao.length > 0) {
            let row_compressao = opcoesDetalhamentoCompressao[index]
            if (Object.keys(row_compressao).length != 0) {
                setRowDetailCompressao(row_compressao)
                setNumBarsInEachRowCompressao(row_compressao['list_barras_por_camada']);
                setBarDiameterInEachRowCompressao(row_compressao['list_bitolas_camadas']);
                setVerticalPositionOfEachRowCompressao(row_compressao['cg_armadura']);
                setHorizontalSpacingInEachRowCompressao(row_compressao['espacamento_horizontal']);
            }
            else {
                setRowDetailCompressao({})
                setNumBarsInEachRowCompressao([]);
                setBarDiameterInEachRowCompressao([]);
                setVerticalPositionOfEachRowCompressao([]);
                setHorizontalSpacingInEachRowCompressao([]);
            }
        }

        executeScroll();
    };

    const handleChangeTracao = (event: any, index: any) => {
        let newIndex = event.target.value
        let newArray = [...opcoesDetalhamentoTracao]
        let newValue = rows[index]['detalhamento_tracao'][newIndex]
        // @ts-ignore
        newArray[index] = newValue
        setOpcoesDetalhamentoTracao(newArray)
    };
    const handleChangeCompressao = (event: any, index: any) => {
        let newIndex = event.target.value
        let newArray = [...opcoesDetalhamentoTracao]
        let newValue = rows[index]['detalhamento_compressao'][newIndex]
        // @ts-ignore
        newArray[index] = newValue
        setOpcoesDetalhamentoCompressao(newArray)
    };


    // @ts-ignore
    const executeScroll = () => myRef.current.scrollIntoView({behavior: "smooth", block: "start"});

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
                        <th>Ação</th>
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
                        <th>Estribos</th>
                        <th>Verificação Biela Comprimida</th>
                        <th>ELS</th>
                    </tr>
                    </thead>
                    <tbody>
                    {rows.map((row: any, index: number) => {
                        return (
                        <tr>
                            <td>
                                <Tooltip title="Detalhar">
                                    <IconButton aria-label="delete" onClick={() => drawFigure(index)}>
                                        <DrawIcon sx={{color: "#00875F"}}/>
                                    </IconButton>
                                </Tooltip></td>
                            <td>{index + 1}</td>
                            <td>{row.coord}</td>
                            <td>{row.Msd}</td>
                            <td>{row.Vsd}</td>
                            <td>{row.Ast}</td>
                            <td>{
                                <Select
                                    onChange={(event) => handleChangeTracao(event, index)}
                                    inputProps={{"aria-label": "Without label"}}
                                    sx={{color: '#C4C4CC', backgroundColor: '#29292E'}}
                                    defaultValue={0}
                                >
                                    <MenuItem value={0}
                                              sx={{color: '#29292E'}}>{row['detalhamento_tracao'][0]['mensagem_detalhamento_tracao']}
                                    </MenuItem>
                                    <MenuItem value={1}
                                              sx={{color: '#29292E'}}>{row['detalhamento_tracao'][1]['mensagem_detalhamento_tracao']}
                                    </MenuItem>
                                    <MenuItem value={2}
                                              sx={{color: '#29292E'}}>{row['detalhamento_tracao'][2]['mensagem_detalhamento_tracao']}
                                    </MenuItem>
                                    <MenuItem value={3}
                                              sx={{color: '#29292E'}}>{row['detalhamento_tracao'][3]['mensagem_detalhamento_tracao']}
                                    </MenuItem>
                                    <MenuItem value={4}
                                              sx={{color: '#29292E'}}>{row['detalhamento_tracao'][4]['mensagem_detalhamento_tracao']}
                                    </MenuItem>
                                </Select>
                            }</td>
                            <td>{opcoesDetalhamentoTracao.length > 0 ? opcoesDetalhamentoTracao[index]['Ast_efe'] : 0}</td>
                            <td>{row.armaduraDupla ? "Dupla" : "Simples"}</td>
                            <td>{(row.Asc && row.Asc != 'nan') ? row.Asc : "-"}</td>
                            <td>{row.detalhamento_compressao ?
                                <Select
                                    onChange={(event) => handleChangeCompressao(event, index)}
                                    inputProps={{"aria-label": "Without label"}}
                                    sx={{color: '#C4C4CC', backgroundColor: '#29292E'}}
                                    defaultValue={0}
                                >
                                    <MenuItem value={0}
                                              sx={{color: '#29292E'}}>{row['detalhamento_compressao'][0]['mensagem_detalhamento_compressao']}
                                    </MenuItem>
                                    <MenuItem value={1}
                                              sx={{color: '#29292E'}}>{row['detalhamento_compressao'][1]['mensagem_detalhamento_compressao']}
                                    </MenuItem>
                                    <MenuItem value={2}
                                              sx={{color: '#29292E'}}>{row['detalhamento_compressao'][2]['mensagem_detalhamento_compressao']}
                                    </MenuItem>
                                    <MenuItem value={3}
                                              sx={{color: '#29292E'}}>{row['detalhamento_compressao'][3]['mensagem_detalhamento_compressao']}
                                    </MenuItem>
                                    <MenuItem value={4}
                                              sx={{color: '#29292E'}}>{row['detalhamento_compressao'][4]['mensagem_detalhamento_compressao']}
                                    </MenuItem>
                                </Select>
                                : "-"}</td>
                            <td>{(row.detalhamento_compressao && opcoesDetalhamentoCompressao.length > 0) ? opcoesDetalhamentoCompressao[index]['Asc_efe'] : "-"}</td>
                            <td>{row.mensagem_estribo}</td>
                            <td>{row.biela_comprimida ? <Status statusColor="red">Não passou</Status> :
                                <Status statusColor="green">Passou</Status>}</td>
                            <td>
                                <Status statusColor="green">Passou</Status>
                            </td>
                        </tr>
                        )
                    })}
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
                    <Stage width={width * scale * 2} height={height * scale * 1.2}>
                        <Layer>
                            <Rect
                                x={width * scale / 2}
                                width={width * scale}
                                height={height * scale}
                                fill="gray"
                                stroke="white"
                                strokeWidth={2} // Scale the stroke width as well
                            />
                            <Line
                                points={[0, 0, width * scale, 0]}
                                stroke="#00B37E"
                                strokeWidth={2}
                                y={(height) * scale + offset}
                                x={width * scale / 2}
                            />
                            <Text
                                text={`${width}`}
                                fill="#00B37E"
                                x={width * scale}
                                y={(height) * scale + 5 + offset}
                            />

                            <Line
                                points={[0, height * scale, 0, 0]}
                                stroke="#00B37E"
                                strokeWidth={2}
                                y={0}
                                x={(width) * scale * 1.5 + offset}
                            />
                            <Text
                                text={`${height}`}
                                fill="#00B37E"
                                x={width * scale * 1.5 + offset + 5}
                                y={(height) * scale  / 2}
                            />

                            <Rect
                                x={width * scale / 2 + (cobrimento+diametroEstribo/2) * scale}
                                y={(cobrimento+diametroEstribo/2) * scale}
                                width={(width - 2 * cobrimento - diametroEstribo) * scale}
                                height={(height - 2 * cobrimento-diametroEstribo) * scale}
                                stroke="white"
                                strokeWidth={diametroEstribo * scale}
                            />
                            {numBarsInEachRow.map((numBars: any, rowIndex: any) => {
                                let position = (cobrimento + diametroEstribo) * scale;  // Initialize position for the first bar in the row
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
                                                x={width * scale / 2 + barPosition + barDiameter / 2}
                                                y={verticalPosition}
                                            />
                                        );
                                    })
                                );
                            })}
                            {numBarsInEachRowCompressao.map((numBars: any, rowIndex: any) => {
                                let positionCompressao = (cobrimento + diametroEstribo) * scale;  // Initialize position for the first bar in the row
                                const barDiameterCompressao = barDiameterInEachRowCompressao[rowIndex] * scale; // Scale the bar diameter
                                const verticalPositionCompressao = verticalPositionOfEachRowCompressao[rowIndex] * scale;
                                const horizontalSpacingCompressao = horizontalSpacingInEachRowCompressao[rowIndex] * scale; // Scale the horizontal spacing

                                return (
                                    [...Array(numBars)].map((_, barIndex) => {
                                        // Calculate position of the bar
                                        const barPositionCompressao = positionCompressao;
                                        // Update position for the next bar
                                        positionCompressao += barDiameterCompressao + horizontalSpacingCompressao;

                                        return (
                                            <Circle
                                                key={`${rowIndex}-${barIndex}`}  // Unique key for each bar
                                                radius={barDiameterCompressao / 2}
                                                fill="white"
                                                x={width * scale / 2 + barPositionCompressao + barDiameterCompressao / 2}
                                                y={verticalPositionCompressao}
                                            />
                                        );
                                    })
                                );
                            })}
                            {numBarsInEachRow.map((numBars: any, rowIndex: any) => {
                                let position = (cobrimento + diametroEstribo) * scale;  // Initialize position for the first bar in the row
                                const barDiameter = barDiameterInEachRow[rowIndex] * scale; // Scale the bar diameter
                                const verticalPosition = verticalPositionOfEachRow[rowIndex] * scale;
                                const horizontalSpacing = horizontalSpacingInEachRow[rowIndex] * scale;

                                let verticalPositionText
                                let verticalPositionQuota
                                let horizontalPositionQuota
                                let lineLengthQuota
                                let verticalPositionTextVerticalQuota

                                if (verticalPosition > height*scale/2) {
                                    verticalPositionText = verticalPosition - 15
                                    if (rowIndex == 0) {
                                        verticalPositionQuota = height*scale
                                        lineLengthQuota = - (height*scale - verticalPosition - barDiameter/2)
                                        horizontalPositionQuota = position + barDiameter/2
                                    } else {
                                        verticalPositionQuota =  height*scale - (height*scale - verticalPositionOfEachRow[rowIndex - 1] * scale) - barDiameterInEachRow[rowIndex - 1] * scale/2
                                        lineLengthQuota = - (height*scale - verticalPosition - barDiameter/2 - (height*scale - verticalPositionOfEachRow[rowIndex - 1] * scale) - barDiameterInEachRow[rowIndex - 1] * scale/2)
                                        horizontalPositionQuota = position + barDiameter/2
                                    }
                                    verticalPositionTextVerticalQuota =  verticalPositionQuota + lineLengthQuota/1.5
                                } else {
                                    verticalPositionText = verticalPosition + 6
                                    if (rowIndex == 0) {
                                        verticalPositionQuota = 0
                                        lineLengthQuota = verticalPosition - barDiameter/2
                                        horizontalPositionQuota = position + barDiameter/2
                                    } else {
                                        verticalPositionQuota = verticalPositionOfEachRow[rowIndex - 1] * scale + barDiameterInEachRow[rowIndex - 1] * scale / 2
                                        lineLengthQuota = verticalPosition - barDiameter/2 - verticalPositionOfEachRow[rowIndex - 1] * scale - barDiameterInEachRow[rowIndex-1] * scale / 2;
                                        horizontalPositionQuota = position + barDiameter/2
                                    }
                                    verticalPositionTextVerticalQuota = verticalPositionQuota + lineLengthQuota/4
                                }

                                if (numBars > 0) {
                                // @ts-ignore
                                    // @ts-ignore
                                    // @ts-ignore
                                    return (
                                    <div>
                                        <Line
                                            points={[0, 0, horizontalSpacing, 0]}
                                            stroke='#00B37E'
                                            strokeWidth={2}
                                            y={verticalPosition}
                                            x={width * scale / 2 + position + barDiameter}
                                        />
                                        <Text
                                            text={`${(horizontalSpacing/scale).toFixed(1).replace('.', ',')}`}
                                            fill='#00B37E'
                                            x={width * scale / 2 + position + barDiameter + (horizontalSpacing*scale)/25}
                                            y={verticalPositionText}
                                        />
                                        <Line
                                            points={[0, lineLengthQuota, 0, 0]}
                                            stroke='#00B37E'
                                            strokeWidth={2}
                                            y={verticalPositionQuota}
                                            x={width * scale / 2 + horizontalPositionQuota}
                                        />
                                        <Text
                                            text={`${(Math.abs(lineLengthQuota/scale)).toFixed(1).replace('.', ',')}`}
                                            fill='#00B37E'
                                            x={width * scale / 2 + horizontalPositionQuota - 20}
                                            y={verticalPositionTextVerticalQuota}
                                        />
                                        <Line
                                            points={[0, 0, width * scale / 2 + position - 22, 0]}
                                            dash={[10,5]}
                                            stroke='#00B37E'
                                            strokeWidth={2}
                                            y={verticalPosition}
                                            x={20}
                                        />
                                        <Text
                                            text={`${rowDetail['mensagem_detalhamento_tracao'].split('+')[rowIndex]}`}
                                            fill='#00B37E'
                                            x={0}
                                            y={verticalPosition-15}
                                        />
                                    </div>
                                )}
                            })}
                            {numBarsInEachRowCompressao.map((numBars: any, rowIndex: any) => {
                                let position = (cobrimento + diametroEstribo) * scale;  // Initialize position for the first bar in the row
                                const barDiameter = barDiameterInEachRowCompressao[rowIndex] * scale; // Scale the bar diameter
                                const verticalPosition = verticalPositionOfEachRowCompressao[rowIndex] * scale;
                                const horizontalSpacing = horizontalSpacingInEachRowCompressao[rowIndex] * scale;

                                let verticalPositionText
                                let verticalPositionQuota
                                let horizontalPositionQuota
                                let lineLengthQuota
                                let verticalPositionTextVerticalQuota
                                let textQuota

                                if (verticalPosition > height*scale/2) {
                                    verticalPositionText = verticalPosition - 15
                                    if (rowIndex == 0) {
                                        verticalPositionQuota = height*scale
                                        lineLengthQuota = - (height*scale - verticalPosition - barDiameter/2)
                                        horizontalPositionQuota = position + barDiameter/2
                                    } else {
                                        verticalPositionQuota =  height*scale - (height*scale - verticalPositionOfEachRowCompressao[rowIndex - 1] * scale) - barDiameterInEachRowCompressao[rowIndex - 1] * scale/2
                                        lineLengthQuota = - (height*scale - verticalPosition - barDiameter/2 - (height*scale - verticalPositionOfEachRowCompressao[rowIndex - 1] * scale) - barDiameterInEachRowCompressao[rowIndex - 1] * scale/2)
                                        horizontalPositionQuota = position + barDiameter/2
                                    }
                                    verticalPositionTextVerticalQuota =  verticalPositionQuota + lineLengthQuota/1.5
                                } else {
                                    verticalPositionText = verticalPosition + 6
                                    if (rowIndex == 0) {
                                        verticalPositionQuota = 0
                                        lineLengthQuota = verticalPosition - barDiameter/2
                                        horizontalPositionQuota = position + barDiameter/2
                                    } else {
                                        verticalPositionQuota = verticalPositionOfEachRowCompressao[rowIndex - 1] * scale + barDiameterInEachRowCompressao[rowIndex - 1] * scale / 2
                                        lineLengthQuota = verticalPosition - barDiameter/2 - verticalPositionOfEachRowCompressao[rowIndex - 1] * scale - barDiameterInEachRowCompressao[rowIndex-1] * scale / 2;
                                        horizontalPositionQuota = position + barDiameter/2
                                    }
                                    verticalPositionTextVerticalQuota = verticalPositionQuota + lineLengthQuota/4
                                }

                                if (rowDetailCompressao != {}) {
                                    // @ts-ignore
                                    textQuota = rowDetailCompressao['mensagem_detalhamento_compressao'].split('+')[rowIndex]
                                } else {
                                   textQuota = ''
                                }

                                if (numBars > 0) {
                                    return (
                                        <div>
                                            <Line
                                                points={[0, 0, horizontalSpacing, 0]}
                                                stroke='#00B37E'
                                                strokeWidth={2}
                                                y={verticalPosition}
                                                x={width * scale / 2 + position + barDiameter}
                                            />
                                            <Text
                                                text={`${(horizontalSpacing/scale).toFixed(1).replace('.', ',')}`}
                                                fill='#00B37E'
                                                x={width * scale / 2 + position + barDiameter + (horizontalSpacing*scale)/25}
                                                y={verticalPositionText}
                                            />
                                            <Line
                                                points={[0, lineLengthQuota, 0, 0]}
                                                stroke='#00B37E'
                                                strokeWidth={2}
                                                y={verticalPositionQuota}
                                                x={width * scale / 2 + horizontalPositionQuota}
                                            />
                                            <Text
                                                text={`${(Math.abs(lineLengthQuota/scale)).toFixed(1).replace('.', ',')}`}
                                                fill='#00B37E'
                                                x={width * scale / 2 + horizontalPositionQuota - 20}
                                                y={verticalPositionTextVerticalQuota}
                                            />
                                            <Line
                                                points={[0, 0, width * scale / 2 + position - 22, 0]}
                                                dash={[10,5]}
                                                stroke='#00B37E'
                                                strokeWidth={2}
                                                y={verticalPosition}
                                                x={20}
                                            />
                                            <Text
                                                text={textQuota}
                                                fill='#00B37E'
                                                x={0}
                                                y={verticalPosition-15}
                                            />
                                        </div>
                                    )}
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
