import insightface
import numpy as np
import requests

from backend.src.utils import numpy_to_base64

__all__ = [
    'FaceProcess',
    "FaceProcess_DeepFace"
]


class FaceProcess:
    def __init__(self):
        # Initialize insightface model
        ctx_id = 0
        self.model = insightface.app.FaceAnalysis(name="buffalo_l",
                                                  providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.model.prepare(ctx_id=ctx_id, det_size=(640, 640))

    # Utility functions
    def get_face_embedding(self, image_np: np.array):
        faces = self.model.get(image_np, max_num=1)
        if len(faces) == 0:
            return None
            # raise HTTPException(status_code=400, detail="No face detected in the image.")
        face_embedding = faces[0].normed_embedding
        # face_embedding: object = face_embedding / np.linalg.norm(face_embedding)
        return face_embedding


class FaceProcess_DeepFace:
    def __init__(self):
        self.url_path = "http://localhost:5000/represent"

    # Utility functions
    def get_face_embedding(self, image_np: np.array):
        img_base64 = numpy_to_base64(image_np)

        data = {
            "model_name": "VGG-Face",
            "align": True,
            "max_faces": "1",
            "silent": True,
            "enforce_detection": False,
            "img_path": "data:image/png;base64, " + img_base64,
        }

        response = requests.post(self.url_path, json=data)
        face_embedding = np.array(response.json()['results'][0]['embedding'])
        # face_embedding: object = face_embedding / np.linalg.norm(face_embedding)
        return face_embedding
