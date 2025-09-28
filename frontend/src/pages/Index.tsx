import { useState } from "react";
import { Card } from "@/components/ui/card";
import { EmailUpload } from "@/components/EmailUpload";
import { EmailInput } from "@/components/EmailInput";
import { ClassificationResult } from "@/components/ClassificationResult";
import { Header } from "@/components/Header";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Mail, FileText, Zap, TrendingUp } from "lucide-react";

interface ClassificationData {
  category: 'productive' | 'unproductive';
  confidence: number;
  suggestedResponse: string;
  originalContent: string;
}

const Index = () => {
  const [classificationResult, setClassificationResult] = useState<ClassificationData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleEmailProcess = async (content: string, source: string) => {
    setIsLoading(true);
    
    // Simulate AI processing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock classification logic
    const isProductive = content.toLowerCase().includes('suporte') || 
                        content.toLowerCase().includes('solicitação') ||
                        content.toLowerCase().includes('problema') ||
                        content.toLowerCase().includes('urgente') ||
                        content.toLowerCase().includes('status') ||
                        content.toLowerCase().includes('andamento');
    
    const mockResult: ClassificationData = {
      category: isProductive ? 'productive' : 'unproductive',
      confidence: Math.random() * 0.3 + 0.7, // 70-100%
      suggestedResponse: isProductive 
        ? "Obrigado pelo seu contato. Recebemos sua solicitação e nossa equipe irá analisá-la em breve. Você receberá uma resposta em até 24 horas úteis com o status atualizado."
        : "Obrigado pela sua mensagem. Ficamos felizes em receber seu contato e desejamos tudo de bom para você também!",
      originalContent: content
    };
    
    setClassificationResult(mockResult);
    setIsLoading(false);
  };

  const resetResults = () => {
    setClassificationResult(null);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <section className="pt-20 pb-12 px-4" />

      <section className="px-4 pb-16">
        <div className="max-w-6xl mx-auto">
          <Card className="gradient-card border-card-border shadow-lg">
            <div className="p-8">
              <h2 className="text-3xl font-bold mb-8 text-center">
                Processe seu Email
              </h2>
              
              <Tabs defaultValue="upload" className="w-full">
                <TabsList className="grid w-full grid-cols-2 mb-8">
                  <TabsTrigger value="upload" className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    Upload de Arquivo
                  </TabsTrigger>
                  <TabsTrigger value="text" className="flex items-center gap-2">
                    <Mail className="w-4 h-4" />
                    Inserir Texto
                  </TabsTrigger>
                </TabsList>
                
                <TabsContent value="upload" className="space-y-6">
                  <EmailUpload 
                    onProcess={handleEmailProcess}
                    isLoading={isLoading}
                    onReset={resetResults}
                  />
                </TabsContent>
                
                <TabsContent value="text" className="space-y-6">
                  <EmailInput 
                    onProcess={handleEmailProcess}
                    isLoading={isLoading}
                    onReset={resetResults}
                  />
                </TabsContent>
              </Tabs>
              
              {classificationResult && (
                <div className="mt-8">
                  <ClassificationResult 
                    result={classificationResult}
                    onReset={resetResults}
                  />
                </div>
              )}
            </div>
          </Card>
        </div>
      </section>
    </div>
  );
};

export default Index;