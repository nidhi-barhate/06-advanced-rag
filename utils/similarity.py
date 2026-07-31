import numpy as np

class Similarity:

    @staticmethod
    def cosine(vector1, vector2):

        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        similarity = np.dot(vector1, vector2) / (
            np.linalg.norm(vector1)
            * np.linalg.norm(vector2)
        )

        return float(similarity)