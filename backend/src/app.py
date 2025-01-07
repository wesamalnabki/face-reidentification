import io
import os
import uuid

from PIL import Image
from fastapi import FastAPI, UploadFile, File, Form

from backend.src.sql_db_manager import SQLDBManager
from backend.src.utils import save_image
from backend.src.vector_db_manager import VectorDBManager

top_search_matches = 5
sql_dp_path = os.getenv("SQL_DB_PATH")

app = FastAPI()
sql_db_manager = SQLDBManager()
vector_db_manager = VectorDBManager()


@app.post("/search_face/")
async def process_face(file: UploadFile = File(...)):
    # Read and process the image
    image_data = await file.read()
    image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")

    # Search in Chroma collection
    results = vector_db_manager.query_db(image_pil)

    # Check for matches
    matches = []
    for face_id, face_distance in zip(results['ids'][0], results['distances'][0]):
        sim_score = round(1 - face_distance, 2)
        if sim_score >= float(os.getenv("FACE_DISTANCE_THRESHOLD")):
            person_info = sql_db_manager.get_person_by_face_id(face_id)
            person_info.update({"sim_score": sim_score})
            if person_info:
                matches.append(person_info)
    return {"matches": matches}


@app.post("/link_face/")
async def link_face(file: UploadFile = File(...), person_id: str = Form(...)):
    # Read and process the image
    image_data = await file.read()
    image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")

    # save new face image
    face_id = str(uuid.uuid4())
    save_image(person_id, face_id, image_pil)

    # save image to vector DB:
    vector_db_manager.upsert_db(face_id, image_pil)

    # Insert MySQL Relation table:
    sql_db_manager.insert_face_relation(face_id, person_id)

    return {"message": "Face linked successfully"}


@app.post("/add_new_face/")
async def add_new_face(file: UploadFile = File(...), first_name: str = Form(...), last_name: str = Form(...),
                       date_of_birth: str = Form(None), country: str = Form(None), city: str = Form(None)):
    # Read and process the image
    image_data = await file.read()
    image_pil = Image.open(io.BytesIO(image_data)).convert("RGB")

    # Insert new face
    person_id = str(uuid.uuid4())
    sql_db_manager.insert_person(person_id, first_name, last_name, date_of_birth, country, city)
    face_id = str(uuid.uuid4())
    sql_db_manager.insert_face_relation(face_id, person_id)
    vector_db_manager.upsert_db(face_id, image_pil)
    save_image(person_id, face_id, image_pil)

    return {"message": "Face inserted successfully", "personID": person_id, "faceID": face_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
