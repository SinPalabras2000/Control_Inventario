import React, { useState } from 'react';
import { Search, Calendar, FileText, Download, AlertCircle } from 'lucide-react';
import { Card, Button, Input, Badge, LoadingSpinner } from '../components/ui';
import { useInventory } from '../hooks/useInventory';
import { InventoryReport } from '../types';
import { format } from 'date-fns';
import toast from 'react-hot-toast';

const InventoryQuery: React.FC = () => {
  const { inventoryReports, loading, fetchInventoryByDate } = useInventory();
  const [selectedDate, setSelectedDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const [hasSearched, setHasSearched] = useState(false);
  
  const handleSearch = async () => {
    if (!selectedDate) {
      toast.error('Debe seleccionar una fecha');
      return;
    }
    
    setHasSearched(true);
    await fetchInventoryByDate(selectedDate);
  };
  
  const handleExport = () => {
    if (inventoryReports.length === 0) {
      toast.error('No hay datos para exportar');
      return;
    }
    
    // Crear CSV
    const headers = ['Código', 'Producto', 'Unidad', 'Paquetes', 'Unidades', 'Observaciones', 'Fecha', 'Usuario'];
    const csvContent = [
      headers.join(','),
      ...inventoryReports.map(item => [
        item.CodMP,
        `"${item.DscNegocio}"`,
        item.UdeM,
        item.CantidadPaquetes || 0,
        item.CantidadUnidades || 0,
        `"${item.Observaciones || ''}"`,
        item.FechaRegistro,
        item.UsuarioRegistro
      ].join(','))
    ].join('\n');
    
    // Descargar archivo
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `inventario_${selectedDate}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    toast.success('Archivo exportado exitosamente');
  };
  
  const getTotalPackages = () => {
    return inventoryReports.reduce((total, item) => total + (item.CantidadPaquetes || 0), 0);
  };
  
  const getTotalUnits = () => {
    return inventoryReports.reduce((total, item) => total + (item.CantidadUnidades || 0), 0);
  };
  
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Consulta de Inventario</h1>
          <p className="text-gray-600">Consulte los inventarios registrados por fecha</p>
        </div>
      </div>
      
      {/* Formulario de búsqueda */}
      <Card>
        <Card.Header>
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-primary-100 rounded-lg">
              <Search className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Buscar Inventario</h2>
              <p className="text-sm text-gray-600">Seleccione la fecha para consultar el inventario</p>
            </div>
          </div>
        </Card.Header>
        
        <Card.Body>
          <div className="flex flex-col sm:flex-row gap-4 items-end">
            <div className="flex-1">
              <Input
                label="Fecha de Inventario"
                type="date"
                value={selectedDate}
                onChange={(e) => setSelectedDate(e.target.value)}
                leftIcon={<Calendar className="h-5 w-5" />}
                required
              />
            </div>
            <Button
              variant="primary"
              onClick={handleSearch}
              isLoading={loading.isLoading}
              leftIcon={<Search className="h-4 w-4" />}
              className="sm:w-auto w-full"
            >
              Consultar
            </Button>
          </div>
        </Card.Body>
      </Card>
      
      {/* Resultados */}
      {loading.isLoading ? (
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner size="lg" text={loading.message} />
        </div>
      ) : hasSearched && (
        <Card>
          <Card.Header>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-success-100 rounded-lg">
                  <FileText className="h-6 w-6 text-success-600" />
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">
                    Inventario del {format(new Date(selectedDate), 'dd/MM/yyyy')}
                  </h2>
                  <p className="text-sm text-gray-600">
                    {inventoryReports.length} productos encontrados
                  </p>
                </div>
              </div>
              
              {inventoryReports.length > 0 && (
                <Button
                  variant="secondary"
                  onClick={handleExport}
                  leftIcon={<Download className="h-4 w-4" />}
                >
                  Exportar CSV
                </Button>
              )}
            </div>
          </Card.Header>
          
          <Card.Body className="p-0">
            {inventoryReports.length === 0 ? (
              <div className="p-8 text-center">
                <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No se encontraron registros
                </h3>
                <p className="text-gray-600">
                  No hay inventarios registrados para la fecha seleccionada
                </p>
              </div>
            ) : (
              <>
                {/* Resumen */}
                <div className="p-6 bg-gray-50 border-b border-gray-200">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-primary-600">{inventoryReports.length}</div>
                      <div className="text-sm text-gray-600">Productos</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-success-600">{getTotalPackages()}</div>
                      <div className="text-sm text-gray-600">Total Paquetes</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-warning-600">{getTotalUnits()}</div>
                      <div className="text-sm text-gray-600">Total Unidades</div>
                    </div>
                  </div>
                </div>
                
                {/* Tabla */}
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50 border-b border-gray-200">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Código
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Producto
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Inv. Preparación
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Inv. Bodega
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Inv. Físico
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Saldo Actual
                        </th>
                        <th className="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Diferencia
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Estado
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {inventoryReports.map((item, index) => (
                        <tr key={`${item.CodMPSys || item.CodMP}-${index}`} className="hover:bg-gray-50">
                          <td className="px-6 py-4 text-sm font-medium text-gray-900">
                            {item.CodMPSys || item.CodMP}
                          </td>
                          <td className="px-6 py-4">
                            <div className="text-sm font-medium text-gray-900">
                              {item.Nombre || item.DscNegocio}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <Badge variant={item.CantidadPaquetes ? 'success' : 'secondary'}>
                              {item.CantidadPaquetes?.toFixed(2) || '0.00'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <Badge variant={item.CantidadUnidades ? 'success' : 'secondary'}>
                              {item.CantidadUnidades?.toFixed(2) || '0.00'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <Badge variant={item.InvFisico ? 'primary' : 'secondary'}>
                              {item.InvFisico?.toFixed(2) || '0.00'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <Badge variant={item.SaldoActual ? 'info' : 'secondary'}>
                              {item.SaldoActual?.toFixed(2) || '0.00'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 text-center">
                            <Badge 
                              variant={
                                (item.Diferencia || 0) > 0 ? 'success' :
                                (item.Diferencia || 0) < 0 ? 'error' : 'secondary'
                              }
                            >
                              {item.Diferencia?.toFixed(2) || '0.00'}
                            </Badge>
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-900">
                            {item.Observaciones ? (
                              <Badge 
                                variant={
                                  item.Observaciones === 'Correcto' ? 'success' :
                                  item.Observaciones === 'Exceso' ? 'warning' :
                                  item.Observaciones === 'Faltante' ? 'error' : 'secondary'
                                }
                              >
                                {item.Observaciones}
                              </Badge>
                            ) : (
                              <Badge variant="secondary">Sin datos</Badge>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </Card.Body>
        </Card>
      )}
    </div>
  );
};

export default InventoryQuery;