export interface Product {
  id: number;
  name: string;
  unit: string;
  type: string;
  inventoryType: number;
}

export interface InventoryData {
  [key: string]: string | number;
}

export interface InventoryFormData {
  Bodega: string;
  Usuario: string;
  FechaInv: string;
}

export interface InventoryItem {
  productCode: string;
  packages?: number;
  units?: number;
  option?: string;
}

export interface InventoryReport {
  CodMPSys?: string;
  CodMP?: string;
  Nombre?: string;
  DscNegocio?: string;
  UdeM?: string;
  CantidadPaquetes?: number;
  CantidadUnidades?: number;
  Observaciones?: string;
  FechaRegistro: string;
  UsuarioRegistro: string;
  InvFisico?: number;
  SaldoActual?: number;
  Diferencia?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

export interface ToastOptions {
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface FormErrors {
  [key: string]: string;
}

export interface SelectOption {
  value: string;
  label: string;
}

export interface WarehouseOption extends SelectOption {
  value: '2' | '4';
  label: 'Preparación' | 'Bodega';
}

export interface UserOption extends SelectOption {
  value: 'Toño' | 'Karen' | 'Stiven' | 'Fredy';
  label: 'Toño' | 'Karen' | 'Stiven' | 'Fredy';
}