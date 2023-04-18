import { HeaderContainer } from './styles'
import { Scroll, Calculator } from 'phosphor-react'

import logoConcreto from '../../assets/logo-concreto.png'
import { NavLink } from 'react-router-dom'

export function Header() {
  return (
    <HeaderContainer>
      <span>
        <img src={logoConcreto} alt="" />
      </span>
      <h1>
        Dimensionador e Detalhador de Vigas
      </h1>
      <nav>
        <NavLink to="/" title="Formulario">
          <Scroll size={36} />
        </NavLink>
        <NavLink to="/calc" title="Cálculos">
          <Calculator size={36} />
        </NavLink>
      </nav>
    </HeaderContainer>
  )
}
