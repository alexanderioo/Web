import { useState } from "react";
import "./Header.css";
import { NavLink } from "react-router-dom";

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <header className="header">
      <div className="container">
        <div className="logo">
          <NavLink to="/" onClick={closeMenu}>Конный клуб</NavLink>
        </div>
        
        <button className="burger-menu" onClick={toggleMenu}>
          <span className={`burger-line ${isMenuOpen ? 'open' : ''}`}></span>
          <span className={`burger-line ${isMenuOpen ? 'open' : ''}`}></span>
          <span className={`burger-line ${isMenuOpen ? 'open' : ''}`}></span>
        </button>

        <nav className={`nav ${isMenuOpen ? 'open' : ''}`}>
          <NavLink to="/news" onClick={closeMenu}>Новости</NavLink>
          <NavLink to="/about" onClick={closeMenu}>О нас</NavLink>
          <NavLink to="/services" onClick={closeMenu}>Услуги</NavLink>
          <NavLink to="/filters" onClick={closeMenu}>Фильтры</NavLink>
          <NavLink to="/contact" onClick={closeMenu}>Контакты</NavLink>
        </nav>
      </div>
    </header>
  );
}
