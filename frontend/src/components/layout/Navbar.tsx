import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Package, Home, ClipboardList, Menu, X } from 'lucide-react';
import { Button } from '../ui';

const Navbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();
  
  const navigation = [
    {
      name: 'Inicio',
      href: '/',
      icon: Home,
      current: location.pathname === '/'
    },
    {
      name: 'Consulta Inventario',
      href: '/consulta-inventario',
      icon: ClipboardList,
      current: location.pathname === '/consulta-inventario'
    },
  ];
  
  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  
  return (
    <nav className="bg-brand-600 shadow-xl sticky top-0 z-40 border-b-4 border-accent-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Título a la izquierda con caricaturas */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2 text-white hover:text-accent-200 transition-all duration-300 transform hover:scale-105">
              <span className="text-2xl">🍔</span>
              <span className="font-bold text-xl tracking-wide">Sin Palabras la 2000</span>
              <span className="text-2xl">🌭</span>
              <span className="text-2xl">🍟</span>
            </Link>
          </div>
          
          {/* Navegación desktop */}
          <div className="hidden md:flex items-center space-x-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-300 transform hover:scale-105 ${
                    item.current
                      ? 'bg-accent-400 text-brand-800 shadow-lg'
                      : 'text-accent-100 hover:bg-accent-500 hover:text-brand-800 hover:shadow-md'
                  }`}
                >
                  <Icon className={`h-4 w-4 ${item.current ? '' : ''}`} />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
          
          {/* Botón menú móvil */}
          <div className="md:hidden flex items-center">
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleMenu}
              className="text-white hover:bg-accent-500 hover:text-brand-800 transition-all duration-300 transform hover:scale-110"
            >
              {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </Button>
          </div>
        </div>
      </div>
      
      {/* Menú móvil */}
      {isMenuOpen && (
        <div className="md:hidden bg-brand-700 border-t-4 border-accent-400 animate-slideDown">
          <div className="px-3 pt-3 pb-4 space-y-2">
            {navigation.map((item, index) => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  onClick={() => setIsMenuOpen(false)}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg text-base font-semibold transition-all duration-300 transform hover:scale-105 animate-fadeIn ${
                    item.current
                      ? 'bg-accent-400 text-brand-800 shadow-lg'
                      : 'text-accent-100 hover:bg-accent-500 hover:text-brand-800 hover:shadow-md'
                  }`}
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <Icon className={`h-5 w-5`} />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;