from FPSim2 import FPSim2Engine
import time

# Variable loaded from the Settings to prevent circular references
FPSIM2_FILE_PATH = None
FPSIM_ENGINE = None

def get_fpsim_engine():
    global FPSIM_ENGINE, FPSIM2_FILE_PATH
    if FPSIM_ENGINE is None:
        t_ini = time.time()
        FPSIM_ENGINE = FPSim2Engine(FPSIM2_FILE_PATH)
        print('FPSIM2 FILE LOADED IN {0} SECS'.format(time.time()-t_ini))
    return FPSIM_ENGINE

def get_similar_molregnos(query_string, similarity=0.7):
    """
    :param query_string: the smiles, inchi or molfile representation of the query
    :param similarity: the minimum similarity threshold
    :return: a list with tuples of (molregno, similarity)
    """
    if similarity < 0.4 or similarity > 1:
        raise ValueError('Similarity should have a value between 0.4 and 1.')

    return get_fpsim_engine().similarity(query_string, similarity, n_workers=1)
