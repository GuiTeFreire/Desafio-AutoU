import { useState, forwardRef, useImperativeHandle } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Mail, MessageSquare, RotateCcw } from "lucide-react";
import { ApiService } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

interface ClassificationData {
  category: string;
  confidence: number;
  suggested_reply: string;
  classify_source: string;
  reply_source?: string;
  originalContent: string;
}

interface EmailInputProps {
  onProcess: (result: ClassificationData) => void;
  isLoading: boolean;
  onReset: () => void;
  onLoadingChange: (loading: boolean) => void;
}

export interface EmailInputRef {
  clearContent: () => void;
}

export const EmailInput = forwardRef<EmailInputRef, EmailInputProps>(
  ({ onProcess, isLoading, onReset, onLoadingChange }, ref) => {
  const [content, setContent] = useState("");
  const [subject, setSubject] = useState("");
  const { toast } = useToast();

  const handleProcess = async () => {
    if (!content.trim()) return;
    
    const fullContent = subject.trim() 
      ? `Assunto: ${subject}\n\n${content}`
      : content;
    
    try {
      onLoadingChange(true);
      const apiResult = await ApiService.processEmailText(fullContent);
      const result: ClassificationData = {
        ...apiResult,
        originalContent: fullContent
      };
      onProcess(result);
    } catch (error) {
      toast({
        title: "Erro ao processar email",
        description: error instanceof Error ? error.message : "Erro desconhecido",
        variant: "destructive"
      });
    } finally {
      onLoadingChange(false);
    }
  };

  const handleClear = () => {
    setContent("");
    setSubject("");
    onReset();
  };

  const clearContent = () => {
    setContent("");
    setSubject("");
  };

  useImperativeHandle(ref, () => ({
    clearContent
  }));

  return (
    <div className="space-y-6">
      <Card className="p-6 gradient-card border-card-border">
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-4">
            <MessageSquare className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold">Inserir Email Manualmente</h3>
          </div>

          <div className="space-y-2">
            <Label htmlFor="subject">Assunto (opcional)</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
              <input
                id="subject"
                type="text"
                placeholder="Assunto do email..."
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-input-border rounded-lg bg-input focus:outline-none focus:ring-2 focus:ring-ring transition-smooth"
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="content">Conteúdo do Email *</Label>
            <Textarea
              id="content"
              placeholder="Cole ou digite o conteúdo do email aqui..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="min-h-[150px] resize-none"
              maxLength={5000}
            />
            <div className="flex justify-between text-sm text-muted-foreground">
              <span>Mínimo 10 caracteres</span>
              <span>{content.length}/5000</span>
            </div>
          </div>

          <div className="flex gap-3 pt-2">
            <Button 
              onClick={handleProcess}
              disabled={isLoading || content.trim().length < 10}
              className="flex-1"
            >
              {isLoading ? 'Processando...' : 'Classificar Email'}
            </Button>
            
            <Button 
              variant="outline" 
              onClick={handleClear}
              disabled={isLoading}
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              Limpar
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
});