"""Example demonstrating Horn clause inference."""
from client import HornEngine

def main():
    # Knowledge base:
    # Q :- P
    # S :- Q, R
    clauses = [
        {'head': 'Q', 'body': ['P']},
        {'head': 'S', 'body': ['Q', 'R']}
    ]
    facts = ['P', 'R']
    engine = HornEngine(clauses, facts)
    print("Facts:", facts)
    print("Is 'S' entailed (Forward)?", engine.forward_chain('S'))
    print("Is 'S' entailed (Backward)?", engine.backward_chain('S'))

if __name__ == "__main__":
    main()
