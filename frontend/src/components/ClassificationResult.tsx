import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { CheckCircle, AlertTriangle, Copy, RotateCcw, TrendingUp, Mail } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { useState } from "react";

interface ClassificationData {
  category: string;
  confidence: number;
  suggested_reply: string;
  classify_source: string;
  reply_source?: string;
  originalContent: string;
}

interface ClassificationResultProps {
  result: ClassificationData;
  onReset: () => void;
}

export const ClassificationResult = ({ result, onReset }: ClassificationResultProps) => {
  const { toast } = useToast();
  const [file, setFile] = useState<File | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const copyResponse = () => {
    navigator.clipboard.writeText(result.suggested_reply);
    toast({
      title: "Resposta copiada!",
      description: "A resposta sugerida foi copiada para a área de transferência.",
    });
  };

  const isProductive = result.category === 'Produtivo';
  const confidencePercentage = Math.round(result.confidence * 100);

  const removeFile = () => {
    setFile(null);
    setUploadProgress(0);
    onReset();
  };

  return (
    <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
      <div className="text-center">
        <h3 className="text-2xl font-bold mb-2">Classificação Concluída</h3>
        <p className="text-muted-foreground">Análise realizada com sucesso pela IA</p>
      </div>

      <Card className="p-6 gradient-card border-card-border">
        <div className="flex items-center gap-4 mb-6">
          <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
            isProductive ? 'bg-productive/10' : 'bg-unproductive/10'
          }`}>
            {isProductive ? (
              <CheckCircle className="w-6 h-6 text-productive" />
            ) : (
              <AlertTriangle className="w-6 h-6 text-unproductive" />
            )}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h4 className="text-xl font-semibold">
                Email {isProductive ? 'Produtivo' : 'Improdutivo'}
              </h4>
              <Badge 
                variant={isProductive ? "default" : "secondary"}
                className={isProductive ? 'bg-productive hover:bg-productive/90' : 'bg-unproductive hover:bg-unproductive/90'}
              >
                {isProductive ? 'Produtivo' : 'Improdutivo'}
              </Badge>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm text-muted-foreground">
                Confiança: {confidencePercentage}%
              </span>
              <div className="flex-1 bg-muted rounded-full h-2 ml-2">
                <div 
                  className={`h-2 rounded-full transition-all duration-1000 ${
                    isProductive ? 'bg-productive' : 'bg-unproductive'
                  }`}
                  style={{ width: `${confidencePercentage}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className={`p-4 rounded-lg ${
          isProductive ? 'bg-productive-bg border border-productive/20' : 'bg-unproductive-bg border border-unproductive/20'
        }`}>
          <p className="text-sm font-medium mb-2">
            {isProductive ? '✅ Este email requer ação ou resposta' : '⚠️ Este email não requer ação imediata'}
          </p>
          <p className="text-xs text-muted-foreground">
            {isProductive 
              ? 'Classificado como produtivo com base no conteúdo que indica necessidade de suporte, informações ou ações específicas.'
              : 'Classificado como improdutivo pois aparenta ser uma mensagem social, comemorativa ou não relacionada a processos de trabalho.'
            }
          </p>
        </div>
      </Card>

      <Card className="p-6 border-card-border">
        <div className="flex items-center gap-2 mb-4">
          <Mail className="w-5 h-5 text-primary" />
          <h4 className="text-lg font-semibold">Resposta Sugerida</h4>
        </div>
        
        <div className="bg-muted/50 rounded-lg p-4 mb-4">
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {result.suggested_reply}
          </p>
        </div>
        
        <div className="flex gap-2">
          <Button onClick={copyResponse} variant="outline" size="sm">
            <Copy className="w-4 h-4 mr-2" />
            Copiar Resposta
          </Button>
        </div>
      </Card>

      <div className="flex justify-center pt-4">
        <Button onClick={onReset} variant="outline" size="lg">
          <RotateCcw className="w-4 h-4 mr-2" />
          Processar Novo Email
        </Button>
      </div>
    </div>
  );
};