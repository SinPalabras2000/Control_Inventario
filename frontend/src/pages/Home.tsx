import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, Package, User, Play } from 'lucide-react';
import { Card, Button, Select, Input } from '../components/ui';
import { useForm } from '../hooks/useForm';
import { InventoryFormData, WarehouseOption, UserOption } from '../types';
import { format } from 'date-fns';

const Home: React.FC = () => {
  const navigate = useNavigate();
  
  const warehouseOptions: WarehouseOption[] = [
    { value: '2', label: 'Preparación' },
    { value: '4', label: 'Bodega' },
  ];
  
  const userOptions: UserOption[] = [
    { value: 'Toño', label: 'Toño' },
    { value: 'Karen', label: 'Karen' },
    { value: 'Stiven', label: 'Stiven' },
    { value: 'Fredy', label: 'Fredy' },
  ];
  
  const { values, handleChange, handleSubmit, getFieldError } = useForm<InventoryFormData>({
    initialValues: {
      Bodega: '',
      Usuario: '',
      FechaInv: format(new Date(), 'yyyy-MM-dd'),
    },
    validate: (values) => {
      const errors: { [key: string]: string } = {};
      
      if (!values.Bodega) {
        errors.Bodega = 'Debe seleccionar una bodega';
      }
      
      if (!values.Usuario) {
        errors.Usuario = 'Debe seleccionar un responsable';
      }
      
      if (!values.FechaInv) {
        errors.FechaInv = 'Debe seleccionar una fecha';
      }
      
      return errors;
    },
    onSubmit: (formData) => {
      // Navegar a la página de inventario con los datos del formulario
      navigate('/inventario', { state: formData });
    },
  });
  
  return (
    <div className="space-y-8">
      {/* Formulario de inicio de inventario */}
      <div className="max-w-2xl mx-auto">
        <Card shadow="lg" className="animate-fade-in border-4 border-accent-400 bg-white transform hover:scale-[1.02] transition-all duration-700 ease-out shadow-2xl shadow-primary-500/30">
          <Card.Header className="bg-primary-600 text-white rounded-t-2xl">
            <div className="flex items-center space-x-4 p-4">
              <div className="p-3 bg-accent-400 rounded-2xl shadow-lg">
                <Package className="h-7 w-7 text-primary-600" />
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-accent-300 drop-shadow-sm">Iniciar Inventario</h2>
                <p className="text-accent-200 font-semibold">Configura los parámetros para comenzar</p>
              </div>
              <div className="text-3xl">
                <span>📋</span>
              </div>
            </div>
          </Card.Header>
          
          <Card.Body className="p-8 space-y-8 bg-primary-50">
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Selección de bodega */}
              <div className="animate-fade-in" style={{animationDelay: '0.2s'}}>
                <label className="flex items-center text-lg font-bold mb-4 text-primary-700">
                  <span className="text-2xl mr-3 text-primary-600">🏪</span>
                  Bodega
                </label>
                <Select
                  name="Bodega"
                  value={values.Bodega}
                  onChange={handleChange}
                  options={warehouseOptions}
                  placeholder="Selecciona una bodega"
                  error={getFieldError('Bodega')}
                  required
                  className="border-3 border-accent-400 focus:border-primary-500 focus:ring-primary-300 rounded-xl text-lg p-4 transition-all duration-300 hover:shadow-lg bg-white"
                />
              </div>

              {/* Fecha de inventario */}
              <div className="animate-fade-in" style={{animationDelay: '0.4s'}}>
                <label className="flex items-center text-lg font-bold mb-4 text-primary-700">
                  <span className="text-2xl mr-3 text-blue-600">📅</span>
                  Fecha de Inventario
                </label>
                <Input
                  type="date"
                  name="FechaInv"
                  value={values.FechaInv}
                  onChange={handleChange}
                  error={getFieldError('FechaInv')}
                  leftIcon={<Calendar className="h-5 w-5 text-primary-600" />}
                  required
                  className="border-3 border-accent-400 focus:border-primary-500 focus:ring-primary-300 rounded-xl text-lg p-4 transition-all duration-300 hover:shadow-lg bg-white"
                />
              </div>

              {/* Usuario responsable */}
              <div className="animate-fade-in" style={{animationDelay: '0.6s'}}>
                <label className="flex items-center text-lg font-bold mb-4 text-primary-700">
                  <span className="text-2xl mr-3 text-accent-600">👤</span>
                  Usuario Responsable
                </label>
                <Select
                  name="Usuario"
                  value={values.Usuario}
                  onChange={handleChange}
                  options={userOptions}
                  placeholder="Selecciona un usuario"
                  error={getFieldError('Usuario')}
                  required
                  className="border-3 border-accent-400 focus:border-primary-500 focus:ring-primary-300 rounded-xl text-lg p-4 transition-all duration-300 hover:shadow-lg bg-white"
                />
              </div>

              {/* Botón de envío */}
              <div className="pt-6 animate-fade-in" style={{animationDelay: '0.8s'}}>
                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  fullWidth
                  leftIcon={<Play className="h-6 w-6" />}
                  className="bg-primary-600 hover:bg-primary-700 text-white font-bold py-4 px-8 rounded-xl text-lg shadow-xl hover:shadow-2xl transform hover:scale-105 transition-all duration-300 border-4 border-accent-400"
                >
                  <span className="mr-3 text-2xl text-accent-300">🚀</span>
                  Comenzar Inventario
                  <span className="ml-3 text-2xl text-accent-300">🚀</span>
                </Button>
              </div>
            </form>
          </Card.Body>
        </Card>
      </div>
      

    </div>
  );
};

export default Home;