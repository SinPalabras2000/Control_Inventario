import { useState, useCallback } from 'react';
import { inventoryApi } from '../services/api';
import { Product, InventoryData, InventoryReport, LoadingState } from '../types';
import toast from 'react-hot-toast';

export const useInventory = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [inventoryReports, setInventoryReports] = useState<InventoryReport[]>([]);
  const [loading, setLoading] = useState<LoadingState>({ isLoading: false });
  const [error, setError] = useState<string | null>(null);

  const fetchProductsByWarehouse = useCallback(async (warehouseId: string) => {
    setLoading({ isLoading: true, message: 'Cargando productos...' });
    setError(null);
    
    try {
      const data = await inventoryApi.getProductsByWarehouse(warehouseId);
      setProducts(data);
      toast.success(`${data.length} productos cargados`);
    } catch (err) {
      const errorMessage = 'Error al cargar productos';
      setError(errorMessage);
      toast.error(errorMessage);
      setProducts([]);
    } finally {
      setLoading({ isLoading: false });
    }
  }, []);

  const saveInventory = useCallback(async (inventoryData: InventoryData) => {
    setLoading({ isLoading: true, message: 'Guardando inventario...' });
    setError(null);
    
    try {
      const response = await inventoryApi.saveInventory(inventoryData);
      
      if (response.success) {
        toast.success(response.message || 'Inventario guardado exitosamente');
        return true;
      } else {
        const errorMessage = response.error || 'Error al guardar inventario';
        setError(errorMessage);
        toast.error(errorMessage);
        return false;
      }
    } catch (err) {
      const errorMessage = 'Error al guardar inventario';
      setError(errorMessage);
      toast.error(errorMessage);
      return false;
    } finally {
      setLoading({ isLoading: false });
    }
  }, []);

  const fetchInventoryByDate = useCallback(async (date: string) => {
    setLoading({ isLoading: true, message: 'Consultando inventario...' });
    setError(null);
    
    try {
      const data = await inventoryApi.getInventoryByDate(date);
      setInventoryReports(data);
      toast.success(`Inventario del ${date} cargado`);
    } catch (err) {
      const errorMessage = 'Error al consultar inventario';
      setError(errorMessage);
      toast.error(errorMessage);
      setInventoryReports([]);
    } finally {
      setLoading({ isLoading: false });
    }
  }, []);

  const clearData = useCallback(() => {
    setProducts([]);
    setInventoryReports([]);
    setError(null);
  }, []);

  return {
    products,
    inventoryReports,
    loading,
    error,
    fetchProductsByWarehouse,
    saveInventory,
    fetchInventoryByDate,
    clearData,
  };
};

export default useInventory;