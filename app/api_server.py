from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.groq_helper import search_and_summarize
import uvicorn

app = FastAPI()

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
def search_patents(request: SearchRequest):
    try:
        summaries = search_and_summarize(request.query)
        if not summaries:
            raise HTTPException(status_code=404, detail="No relevant patents found.")
        return {"query": request.query, "results": summaries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)
