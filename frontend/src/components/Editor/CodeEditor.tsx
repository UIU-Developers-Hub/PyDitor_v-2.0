// src/components/Editor/CodeEditor.tsx
import React from 'react';
import AceEditor from 'react-ace';
import { AlertCircle, Code2, Save } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

// Import modes
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/mode-javascript';
import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/mode-c_cpp';
import 'ace-builds/src-noconflict/mode-html';
import 'ace-builds/src-noconflict/mode-css';

// Import themes
import 'ace-builds/src-noconflict/theme-monokai';
import 'ace-builds/src-noconflict/theme-github';

// Import extensions
import 'ace-builds/src-noconflict/ext-language_tools';
import 'ace-builds/src-noconflict/ext-searchbox';

interface EditorProps {
  code: string;
  language?: string;
  theme?: 'dark' | 'light';
  onChange?: (value: string) => void;
  onSave?: (value: string) => void;
}

const getModeForLanguage = (language: string): string => {
  switch (language.toLowerCase()) {
    case 'python':
      return 'python';
    case 'javascript':
    case 'typescript':
      return 'javascript';
    case 'java':
      return 'java';
    case 'cpp':
    case 'c++':
      return 'c_cpp';
    case 'html':
      return 'html';
    case 'css':
      return 'css';
    default:
      return 'python';
  }
};

const CodeEditor: React.FC<EditorProps> = ({
  code,
  language = 'python',
  theme = 'dark',
  onChange,
  onSave
}) => {
  const [error, setError] = React.useState<string>('');
  const editorRef = React.useRef<any>(null);

  const handleChange = React.useCallback(
    (value: string) => {
      try {
        onChange?.(value);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to update code');
      }
    },
    [onChange]
  );

  const handleSave = React.useCallback(async () => {
    try {
      if (onSave) {
        await onSave(code);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save code');
    }
  }, [code, onSave]);

  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        handleSave();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleSave]);

  return (
    <div className="h-full w-full relative flex flex-col">
      {error && (
        <Alert variant="destructive" className="absolute top-0 right-0 m-4 z-50 max-w-md">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
      
      <div className="h-12 bg-gray-800 flex items-center px-4 border-b border-gray-700">
        <Code2 className="h-5 w-5 text-gray-400 mr-2" />
        <span className="text-sm text-gray-300">{language}</span>
        <div className="flex-1" />
        <Save 
          className="h-5 w-5 text-gray-400 cursor-pointer hover:text-white transition-colors"
          onClick={handleSave}
        />
      </div>

      <div className="flex-1 relative">
        <AceEditor
          ref={editorRef}
          mode={getModeForLanguage(language)}
          theme={theme === 'dark' ? 'monokai' : 'github'}
          onChange={handleChange}
          value={code}
          name="code-editor"
          width="100%"
          height="100%"
          fontSize={14}
          showPrintMargin={true}
          showGutter={true}
          highlightActiveLine={true}
          setOptions={{
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: true,
            showLineNumbers: true,
            tabSize: 4,
            useWorker: false,
            displayIndentGuides: true,
            printMarginColumn: 80,
            showInvisibles: false
          }}
          style={{
            fontFamily: 'JetBrains Mono, monospace',
            lineHeight: 1.5,
            position: 'absolute',
            top: 0,
            right: 0,
            bottom: 0,
            left: 0
          }}
        />
      </div>
    </div>
  );
};

export default CodeEditor;