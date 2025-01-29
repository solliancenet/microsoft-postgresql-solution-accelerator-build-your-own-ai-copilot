export type User = {
  id: string;
  name: string;
  email: string;
};

export type Product = {
  id: string;
  title: string;
  price: number;
  description: string;
};

export interface ApiResponse<T> {
  data: T;
  error?: string;
}