# Horn Clause Deductive Engine Skill

Definite Horn clause reasoning system featuring forward chaining fixpoint derivation and goal-directed backward chaining search.

```mermaid
flowchart LR
    KB["Rule Base (Head :- Body)"] --> Forward["Forward Chaining (Data-Driven Fixpoint)"]
    Facts["Known Facts"] --> Forward
    Forward --> Derived["Derived Propositions"]
    
    Goal["Query Goal"] --> Backward["Backward Chaining (Goal-Directed SLD)"]
    KB --> Backward
    Backward --> Proof["Entailment Proof"]
```

## Features
- **100% Python Standard Library**: Linear-time forward chaining agenda algorithm.
- **Dual Inference Modes**: Forward propagation from facts or backward verification from goals.
- **Cycle Prevention**: Built-in branch history tracking.
