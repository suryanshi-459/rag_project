from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.pdf_loader import extract_text_from_pdf
from app.embeddings.chunker import chunk_text
from app.embeddings.embedder import embed_and_store

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    contents = await file.read()
    
    # Extract text
    text = extract_text_from_pdf(contents)
    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in the PDF.")
    
    # Chunk text
    chunks = chunk_text(text)
    if not chunks:
        raise HTTPException(status_code=400, detail="No text chunks were created from the PDF.")
    # Embed and store in vector DB
    embed_and_store(chunks, file.filename)

    return {"message": f"{file.filename} uploaded and processed successfully."}
