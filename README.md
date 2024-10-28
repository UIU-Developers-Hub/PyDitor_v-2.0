# PyDitor v2.0

## Overview
**PyDitor**  is a multi-language Integrated Development Environment (IDE) available as both a desktop application and web platform. Built with Electron, React, and FastAPI, it provides a comprehensive development environment with support for multiple programming languages.

## Distribution Types

## 1. Desktop Application (Primary)
- Standalone executable for Windows, macOS, and Linux
- Local file system access
- Integrated terminal support
- Offline functionality
- Native performance

## 2. Web Application (Secondary)
- Browser-based access
- Cloud storage integration
- Real-time collaboration
- Cross-platform compatibility
# PyDitor v2.0

**PyDitor** is a Python IDE Backend API designed to support code execution, file management, and real-time collaboration. This README outlines its current features, future plans, and licensing details.

## Component Diagram

Below is a high-level component diagram illustrating the architecture of PyDitor.

```mermaid
graph TD
    A[PyDitor API] -->|HTTP| B[Code Execution Service]
    A -->|HTTP| C[File Management Service]
    A -->|WebSocket| D[Real-Time Collaboration Service]
    B --> E[Execution Engine]
    C --> F[File Storage]
    D --> G[Collaboration Database]

    subgraph Backend
        B
        C
        D
    end

    subgraph Services
        E
        F
        G
    end

## Supported Languages

### Current Support
1. **Python**
   ```python
   print("Hello, World!")
   ```
   - Full language support
   - Built-in package management
   - Virtual environment integration

2. **C++**
   ```cpp
   #include <iostream>
   int main() {
       std::cout << "Hello, World!" << std::endl;
       return 0;
   }
   ```
   - Compilation support
   - Standard library integration
   - Debug symbols

3. **Java**
   ```java
   public class Main {
       public static void main(String[] args) {
           System.out.println("Hello, World!");
       }
   }
   ```
   - JDK integration
   - Class management
   - Package support

4. **JavaScript**
   ```javascript
   console.log("Hello, World!");
   ```
   - Node.js support
   - NPM integration
   - Modern ES features

## Core Features

### 1. Code Editor
- Monaco Editor integration
- Multi-language syntax highlighting
- Code completion
- Error diagnostics
- Multiple themes
```javascript
// Editor Configuration
{
    theme: "vs-dark",
    language: "python",
    automaticLayout: true,
    minimap: { enabled: true }
}
```

### 2. File Management
- Local file system integration
- Project workspace
- File tree navigation
- Auto-save functionality
```typescript
interface FileSystem {
    readFile(path: string): Promise<string>;
    writeFile(path: string, content: string): Promise<void>;
    listFiles(directory: string): Promise<string[]>;
}
```

### 3. Code Execution
- Multi-language execution support
- Output streaming
- Error handling
- Execution timeout management
```python
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
```

### 4. Development Tools
- Integrated terminal
- Git integration
- Package management
- Debug support

## Architecture

### Desktop Application Structure
```
pyditor-v2/
├── electron/
│   ├── main.js              # Electron main process
│   └── preload.js           # Preload scripts
├── src/
│   ├── components/          # React components
│   ├── services/            # Frontend services
│   └── App.tsx              # Main React app
├── backend/
│   ├── app/
│   │   ├── core/           # Core backend services
│   │   ├── services/       # Language services
│   │   └── routers/        # API routes
│   └── run.py              # Backend entry point
└── package.json            # Project configuration
```

### Key Components
1. **Electron Main Process**
   - Window management
   - Native API access
   - Backend process management

2. **Frontend (React)**
   - User interface
   - Editor integration
   - State management

3. **Backend (FastAPI)**
   - Code execution
   - File operations
   - Language services

## Installation

### Desktop Installation
```bash
# Download the installer
PyDitor-Setup-2.0.0.exe  # Windows
PyDitor-2.0.0.dmg        # macOS
PyDitor-2.0.0.AppImage   # Linux

# Or build from source
npm install
npm run package
```

### Development Setup
```bash
# Clone repository
git clone https://github.com/username/pyditor-v2.git

# Install dependencies
npm install
pip install -r requirements.txt

# Start development
npm start
```

## Configuration

### Language Configuration
```json
{
    "languages": {
        "python": {
            "path": "python",
            "extensions": [".py"],
            "packageManager": "pip"
        },
        "cpp": {
            "path": "g++",
            "extensions": [".cpp", ".h"],
            "compilerFlags": ["-std=c++17"]
        }
    }
}
```

### Editor Settings
```json
{
    "editor": {
        "theme": "vs-dark",
        "fontSize": 14,
        "tabSize": 4,
        "autoSave": true
    }
}
```

## Features in Development

### 1. Language Support
- Rust integration
- Go support
- Ruby execution
- PHP development

### 2. Development Tools
- Integrated debugger
- Docker support
- Database tools
- Unit testing framework

### 3. Collaboration Features
- Real-time code sharing
- Voice/video chat
- Shared terminal
- Version control integration

## Performance Considerations

### Desktop Application
1. **Resource Management**
   - Memory usage optimization
   - CPU utilization control
   - Disk I/O management

2. **Startup Performance**
   - Lazy loading
   - Caching strategies
   - Background processes

### Multi-language Support
1. **Compilation Management**
   - Parallel compilation
   - Incremental builds
   - Cache management

2. **Resource Isolation**
   - Process sandboxing
   - Memory limits
   - Execution timeouts

## Security

### Desktop Security
1. **File System Access**
   - Workspace isolation
   - Permission management
   - Safe file operations

2. **Code Execution**
   - Process isolation
   - Resource limitations
   - Sandboxed environments

## Future Scope

### 1. Extended Language Support
- TypeScript
- Swift
- Kotlin
- R language

### 2. Advanced Features
- AI code completion
- Refactoring tools
- Code analytics
- Performance profiling

### 3. Integration Capabilities
- Cloud deployment
- CI/CD pipelines
- Container orchestration
- Remote development

### 4. Collaborative Features
- Team workspaces
- Code review tools
- Pair programming
- Chat integration

## Development Guidelines

### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Submit pull request

### Code Style
```typescript
// Example component structure
import React from 'react';

interface EditorProps {
    language: string;
    content: string;
    onChange: (content: string) => void;
}

export const Editor: React.FC<EditorProps> = ({
    language,
    content,
    onChange
}) => {
    // Implementation
};
```
##Future Work
Our goal is to make PyDitor a robust, adaptable IDE backend with the following future enhancements:

AI Integration: Intelligent code suggestions and error handling.
Firebase Integration: Real-time data synchronization.
Docker Compatibility: Seamless deployment and scalability.
Remote Code Execution: Allow users to run code remotely, supporting multiple environments.
Plugin System: Extend functionality with customizable plugins.
Real-Time Collaboration Tools: Enable collaborative coding with live updates and shared sessions.
These enhancements will transform PyDitor into a comprehensive IDE backend capable of adapting to various developer needs.

##Author
GitHub: Sifat Ali
Email: sifatali0051@gmail.com

##License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software. See the LICENSE file for full license details.


MIT License

Copyright (c) 2024 Sifat Ali

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
