// src/services/terminalService.ts
export class TerminalService {
    private ws: WebSocket | null = null;
    private reconnectAttempts = 0;
    private readonly MAX_RECONNECT_ATTEMPTS = 5;
    private closeListeners: ((event: CloseEvent) => void)[] = [];

    constructor(
        private terminalId: string,
        private onData: (data: string) => void
    ) {}

    addCloseListener(listener: (event: CloseEvent) => void) {
        this.closeListeners.push(listener);
    }

    connect() {
        const token = localStorage.getItem('token');
        if (!token) {
            console.error('No authentication token found');
            return;
        }

        this.ws = new WebSocket(
            `ws://localhost:8000/ws/terminal/${this.terminalId}?token=${token}`
        );

        this.ws.onopen = () => {
            console.log('Terminal connected:', this.terminalId);
            this.reconnectAttempts = 0;
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'output') {
                    this.onData(data.content);
                }
            } catch (error) {
                console.error('Error processing message:', error);
            }
        };

        this.ws.onclose = (event) => {
            this.closeListeners.forEach(listener => listener(event));

            if (event.code === 4003) {
                console.error('Authentication failed');
                return;
            }

            if (this.reconnectAttempts < this.MAX_RECONNECT_ATTEMPTS) {
                setTimeout(() => {
                    this.reconnectAttempts++;
                    this.connect();
                }, 1000 * this.reconnectAttempts);
            }
        };
    }

    sendInput(data: string) {
        if (this.ws?.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'input',
                content: data
            }));
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.closeListeners = [];
    }
}
