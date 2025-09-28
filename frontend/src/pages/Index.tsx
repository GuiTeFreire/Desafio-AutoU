import { useState } from "react";
import { Card } from "@/components/ui/card";
import { EmailUpload } from "@/components/EmailUpload";
import { EmailInput } from "@/components/EmailInput";
import { ClassificationResult } from "@/components/ClassificationResult";
import { Header } from "@/components/Header";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Mail, FileText } from "lucide-react";

interface ClassificationData {
  category: string;
  confidence: number;
  suggested_reply: string;
  classify_source: string;
  reply_source?: string;
  originalContent: string;
}

const Index = () => {
  const [classificationResult, setClassificationResult] = useState<ClassificationData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleEmailProcess = (result: ClassificationData) => {
    setClassificationResult(result);
  };

  const resetResults = () => {
    setClassificationResult(null);
  };

  const handleLoadingChange = (loading: boolean) => {
    setIsLoading(loading);
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
                    onLoadingChange={handleLoadingChange}
                  />
                </TabsContent>
                
                <TabsContent value="text" className="space-y-6">
                  <EmailInput 
                    onProcess={handleEmailProcess}
                    isLoading={isLoading}
                    onReset={resetResults}
                    onLoadingChange={handleLoadingChange}
                  />
                </TabsContent>
              </Tabs>
              
              {isLoading && (
                <div className="mt-8">
                  <Card className="p-8 text-center">
                    <div className="flex flex-col items-center space-y-4">
                      <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
                      <p className="text-muted-foreground">Processando email...</p>
                    </div>
                  </Card>
                </div>
              )}
              
              {classificationResult && !isLoading && (
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