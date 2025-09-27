from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from pypdf import PdfReader
import io

from interfaces.api.schemas import ProcessEmailResponse
from use_cases.classify_email import ClassifyEmailUseCase, ClassifyEmailInput

router = APIRouter(tags=["emails"])

def _read_pdf_bytes(data: bytes) -> str:
    r = PdfReader(io.BytesIO(data))
    txt = []
    for p in r.pages:
        txt.append(p.extract_text() or "")
    return "\n".join(txt).strip()

@router.post("/process_email", response_model=ProcessEmailResponse)
async def process_email(request: Request, text: str | None = Form(None), file: UploadFile | None = File(None)) -> ProcessEmailResponse:
    if not text and not file:
        raise HTTPException(400, "Envie 'text' ou 'file' (.txt/.pdf).")
    content = text or ""
    if file:
        if file.filename.lower().endswith(".txt"):
            content = (await file.read()).decode("utf-8", errors="ignore")
        elif file.filename.lower().endswith(".pdf"):
            content = _read_pdf_bytes(await file.read())
        else:
            raise HTTPException(400, "Formato não suportado. Use .txt ou .pdf.")

    # Acessa o use case do estado da aplicação
    uc: ClassifyEmailUseCase = request.app.state.uc
    out = uc.execute(ClassifyEmailInput(text=content))
    return ProcessEmailResponse(**out.__dict__)
