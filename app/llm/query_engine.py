from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
DB_DIR = "chroma_db"

# Load CPU-friendly LLM
MODEL_NAME = "EleutherAI/gpt-neo-125M"
print("[INFO] Loading lightweight model for inference...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token  # Avoid padding errors

model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
model.to("cpu")

def retrieve_and_answer(query: str, k: int = 3) -> dict:
    db = Chroma(persist_directory=DB_DIR, embedding_function=embedding_model)
    docs = db.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])

    if not context:
        return {
            "answer": "No relevant context found.",
            "sources": []
        }

    prompt = f"""Use ONLY the context below to answer the user's question. If the answer is not contained, say "I don't know".

Context:
{context}

Question: {query}

Answer:"""

    print("[INFO] Running inference...")
    print("[DEBUG] Retrieved context:\n", context[:1000])  # Optional: Show first 1000 chars

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024, padding=True).to("cpu")
    input_ids = inputs["input_ids"]

    try:
        with torch.no_grad():
            outputs = model.generate(
                input_ids=input_ids,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
            )
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = output_text.split("Answer:")[-1].strip()
    except Exception as e:
        print("[ERROR] Failed during inference:", str(e))
        return {
            "answer": "Failed to generate response.",
            "sources": []
        }

    return {
        "answer": answer,
        "sources": list(set(doc.metadata["source"] for doc in docs))
    }


