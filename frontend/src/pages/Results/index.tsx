import { HistoryContainer, HistoryList, Status } from './styles'

export function History() {
  return (
    <HistoryContainer>
      <h1>Resultados</h1>

      <HistoryList>
        <table>
          <thead>
            <tr>
              <th>Tramo</th>
              <th>Aréa de aço armadura longitudinal</th>
              <th>Detalhamento</th>
              <th>Verificação</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>2</td>
              <td></td>
              <td>
                <Status statusColor="green">Passou</Status>
              </td>
            </tr>
            <tr>
              <td>2</td>
              <td>3</td>
              <td></td>
              <td>
                <Status statusColor="red">Não passou</Status>
              </td>
            </tr>
          </tbody>
        </table>
      </HistoryList>
    </HistoryContainer>
  )
}
