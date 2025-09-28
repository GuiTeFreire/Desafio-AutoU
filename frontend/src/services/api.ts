const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://desafio-autou-back-fxvg.onrender.com';

export interface ProcessEmailResponse {
  category: string;
  confidence: number;
  suggested_reply: string;
  classify_source: string;
  reply_source?: string;
}

export class ApiService {
  private static async makeRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro na API: ${response.status} - ${errorText}`);
    }

    return response.json();
  }

  static async processEmailText(text: string): Promise<ProcessEmailResponse> {
    const formData = new FormData();
    formData.append('text', text);

    const response = await fetch(`${API_BASE_URL}/api/process_email`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro na API: ${response.status} - ${errorText}`);
    }

    return response.json();
  }

  static async processEmailFile(file: File): Promise<ProcessEmailResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/process_email`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Erro na API: ${response.status} - ${errorText}`);
    }

    return response.json();
  }

  static async healthCheck(): Promise<{ status: string }> {
    return this.makeRequest('/health');
  }
}
