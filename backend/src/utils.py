import os


def save_image(person_id, face_id, image_pil):
    folder_path = os.path.join(os.getenv("FACES_DB_PATH"), person_id)
    os.makedirs(folder_path, exist_ok=True)
    image_pil.save(os.path.join(folder_path, face_id + ".png"), "PNG")
