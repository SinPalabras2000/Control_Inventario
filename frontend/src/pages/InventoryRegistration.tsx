import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Save, ArrowLeft, Package, User, Calendar, AlertCircle } from 'lucide-react';
import { Card, Button, Input, Select, Badge, LoadingSpinner } from '../components/ui';
import { useInventory } from '../hooks/useInventory';
import { InventoryFormData, Product, InventoryData } from '../types';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

const InventoryRegistration: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { products, loading, fetchProductsByWarehouse, saveInventory } = useInventory();
  
  const [inventoryData, setInventoryData] = useState<InventoryData>({});
  const [isSaving, setIsSaving] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Set<string>>(new Set());
  
  // Obtener datos del formulario desde el estado de navegación
  const formData = location.state as InventoryFormData;
  
  // Redirigir si no hay datos del formulario
  useEffect(() => {
    if (!formData) {
      toast.error('Datos de inventario no encontrados');
      navigate('/');
      return;
    }
    
    // Cargar productos de la bodega seleccionada
    fetchProductsByWarehouse(formData.Bodega);
    
    // Inicializar datos del inventario con información del formulario
    setInventoryData({
      Bodega: formData.Bodega,
      Usuario: formData.Usuario,
      FechaInv: formData.FechaInv,
    });
  }, [formData, fetchProductsByWarehouse, navigate]);
  
  // Debug: mostrar productos en consola
  useEffect(() => {
    console.log('Productos cargados:', products);
  }, [products]);
  
  const handleInputChange = (productCode: string, field: string, value: string) => {
    const key = `${field}_${productCode}`;
    setInventoryData(prev => ({
      ...prev,
      [key]: value,
    }));
    
    // Limpiar error de validación si el campo ahora tiene valor
    if (value && value.trim() !== '') {
      setValidationErrors(prev => {
        const newErrors = new Set(prev);
        newErrors.delete(key);
        return newErrors;
      });
    }
  };
  
  const validateRequiredFields = (): boolean => {
    const errors = new Set<string>();
    
    products.forEach(product => {
      // Validar campos según el tipo de producto
      if (product.type === 'Paquetes' || product.type === 'Ambos') {
        const paquetesKey = `Paquetes_${product.id}`;
        const paquetesValue = inventoryData[paquetesKey];
        if (!paquetesValue || String(paquetesValue).trim() === '') {
          errors.add(paquetesKey);
        }
      }
      
      if (product.type === 'Unidades' || product.type === 'Ambos') {
        const unidadesKey = `Unidades_${product.id}`;
        const unidadesValue = inventoryData[unidadesKey];
        if (!unidadesValue || String(unidadesValue).trim() === '') {
          errors.add(unidadesKey);
        }
      }
    });
    
    setValidationErrors(errors);
    
    // Navegar al primer campo con error
    if (errors.size > 0) {
      const firstErrorField = Array.from(errors)[0];
      const element = document.querySelector(`[data-field="${firstErrorField}"]`);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        (element as HTMLElement).focus();
      }
    }
    
    return errors.size === 0;
  };
  
  const handleSaveInventory = async () => {
    // Validar campos obligatorios antes de guardar
    if (!validateRequiredFields()) {
      toast.error('Por favor complete todos los campos obligatorios marcados en rojo');
      return;
    }
    
    setIsSaving(true);
    
    try {
      const success = await saveInventory(inventoryData);
      
      if (success) {
        navigate('/');
      }
    } catch (error) {
      // El error ya se maneja en el hook useInventory
    } finally {
      setIsSaving(false);
    }
  };
  
  const getWarehouseName = (warehouseId: string) => {
    return warehouseId === '2' ? 'Preparación' : 'Bodega';
  };
  
  if (!formData) {
    return null;
  }
  
  if (loading.isLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="lg" text={loading.message} />
      </div>
    );
  }
  
  return (
    <div className="relative">
      {/* Botón Volver en esquina superior izquierda */}
      <div className="fixed top-20 left-4 z-50 md:top-4">
        <Button
          variant="primary"
          onClick={() => navigate('/')}
          leftIcon={<ArrowLeft className="h-4 w-4" />}
          className="!bg-brand-600 !text-white hover:!bg-brand-700 shadow-lg border-2 border-accent-400 rounded-lg"
        >
          Volver
        </Button>
      </div>
      
      {/* Información del inventario en esquina */}
      <div className="fixed top-20 right-4 z-40 md:top-4">
        <div className="bg-white/95 backdrop-blur-sm border border-gray-200 rounded-lg p-2 shadow-md">
          <div className="flex flex-col gap-1">
            <div className="flex items-center gap-1">
              <div className="bg-brand-600 rounded-full p-1">
                <User className="h-2 w-2 text-white" />
              </div>
              <span className="text-xs font-medium text-gray-700">{formData.Usuario}</span>
            </div>
            
            <div className="flex items-center gap-1">
              <div className="bg-accent-600 rounded-full p-1">
                <Package className="h-2 w-2 text-white" />
              </div>
              <span className="text-xs font-medium text-gray-700">{getWarehouseName(formData.Bodega)}</span>
            </div>
            
            <div className="flex items-center gap-1">
              <div className="bg-primary-600 rounded-full p-1">
                <Calendar className="h-2 w-2 text-white" />
              </div>
              <span className="text-xs font-medium text-gray-700">{format(new Date(formData.FechaInv), 'dd/MM/yyyy')}</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Tabla de productos */}
      <div className="w-full">
        <Card shadow="lg" className="border-4 border-accent-400 bg-white transform hover:scale-[1.01] transition-all duration-300 shadow-2xl shadow-brand-500/20 rounded-2xl">
        <Card.Body className="p-0">
          {products.length === 0 ? (
            <div className="p-12 text-center">
              <div className="bg-accent-100 rounded-full p-6 w-24 h-24 mx-auto mb-6 flex items-center justify-center">
                <AlertCircle className="h-12 w-12 text-accent-600" />
              </div>
              <h3 className="text-xl font-bold text-brand-700 mb-2">📦 No hay productos disponibles</h3>
              <p className="text-brand-600 text-lg">No se encontraron productos para inventariar en esta bodega</p>
              <div className="mt-6">
                <Button
                  variant="primary"
                  onClick={() => navigate('/')}
                  leftIcon={<ArrowLeft className="h-5 w-5" />}
                  className="bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 font-semibold"
                >
                  🏠 Volver al Inicio
                </Button>
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-accent-100 border-b-4 border-accent-300">
                  <tr>
                    <th className="w-1/2 px-2 py-4 text-left text-sm font-bold text-brand-700 uppercase tracking-wider">
                      📦 Producto
                    </th>

                    <th className="w-1/4 px-1 py-3 text-center text-xs font-bold text-brand-700 uppercase tracking-wider">
                      📦 Paquetes
                    </th>
                    <th className="w-1/4 px-1 py-3 text-center text-xs font-bold text-brand-700 uppercase tracking-wider">
                      🔢 Unidades
                    </th>

                  </tr>
                </thead>
                <tbody className="bg-white divide-y-2 divide-accent-200">
                  {products.map((product, index) => (
                    <tr key={product.id} className={`hover:bg-accent-50 transition-all duration-200 ${index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}>
                      <td className="w-1/2 px-2 py-4">
                        <div>
                          <div className="text-sm font-bold text-brand-800">{product.name}</div>
                          <div className="text-xs text-gray-500 mt-1">{product.unit}</div>
                        </div>
                      </td>

                      <td className="w-1/4 px-1 py-4 text-center">
                        {product.type === 'Paquetes' || product.type === 'Ambos' ? (
                          <input
                            type="number"
                            placeholder="0"
                            className={`w-full px-2 py-2 text-sm border-2 rounded-lg focus:ring-2 focus:outline-none ${
                              validationErrors.has(`Paquetes_${product.id}`) 
                                ? 'border-red-500 focus:border-red-500 focus:ring-red-200 bg-red-50' 
                                : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
                            }`}
                            min="0"
                            value={inventoryData[`Paquetes_${product.id}`] || ''}
                            onChange={(e) => handleInputChange(product.id.toString(), 'Paquetes', e.target.value)}
                            data-field={`Paquetes_${product.id}`}
                          />
                        ) : (
                          <span className="text-gray-500 bg-gray-100 px-2 py-1 rounded-full text-xs font-medium mx-auto block w-fit">N/A</span>
                        )}
                      </td>
                      <td className="w-1/4 px-1 py-4 text-center">
                        {product.type === 'Unidades' || product.type === 'Ambos' ? (
                          product.inventoryType === 2 ? (
                            <select
                              className={`w-full px-2 py-2 text-xs border-2 rounded-lg focus:ring-2 focus:outline-none ${
                                validationErrors.has(`Unidades_${product.id}`) 
                                  ? 'border-red-500 focus:border-red-500 focus:ring-red-200 bg-red-50' 
                                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
                              }`}
                              value={inventoryData[`Unidades_${product.id}`] || ''}
                              onChange={(e) => handleInputChange(product.id.toString(), 'Unidades', e.target.value)}
                              required
                              data-field={`Unidades_${product.id}`}
                            >
                              <option value="">Seleccione</option>
                              <option value="0.75">Casi Completo</option>
                              <option value="0.50">Medio</option>
                              <option value="0.25">Un Cuarto</option>
                              <option value="0">Nada</option>
                            </select>
                          ) : product.inventoryType === 3 ? (
                            <select
                              className={`w-40 px-4 py-3 text-xs border-2 rounded-lg focus:ring-2 focus:outline-none ${
                                validationErrors.has(`Unidades_${product.id}`) 
                                  ? 'border-red-500 focus:border-red-500 focus:ring-red-200 bg-red-50' 
                                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
                              }`}
                              value={inventoryData[`Unidades_${product.id}`] || ''}
                              onChange={(e) => handleInputChange(product.id.toString(), 'Unidades', e.target.value)}
                              required
                              data-field={`Unidades_${product.id}`}
                            >
                              <option value="">Seleccione</option>
                              <option value="0">Nada</option>
                              <option value="350">1 Tarro</option>
                              <option value="700">2 Tarros</option>
                              <option value="1050">3 Tarros</option>
                              <option value="1400">4 Tarros</option>
                              <option value="1750">5 Tarros</option>
                              <option value="2100">6 Tarros</option>
                              <option value="2450">7 Tarros</option>
                              <option value="2800">8 Tarros</option>
                              <option value="3150">9 Tarros</option>
                              <option value="3500">10 Tarros</option>
                            </select>
                          ) : (
                            <input
                              type="number"
                              placeholder="0"
                              className={`w-full px-2 py-2 text-sm border-2 rounded-lg focus:ring-2 focus:outline-none ${
                                validationErrors.has(`Unidades_${product.id}`) 
                                  ? 'border-red-500 focus:border-red-500 focus:ring-red-200 bg-red-50' 
                                  : 'border-gray-300 focus:border-blue-500 focus:ring-blue-200'
                              }`}
                              min="0"
                              value={inventoryData[`Unidades_${product.id}`] || ''}
                              onChange={(e) => handleInputChange(product.id.toString(), 'Unidades', e.target.value)}
                              data-field={`Unidades_${product.id}`}
                            />
                          )
                        ) : (
                          <span className="text-gray-500 bg-gray-100 px-3 py-2 rounded-full text-sm font-medium mx-auto block w-fit">N/A</span>
                        )}
                      </td>

                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card.Body>
        
        {products.length > 0 && (
          <Card.Footer className="bg-accent-50 border-t-4 border-accent-300 rounded-b-2xl">
            <div className="flex justify-center space-x-6 p-6">
              <Button
                variant="secondary"
                onClick={() => navigate('/')}
                className="bg-gray-100 hover:bg-gray-200 text-gray-700 border-2 border-gray-300 px-8 py-3 text-lg font-semibold transform hover:scale-105 transition-all duration-300"
                leftIcon={<ArrowLeft className="h-5 w-5 text-gray-700" />}
              >
                Cancelar
              </Button>
              <Button
                variant="success"
                onClick={handleSaveInventory}
                isLoading={isSaving}
                leftIcon={<Save className="h-5 w-5 text-white" />}
                className="bg-brand-600 hover:bg-brand-700 text-white border-2 border-accent-400 px-8 py-3 text-lg font-semibold transform hover:scale-105 transition-all duration-300 shadow-lg"
              >
                Guardar Inventario
              </Button>
            </div>
          </Card.Footer>
        )}
      </Card>
      </div>
    </div>
  );
};

export default InventoryRegistration;