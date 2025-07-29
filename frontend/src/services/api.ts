import axios, { AxiosResponse } from 'axios';
import { Product, InventoryData, InventoryReport, ApiResponse } from '../types';

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para manejar errores globalmente
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export const inventoryApi = {
  // Obtener productos por bodega
  getProductsByWarehouse: async (warehouseId: string): Promise<Product[]> => {
    try {
      const response: AxiosResponse<Product[]> = await api.get(`/api/products/${warehouseId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },

  // Guardar inventario
  saveInventory: async (inventoryData: InventoryData): Promise<ApiResponse<any>> => {
    try {
      const formData = new FormData();
      
      // Agregar todos los datos del inventario al FormData
      Object.entries(inventoryData).forEach(([key, value]) => {
        formData.append(key, value.toString());
      });
      
      const response: AxiosResponse<string> = await api.post('/guardar_inventario', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      // Verificar si la respuesta contiene mensaje de éxito
      const isSuccess = response.data.includes('exitosamente');
      
      return {
        success: isSuccess,
        message: isSuccess ? 'Inventario guardado exitosamente' : 'Error al guardar inventario'
      };
    } catch (error) {
      console.error('Error saving inventory:', error);
      return {
        success: false,
        error: 'Error al guardar el inventario'
      };
    }
  },

  // Consultar inventario por día
  getInventoryByDate: async (date: string): Promise<InventoryReport[]> => {
    try {
      const response: AxiosResponse<any[]> = await api.get(`/api/inventory-report/${date}`);
      
      // Mapear los datos del backend al formato esperado por el frontend
      const mappedData: InventoryReport[] = response.data.map((item: any) => ({
        CodMPSys: item.CodMPSys,
        Nombre: item.Nombre,
        CantidadPaquetes: item.InvPreparacion || 0,
        CantidadUnidades: item.InvBodega || 0,
        Observaciones: item.Diferencia > 0 ? 'Exceso' : item.Diferencia < 0 ? 'Faltante' : 'Correcto',
        UsuarioRegistro: 'Sistema',
        FechaRegistro: date,
        InvFisico: item.InvFisico,
        SaldoActual: item.SaldoActual,
        Diferencia: item.Diferencia
      }));
      
      return mappedData;
    } catch (error) {
      console.error('Error fetching inventory report:', error);
      throw error;
    }
  },
};

// Funciones mock para simular datos mientras mantenemos la funcionalidad
// Funciones auxiliares removidas - ahora usamos la API real

export default api;