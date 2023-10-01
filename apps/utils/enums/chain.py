from .base import BaseEnum

class BlockchainConsensusType(BaseEnum):
    PROOF_OF_WORK = "(PoW)"
    PROOF_OF_STAKE ="(PoS)"
    DELEGATED_PROOF_OF_STAKE= "(DPoS)"
    PROOF_OF_AUTHORITY = "(PoA)"
    PROOF_OF_SPACE_AND_TIME = "(PoST)"
    PROOF_OF_HISTORY = "(PoH)"
    PROOF_OF_ELASPSED_TIME = "(PoET)"
    PRATICAL_BYZANTINE_FAULT_TOLERANCE = "(PBFT)"
    DIRECTED_ACYCLIC_GRAPH = "(DAG)"