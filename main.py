from fastapi import FastAPI, status
from decouple import config
from supabase import create_client, Client
from pydantic import BaseModel
import random

url = config("SUPABASE_URL")
key = config("SUPABASE_KEY")


app = FastAPI()
supabase: Client = create_client(url, key)


@app.get("/learningstyle/")
def get_learningstyle():
    learningstyle = supabase.table("learningstyle").select("*").execute()
    return learningstyle

class learningstyleSchema(BaseModel):
    dominantStyle : str
    confidence : float
    recommendedFormat : str
    detectedShift : bool

class updatelearningstyleSchema(BaseModel):
    dominantStyle : str
    confidence : float
    recommendedFormat : str
    detectedShift : bool

@app.get("/learningstyle/{id}")
def get_learning(id : int):
    learning = supabase.table("learningstyle").select("*").eq("id", id).execute()
    return learning

@app.post("/learningstyle/", status_code=status.HTTP_201_CREATED)
def create_learningstyle(learning: learningstyleSchema):
    learning = supabase.table("learningstyle").insert({
        "dominantStyle" : learning.dominantStyle,
        "confidence" : learning.confidence,
        "recommendedFormat": learning.recommendedFormat,
        "detectedShift": learning.detectedShift
    }).execute()

    if not learning.data:
        return {"message": "No record found or insert failed"}

    return {
        "message": "Learning style added successfully", "data": learning.data }

@app.delete("/learningstyle/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_learning(id: str):
    learning = supabase.table("learningstyle").delete().eq("id", id).execute()
    if not learning.data:
        return {"message": "No record found or delete failed"}

    return {"message": "Learning style deleted successfully", "data": learning.data}

@app.put("/learningstyle/", status_code=status.HTTP_202_ACCEPTED)
def create_learningstyle(id: int, learning: updatelearningstyleSchema):
    learning = supabase.table("learningstyle").update({
        "dominantStyle" : learning.dominantStyle,
        "confidence" : learning.confidence,
        "recommendedFormat": learning.recommendedFormat,
        "detectedShift": learning.detectedShift
    }).eq("id", id).execute()

    if not learning.data:
        return {"message": "No record found or update failed"}
    
    return {"message": "Learning style updated successfully", "data": learning.data}
