import styled from 'styled-components'

export const LayoutContainer = styled.div`
  height: 100%;
  margin: auto;
  padding: 2.5rem;

  background: ${(props) => props.theme['gray-800']};
  border-radius: 8px;

  display: flex;
  flex-direction: column;
`
