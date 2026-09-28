"""Definite Horn Clause Inference Engine.
100% Python Standard Library.
"""

class HornEngine:
    """Deductive inference for propositional definite Horn clauses.
    Clause format: {'head': 'P', 'body': ['Q', 'R']}
    """
    def __init__(self, clauses, facts=None):
        self.clauses = clauses
        self.facts = set(facts or [])

    def forward_chain(self, query):
        """Forward chaining algorithm reaching fixpoint."""
        inferred = set(self.facts)
        count = {i: len(c['body']) for i, c in enumerate(self.clauses)}
        agenda = list(self.facts)
        
        while agenda:
            p = agenda.pop()
            if p == query:
                return True
            for i, c in enumerate(self.clauses):
                if p in c['body']:
                    count[i] -= 1
                    if count[i] == 0:
                        head = c['head']
                        if head not in inferred:
                            inferred.add(head)
                            agenda.append(head)
        return query in inferred

    def backward_chain(self, query, visited=None):
        """Goal-directed backward chaining with cycle detection."""
        if visited is None:
            visited = set()
        if query in self.facts:
            return True
        if query in visited:
            return False
        visited.add(query)
        
        for c in self.clauses:
            if c['head'] == query:
                if all(self.backward_chain(b, visited.copy()) for b in c['body']):
                    return True
        return False
