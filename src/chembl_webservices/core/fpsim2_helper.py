from FPSim2 import FPSim2Engine
from django.conf import settings

fpe = FPSim2Engine(settings.FPSIM2_FILE_PATH)

def get_similar_molregnos(query_smiles, similarity=0.7):
    """
    :param query_smiles: the smiles representation of the query
    :param similarity: the minimum similarity threshold
    :return: a list with tuples of (molregno, similarity)
    """
    if similarity < 0.7 or similarity > 1:
        raise ValueError('Similarity should have a value between 0.7 and 1.')

    return fpe.similarity(query_smiles, similarity, n_workers=1)
