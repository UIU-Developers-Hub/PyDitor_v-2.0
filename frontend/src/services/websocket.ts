// src/services/websocket.ts
export type WebSocketMessageData = {
    type: string;
    data: unknown;
  };
  
  export class WebSocketService {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private maxReconnectAttempts = 5;
    private listeners: Map<string, Set<(data: unknown) => void>> = new Map();
  
    constructor(private url: string) {}
  
    connect(): void {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = () => {
        this.reconnectAttempts = 0;
        this.notifyListeners('connection', { status: 'connected' });
      };
  
      this.ws.onclose = () => {
        this.notifyListeners('connection', { status: 'disconnected' });
        this.attemptReconnect();
      };
  
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data) as WebSocketMessageData;
        this.notifyListeners(data.type, data.data);
      };
  
      this.ws.onerror = (error) => {
        this.notifyListeners('error', error);
      };
    }
  
    private attemptReconnect(): void {
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.reconnectAttempts++;
        setTimeout(() => this.connect(), 1000 * this.reconnectAttempts);
      }
    }
  
    send(type: string, data: unknown): void {
      if (this.ws?.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type, data }));
      }
    }
  
    subscribe(event: string, callback: (data: unknown) => void): void {
      if (!this.listeners.has(event)) {
        this.listeners.set(event, new Set());
      }
      this.listeners.get(event)?.add(callback);
    }
  
    unsubscribe(event: string, callback: (data: unknown) => void): void {
      this.listeners.get(event)?.delete(callback);
    }
  
    private notifyListeners(event: string, data: unknown): void {
      this.listeners.get(event)?.forEach(callback => callback(data));
    }
  
    disconnect(): void {
      this.ws?.close();
      this.ws = null;
    }
  }
  