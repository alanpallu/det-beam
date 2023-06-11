import styled from 'styled-components'

export const HomeContainer = styled.main`
  flex: 1;
  
  padding: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;

  form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3.5rem;
    width: 75%;
  }
`

export const FormContainer = styled.div`
  display: flex;
  margin-top: 3rem;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  color: ${(props) => props.theme['gray-100']};
  font-size: 1.125rem;
  font-weight: bold;
  width: 100%;

  .div-1 {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
    gap: 2rem;
    width: 100%
  };

  .start {
    align-items: start;
  };
  
  .div-2 {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    
    label {
      white-space: nowrap;
    }
    
    .inicial {
      display: flex;
      align-items: start;
    }
    
    .div-nota {
      width: 100%;
      font-size: 14px;
      color: ${(props) => props.theme['gray-400']};
    }

    .div-nota-end {
      justify-content: end;
      display: flex;
    }
  
  .tramos-label {
    font-size: 1.5rem;
  }

  .cargas-label {
    font-size: 1.5rem;
  }

  .espaco-menor {
    width: 100%;
  }
`;

export const BasicInput = styled.input`
  width: 100%;
  background: transparent;
  height: 4rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
  border: 2px solid ${(props) => props.theme['gray-500']};
  font-weight: bold;
  font-size: 1.25rem;
  padding: 0 1rem;
  color: ${(props) => props.theme['gray-100']};

  &:focus {
    box-shadow: none;
    border-color: ${(props) => props.theme['green-500']};
  }

  &::placeholder {
    color: ${(props) => props.theme['gray-500']};
  }

  &::-webkit-calendar-picker-indicator {
    display: none !important;
  }
`

const BaseButton = styled.button`
  width: 100%;
  border: 0;
  padding: 1rem;
  border-radius: 8px;

  display: flex;
  align-items: center;
  justify-content: center;
  
  font-weight: bold;

  cursor: pointer;
  
  color: ${(props) => props.theme['gray-100']};

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  &:not(:disabled):hover {
    background: ${(props) => props.theme['green-700']};
  }
`

export const CalculateButton = styled(BaseButton)`
  background: ${(props) => props.theme['green-500']};
`

export const TramosButton = styled(BaseButton)`
  margin-top: 1.5rem;
  width: 20%;
  height: 5%;
  background: transparent;
  font-size: 1rem;
  color: ${(props) => props.theme['green-700']};
  
  &:not(:disabled):hover {
    background: transparent;
  }
`

