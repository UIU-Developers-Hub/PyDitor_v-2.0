// src/workers/terminalWorker.ts

const terminalWorker = () => {
    let ws: WebSocket | null = null;
    let messageQueue: string[] = [];
    let processTimer: ReturnType<typeof setTimeout> | null = null;  // Updated type to support Node.js and browser
  
    // Process message queue every 16ms (60fps)
    const processMessageQueue = () => {
      if (messageQueue.length > 0) {
        const batch = messageQueue.splice(0, 100); // Process 100 messages at a time
        self.postMessage({ type: 'output', data: batch });
      }
      processTimer = setTimeout(processMessageQueue, 16);
    };
  
    self.onmessage = (event) => {
      const { type, data } = event.data;
  
      switch (type) {
        case 'connect':
          ws = new WebSocket(`ws://localhost:8000/ws/terminal/${data.terminalId}`);
          ws.onmessage = (wsEvent) => {
            messageQueue.push(wsEvent.data);
            if (!processTimer) {
              processMessageQueue();
            }
          };
          break;
  
        case 'command':
          if (ws?.readyState === WebSocket.OPEN) {
            ws.send(
              JSON.stringify({
                type: 'command',
                content: data.command,
              })
            );
          }
          break;
  
        case 'disconnect':
          if (ws) {
            ws.close();
            ws = null;
          }
          if (processTimer) {
            clearTimeout(processTimer);
            processTimer = null;
          }
          break;
      }
    };
  };
  
  export default terminalWorker;
  