import insightface
import numpy as np

__all__ = [
    'FaceProcess'
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
