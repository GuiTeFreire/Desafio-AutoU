import { useState, useCallback } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Upload, FileText, X, CheckCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { ApiService } from "@/services/api";

interface ClassificationData {
  category: string;
  confidence: number;
  suggested_reply: string;
  classify_source: string;
  reply_source?: string;
  originalContent: string;
}

interface EmailUploadProps {
  onProcess: (result: ClassificationData) => void;
  isLoading: boolean;
  onReset: () => void;
  onLoadingChange: (loading: boolean) => void;
}

export const EmailUpload = ({ onProcess, isLoading, onReset, onLoadingChange }: EmailUploadProps) => {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const { toast } = useToast();

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFileSelect = (selectedFile: File) => {
    const allowedTypes = ['text/plain', 'application/pdf'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!allowedTypes.includes(selectedFile.type)) {
      toast({
        title: "Tipo de arquivo inválido",
        description: "Por favor, selecione apenas arquivos .txt ou .pdf",
        variant: "destructive"
      });
      return;
    }

    if (selectedFile.size > maxSize) {
      toast({
        title: "Arquivo muito grande",
        description: "O arquivo deve ter no máximo 10MB",
        variant: "destructive"
      });
      return;
    }

    setFile(selectedFile);
    simulateUpload();
  };

  const simulateUpload = () => {
    setUploadProgress(0);
    const interval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          return 100;
        }
        return prev + 10;
      });
    }, 100);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const processFile = async () => {
    if (!file) return;

    try {
      onLoadingChange(true);
      const apiResult = await ApiService.processEmailFile(file);
      const result: ClassificationData = {
        ...apiResult,
        originalContent: `Arquivo: ${file.name}`
      };
      onProcess(result);
    } catch (error) {
      toast({
        title: "Erro ao processar arquivo",
        description: error instanceof Error ? error.message : "Erro desconhecido",
        variant: "destructive"
      });
    } finally {
      onLoadingChange(false);
    }
  };

  const readFileContent = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target?.result as string;
        resolve(content);
      };
      reader.onerror = () => reject(new Error("Erro ao ler arquivo"));
      reader.readAsText(file);
    });
  };

  const removeFile = () => {
    setFile(null);
    setUploadProgress(0);
    onReset();
  };

  return (
    <div className="space-y-6">
      {!file ? (
        <Card
          className={`p-8 border-2 border-dashed transition-all duration-300 ${
            dragActive 
              ? 'border-primary bg-primary/5 shadow-glow' 
              : 'border-card-border hover:border-primary/50 hover:bg-primary/5'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="text-center">
            <div className="mb-4 flex justify-center">
              <div className={`w-16 h-16 rounded-full flex items-center justify-center transition-all ${
                dragActive ? 'bg-primary shadow-glow' : 'bg-muted'
              }`}>
                <Upload className={`w-8 h-8 ${dragActive ? 'text-white' : 'text-muted-foreground'}`} />
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-2">
              {dragActive ? 'Solte o arquivo aqui' : 'Faça upload do seu email'}
            </h3>
            <p className="text-muted-foreground mb-6">
              Arraste e solte ou clique para selecionar<br />
              <span className="text-sm">Formatos aceitos: .txt, .pdf (máx. 10MB)</span>
            </p>
            <input
              type="file"
              accept=".txt,.pdf"
              onChange={handleFileInput}
              className="hidden"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <Button variant="outline" asChild>
                <span>Selecionar Arquivo</span>
              </Button>
            </label>
          </div>
        </Card>
      ) : (
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                <FileText className="w-5 h-5 text-primary" />
              </div>
              <div>
                <h4 className="font-medium">{file.name}</h4>
                <p className="text-sm text-muted-foreground">
                  {(file.size / 1024).toFixed(1)} KB
                </p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={removeFile}>
              <X className="w-4 h-4" />
            </Button>
          </div>

          {uploadProgress < 100 ? (
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Carregando...</span>
                <span>{uploadProgress}%</span>
              </div>
              <Progress value={uploadProgress} className="w-full" />
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-productive">
                <CheckCircle className="w-4 h-4" />
                <span className="text-sm font-medium">Arquivo carregado com sucesso</span>
              </div>
              
              <Button 
                onClick={processFile} 
                disabled={isLoading}
                className="w-full"
              >
                {isLoading ? 'Processando...' : 'Classificar Email'}
              </Button>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};