[English](README.md) · [Русский](README.ru.md)

# Adaptive Code Memory

> **Heterogeneous memory with adaptive information allocation for repository-level code reasoning**

**Status:** Research / Early Development  
**Category:** AI / Machine Learning / Code Intelligence / Representation Learning  
**Focus:** Latent representations, heterogeneous memory, information bottlenecks, adaptive compression, code reasoning, LLMs

---

# Overview

Modern language models can reason about source code surprisingly well, but large repositories create a fundamental information bottleneck.

A repository may contain tens or hundreds of thousands of tokens:

```text
Repository
├── source code
├── modules
├── classes
├── functions
├── dependencies
├── configuration
└── documentation
```

Traditional systems address this problem through larger context windows, retrieval-augmented generation, code search, graph-based retrieval, or context compression.

Another line of research attempts to compress repository information into compact latent representations.

This project explores a different hypothesis:

> **Repository knowledge is heterogeneous, so it may be fundamentally inefficient to compress all of it into a single representation.**

Code contains fundamentally different kinds of information:

```text
Semantic
"What does this component mean?"

Structural
"How are these components connected?"

Symbolic
"What is the exact function name?"

Behavioral
"What happens under this condition?"

Literal
"What is the exact value of this constant?"
```

These types of information have different properties and may require different representations.

Instead of forcing everything through one compression mechanism, this project investigates a **heterogeneous code memory** consisting of multiple complementary representations.

Conceptually:

```text
                         Repository
                             │
                             ▼
                     Code Understanding
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
          Semantic       Structural      Symbolic
           Memory          Memory          Memory
              │              │              │
              ▼              ▼              ▼
          Latents          Graph         Exact facts
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                     Adaptive Router
                             │
                             ▼
                    Information Budget
                             │
                             ▼
                        Receiver LLM
                             │
                             ▼
                           Answer
```

The central idea is not simply to compress more aggressively.

The goal is to investigate whether **different types of repository knowledge should be compressed, stored, and transmitted differently**.

---

# Research Question

The central research question is:

> **Can heterogeneous semantic, structural, and symbolic memory preserve more task-relevant repository information than monolithic compression when both systems operate under the same information budget?**

This leads to several subquestions:

- Does heterogeneous memory outperform a single latent bottleneck?
- Which types of code knowledge benefit from which representation?
- Can semantic information be stored efficiently in continuous latent representations?
- Is structural information better represented explicitly as a graph?
- Is exact symbolic information better preserved deterministically?
- Can a learned router dynamically allocate memory according to the question?
- Can the system use progressively more information only when necessary?
- Does adaptive allocation improve information efficiency?
- Does the learned memory transfer between different receiver models?
- Can counterfactual experiments verify that answers actually depend on the stored memory?
- How much performance can be obtained per unit of information budget?

---

# Motivation

Large codebases contain different kinds of information that behave very differently under compression.

Consider the following function:

```python
def authenticate_user(token):
    if not verify_signature(token):
        raise AuthenticationError()
    return get_user_from_token(token)
```

A system may need to answer:

> What does this function do?

This primarily requires **semantic information**.

But another question might be:

> Which function does `authenticate_user()` call?

This requires **structural information**.

Another question:

> What is the exact name of the exception?

This requires **symbolic information**.

And:

> What happens when signature verification fails?

This requires **behavioral information**.

A single latent representation must implicitly encode all of these.

That may be possible, but it may not be optimal.

The central hypothesis of this project is therefore:

> **The information structure of software is heterogeneous, and memory architecture should reflect that heterogeneity.**

---

# Core Hypothesis

The primary hypothesis is:

> **Under a fixed information budget, an adaptive heterogeneous memory that distributes capacity between semantic, structural, and symbolic representations will preserve more task-relevant information than a monolithic latent representation or uniform compression strategy.**

The hypothesis can be represented as:

```text
                    Fixed Information Budget
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
         Semantic         Structural        Symbolic
          Memory            Memory            Memory
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                       Adaptive Allocation
                              │
                              ▼
                         Receiver LLM
```

The system does not assume that every question requires the same kind of information.

For example:

```text
Question:
"How does authentication work?"

Semantic      ████████████████████
Structural    █████
Symbolic      ██
```

while:

```text
Question:
"Where is validate_token() called?"

Semantic      ███
Structural    ████████████████████
Symbolic      ████
```

and:

```text
Question:
"What is the exact timeout constant?"

Semantic      █
Structural    ██
Symbolic      █████████████████████
```

The allocation above is illustrative rather than a predetermined design.

The experiments must determine whether such specialization is actually beneficial.

---

# Important Research Position

This project does **not** assume that latent memory is inherently superior to retrieval.

Recent work has already demonstrated that repository-level context compression can be approached through multiple paradigms, including discrete token compression, continuous latent representations, and other compressed representations.

Similarly, adaptive code compression and repository-aware retrieval are active research areas.

Therefore, the goal is not:

> "We invented code compression."

Nor:

> "Latent representations replace RAG."

Instead, the project investigates a narrower question:

> **Does representing different classes of code knowledge differently provide an advantage when the total information budget is constrained?**

This distinction is central to the research.

---

# What Is Heterogeneous Code Memory?

The proposed memory consists of several complementary components.

## 1. Semantic Memory

Semantic memory attempts to capture high-level meaning.

Potential information includes:

- what a function does;
- what a module is responsible for;
- the purpose of a component;
- high-level behavior;
- conceptual relationships;
- implementation intent.

A possible representation is a learned continuous latent memory:

```text
Code
 │
 ▼
Semantic Encoder
 │
 ▼
z₁ z₂ z₃ ... zₖ
```

The representation does not need to correspond directly to textual tokens.

---

# 2. Structural Memory

Structural memory represents relationships between components.

Examples include:

```text
imports
calls
inherits
implements
references
depends_on
contains
```

Conceptually:

```text
A ──calls──► B
B ──imports─► C
D ──inherits► A
```

A graph representation can preserve information that may be unnecessarily expensive to encode into continuous latent vectors.

Possible structural memory:

```text
Repository
    │
    ▼
AST / static analysis
    │
    ▼
Code Graph
    │
    ▼
Graph Representation
```

The exact implementation is an experimental variable.

---

# 3. Symbolic Memory

Symbolic memory stores information where exactness matters.

Examples:

```text
function names
class names
argument counts
types
constants
literals
file paths
imports
line references
```

For example:

```text
{
    "function": "validate_token",
    "arity": 2,
    "file": "auth/token.py"
}
```

A key design principle is:

> **Do not force a neural network to approximate information that a deterministic program can preserve exactly.**

For supported languages, AST or compiler tooling may provide a deterministic source of symbolic facts.

However, symbolic memory itself can still be compressed or selectively stored under a limited budget.

---

# 4. Behavioral Memory

Behavioral information sits between semantic and structural representations.

Examples:

```text
condition
    ↓
branch
    ↓
side effect
    ↓
exception / return value
```

A possible future extension is to explicitly model control-flow or behavioral representations.

This component is intentionally not assumed to be necessary from the beginning.

The research should determine whether behavioral knowledge is adequately captured by semantic and structural memory.

---

# Why Not Just Use One Encoder?

A monolithic architecture looks like:

```text
Repository
    │
    ▼
Encoder
    │
    ▼
128 latent units
    │
    ▼
LLM
```

This has a simple interface, but the same latent capacity must encode:

```text
meaning
structure
identifiers
literals
relationships
behavior
```

The proposed architecture instead treats the repository as a collection of different information types:

```text
Repository
    │
    ├──► Semantic Memory
    │
    ├──► Structural Memory
    │
    └──► Symbolic Memory
```

The research question is whether this decomposition provides better information efficiency.

---

# Adaptive Information Budget

The most important component of the proposed system is the **adaptive information budget**.

Suppose the total memory budget is:

```text
B = 128 units
```

A conventional system might always allocate:

```text
Semantic      64
Structural    32
Symbolic      32
```

regardless of the question.

Our proposed system allows the allocation to change.

For example:

```text
Question A

Semantic      80
Structural    32
Symbolic      16
```

and:

```text
Question B

Semantic      24
Structural    88
Symbolic      16
```

The total remains:

```text
80 + 32 + 16 = 128

24 + 88 + 16 = 128
```

The important constraint is therefore:

> **The total information budget remains fixed.**

Only its allocation changes.

---

# Query-Aware Routing

The router receives the question and determines which memory components are likely to be useful.

Conceptually:

```text
                 Question
                    │
                    ▼
              Query Encoder
                    │
                    ▼
             Allocation Router
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
   Semantic     Structural    Symbolic
    budget        budget        budget
```

The router should not simply choose one memory.

It should potentially allocate a continuous budget between several memory types.

For example:

```text
B = 128

Semantic:      72
Structural:    40
Symbolic:      16
```

The exact routing mechanism is an open research question.

---

# Progressive Information Disclosure

A further extension is to make the information budget dynamic over time.

Instead of immediately providing the full memory:

```text
128 units
```

the receiver could initially receive:

```text
16 units
```

If the answer remains uncertain, additional information could be requested:

```text
16 → 32 → 64 → 128
```

Conceptually:

```text
Question
   │
   ▼
Small Memory
   │
   ▼
Receiver
   │
   ├── sufficient ──► Answer
   │
   └── insufficient
           │
           ▼
       More Memory
           │
           ▼
        Receiver
```

This introduces a second optimization objective:

> **How much information does the model actually need to answer a given question?**

This could potentially reduce average information usage even when the maximum budget remains large.

---

# Latent Memory

Continuous latent representations remain an important component of the project.

A semantic encoder may produce:

```text
z₁ z₂ z₃ ... zₖ
```

where:

```text
k << number of source tokens
```

The latent representation acts as a learned communication channel.

However, the project explicitly avoids assuming that all information should pass through this channel.

Instead:

```text
Semantic knowledge
        ↓
Latent representation

Structural knowledge
        ↓
Graph representation

Exact symbolic knowledge
        ↓
Symbolic representation
```

This is the main conceptual difference from monolithic latent compression.

---

# Information Budget as a Common Currency

A major experimental challenge is comparing different memory types fairly.

A graph, a latent vector, and an exact symbolic sidecar do not naturally have the same unit of size.

The project therefore needs an explicit definition of **information budget**.

Possible measures include:

- serialized token count;
- bytes;
- number of latent vectors;
- number of graph edges/nodes;
- number of symbolic facts;
- model input cost;
- learned communication units.

The exact budget definition is itself an important methodological decision.

The final benchmark should report multiple resource measures rather than relying on a single arbitrary number.

---

# Evaluation Dimensions

The project should not be evaluated using a single accuracy score.

We want to measure at least four dimensions.

## 1. Task Performance

Can the receiver answer questions correctly?

Possible task categories:

```text
Semantic
Structural
Architectural
Behavioral
Relational
Identifier
Literal
```

---

## 2. Information Efficiency

How much performance is obtained per unit of information?

A simple conceptual metric is:

```text
Information Efficiency =
Task Performance / Information Budget
```

The exact metric will be refined after establishing reliable evaluation methodology.

---

## 3. Adaptive Allocation Efficiency

Does the router allocate more budget to the memory type actually needed by the task?

For example:

```text
Question type       Actual useful memory

Semantic            Semantic
Call graph          Structural
Exact identifier    Symbolic
```

This can be evaluated using controlled synthetic and real-world tasks.

---

## 4. Computational Efficiency

Measure:

- input tokens;
- memory size;
- latency;
- throughput;
- GPU memory;
- encoder cost;
- receiver cost;
- total inference cost.

The project should distinguish **information efficiency** from **wall-clock efficiency**.

A method may be information-efficient while being computationally expensive.

---

# Baselines

The project requires strong baselines.

## Baseline 1 — Full Context

The receiver receives the relevant source code directly.

```text
Code ──► LLM
```

This provides an upper-bound-style reference for available textual information.

---

# Baseline 2 — Standard Retrieval

A conventional repository retrieval pipeline:

```text
Repository
    │
    ▼
Retriever
    │
    ▼
Relevant code
    │
    ▼
LLM
```

Possible retrieval strategies can include lexical, embedding-based, or hybrid retrieval.

---

# Baseline 3 — Context Compression

Use an existing code/context compression method.

```text
Repository
    │
    ▼
Compressor
    │
    ▼
Compressed text
    │
    ▼
LLM
```

This tests whether the proposed representation is better than simply selecting or compressing textual tokens.

---

# Baseline 4 — Monolithic Latent Memory

A single encoder produces one latent representation:

```text
Repository
    │
    ▼
Single Encoder
    │
    ▼
K latent units
    │
    ▼
LLM
```

This is the most important architectural baseline.

---

# Baseline 5 — Static Hybrid Memory

Use multiple memory types but with a fixed allocation:

```text
Semantic       64
Structural     32
Symbolic       32
```

This isolates the contribution of adaptive routing.

---

# Baseline 6 — Adaptive Heterogeneous Memory

The proposed approach:

```text
Semantic
Structural
Symbolic
    │
    ▼
Adaptive Router
    │
    ▼
Fixed total budget
    │
    ▼
Receiver
```

The key comparison becomes:

> **Does adaptive allocation outperform static allocation when total information is held constant?**

---

# Main Experimental Matrix

The core experiment should compare:

```text
A. Full Context

B. Retrieval

C. Text Compression

D. Monolithic Latent

E. Static Hybrid

F. Adaptive Hybrid
```

under controlled information budgets.

For example:

```text
              Low Budget   Medium Budget   High Budget

Full Context       -             -              ✓
Retrieval          ✓             ✓              ✓
Compression        ✓             ✓              ✓
Latent             ✓             ✓              ✓
Static Hybrid      ✓             ✓              ✓
Adaptive Hybrid    ✓             ✓              ✓
```

The exact budgets will be determined after establishing the benchmark.

---

# Information-Type Benchmark

A central part of the evaluation should explicitly separate information types.

## Semantic Questions

Example:

> What is the purpose of the authentication module?

---

## Structural Questions

Example:

> Which modules call `AuthService`?

---

## Symbolic Questions

Example:

> What is the exact name of the token validation function?

---

## Literal Questions

Example:

> What timeout value is configured?

---

## Behavioral Questions

Example:

> What happens when token verification fails?

---

## Relational Questions

Example:

> How is `UserService` connected to the authentication subsystem?

---

This allows us to determine not only whether the model succeeds, but **which kinds of information each memory architecture preserves**.

---

# Counterfactual Evaluation

A major concern in latent communication is that a receiver may produce a plausible answer without actually using the encoded information.

For example:

```text
Code A:
MAX_RETRIES = 3

Code B:
MAX_RETRIES = 10
```

Only one fact changes.

The system produces:

```text
Memory A
Memory B
```

and we measure:

- latent distance;
- receiver output;
- answer probability;
- relevant feature changes.

If the answer remains unchanged despite the source fact changing, the memory system may have failed to encode that information.

Counterfactual tests therefore provide stronger evidence than accuracy alone.

---

# Receiver Prior Tests

Suppose the receiver answers:

> `Authentication is implemented by validate_token().`

There are at least two explanations.

### Genuine information transfer

The encoder transmitted enough information to identify the function.

### Receiver prior

The receiver generated a plausible answer based on patterns already present in its pretrained knowledge.

The project therefore needs controlled tests where:

- identifiers are randomized;
- function names are unusual;
- repository-specific constants are changed;
- semantically equivalent implementations use different symbols.

This helps determine whether the receiver actually depends on repository memory.

---

# Cross-Receiver Transfer

Another important experiment is to test whether memory is tied to a specific receiver.

```text
                  Encoder
                     │
                     ▼
                Shared Memory
                /     |      \
               /      |       \
              ▼       ▼        ▼
           Model A  Model B  Model C
```

The encoder can be trained with one receiver and evaluated with another.

Questions:

- Does semantic memory transfer?
- Does structural memory transfer?
- Does symbolic memory transfer?
- Which representations are receiver-dependent?
- Does adaptive routing generalize?

A successful cross-receiver representation would provide evidence that the memory contains reusable information rather than merely encoding a private interface between two models.

---

# Latent Intervention

Where possible, the project can investigate causal relationships between latent features and outputs.

Conceptually:

```text
Original memory
      │
      ▼
Receiver
      │
      ▼
Answer

        vs.

Intervened memory
      │
      ▼
Receiver
      │
      ▼
Changed Answer?
```

If controlled modifications to a memory component systematically affect the corresponding task output, this provides stronger evidence that the representation contains task-relevant information.

This should be treated as an advanced research direction rather than a prerequisite for the first prototype.

---

# Ablation Studies

Ablation is essential.

Possible experiments include:

### Remove semantic memory

```text
Structural + Symbolic
```

### Remove structural memory

```text
Semantic + Symbolic
```

### Remove symbolic memory

```text
Semantic + Structural
```

### Disable adaptive routing

```text
Static allocation
```

### Disable progressive disclosure

```text
Full budget immediately
```

### Replace latent semantic memory

```text
Latent → text summary
```

### Remove query conditioning

```text
Same memory allocation for every question
```

These experiments allow us to identify where performance actually comes from.

---

# Expected Failure Modes

Failure is an explicit part of the research.

Possible outcomes include:

### Semantic collapse

Semantic memory preserves only broad concepts.

### Structural collapse

The model knows individual components but loses relationships.

### Symbolic loss

Exact identifiers and literals disappear.

### Router collapse

The adaptive router learns to allocate almost all capacity to one memory type.

### Budget misallocation

The router allocates information to a representation that is not useful for the current question.

### Receiver prior dominance

The receiver answers from pretrained knowledge rather than repository memory.

### Representation entanglement

Different information types cannot be cleanly separated.

### Cross-receiver incompatibility

Memory works only with the receiver used during training.

### Progressive-disclosure overhead

The cost of requesting additional memory exceeds the savings.

### Retrieval dominance

A conventional retrieval system remains more effective at the same computational budget.

Any of these results can be scientifically useful.

---

# What Makes This Different

The project is not based on the assumption that:

> "Latent tokens are better than text."

Instead, it investigates:

> **"Does the type of representation matter when the information budget is constrained?"**

The core comparison is therefore:

```text
Monolithic Memory
       │
       ▼
One representation
       │
       ▼
One bottleneck


            VS


Heterogeneous Memory
       │
 ┌─────┼─────┐
 ▼     ▼     ▼
Sem.  Struct. Sym.
 │     │     │
 └─────┼─────┘
       ▼
Adaptive allocation
       │
       ▼
Same total budget
```

This gives the project a falsifiable research hypothesis rather than simply another architecture.

---

# What This Project Is NOT

This project is not intended to be:

- another ChatGPT clone;
- another generic coding assistant;
- another simple RAG wrapper;
- another vector database tutorial;
- another prompt-engineering project;
- another generic context compressor;
- a claim that latent representations automatically replace retrieval;
- a claim that deterministic symbolic memory is always superior;
- a claim that heterogeneous memory will necessarily outperform existing methods.

The architecture is a hypothesis.

The experiments determine whether it works.

---

# Potential Applications

If the approach proves useful, potential applications include:

## Persistent Repository Memory

A codebase could be encoded into a compact heterogeneous memory and reused across sessions.

## Long-Running Coding Agents

Agents could maintain persistent representations of large codebases without repeatedly processing the entire repository.

## Adaptive Context Reduction

Simple questions could use very small information budgets while difficult questions receive additional information.

## Multi-Model Communication

Different models could potentially consume the same repository memory.

## Repository Understanding

The memory could act as a compact representation of semantic, structural, and symbolic knowledge.

These are potential applications, not demonstrated capabilities.

---

# Potential Research Contributions

The final contribution does not have to be a completely new neural architecture.

Possible contributions include:

### Contribution A — Heterogeneous Code Memory

A framework for separating semantic, structural, and symbolic repository knowledge.

### Contribution B — Adaptive Information Allocation

A learned mechanism for allocating a fixed information budget between memory types.

### Contribution C — Information-Budget Benchmark

A benchmark that compares repository reasoning systems under controlled information budgets.

### Contribution D — Information Retention Analysis

A systematic study of which types of code knowledge survive different compression strategies.

### Contribution E — Counterfactual Evaluation

Methods for distinguishing genuine information transfer from receiver priors.

### Contribution F — Cross-Receiver Analysis

An investigation of whether learned code memory is reusable across different receiver models.

### Contribution G — Negative Results

A clear demonstration of where heterogeneous memory fails or provides no advantage.

The final contribution will be determined by experimental evidence.

---

# Information Efficiency

One of the central goals is to move beyond raw accuracy.

Suppose two systems achieve:

```text
System A
90% accuracy
1000 information units

System B
88% accuracy
128 information units
```

System B may be considerably more information-efficient.

The project will therefore investigate metrics that relate:

```text
Task performance
        ↕
Information budget
        ↕
Computational cost
```

The final metric definition will be established before the main comparison to avoid optimizing the evaluation after seeing the results.

---

# Research Workflow

The project follows a research workflow rather than immediately implementing the complete architecture.

```text
Study fundamentals
        │
        ▼
Literature / related-work audit
        │
        ▼
Define exact research gap
        │
        ▼
Build minimal monolithic latent baseline
        │
        ▼
Build strong retrieval / compression baselines
        │
        ▼
Define information budget
        │
        ▼
Introduce semantic memory
        │
        ▼
Introduce structural memory
        │
        ▼
Introduce symbolic memory
        │
        ▼
Build static hybrid baseline
        │
        ▼
Introduce adaptive routing
        │
        ▼
Introduce progressive disclosure
        │
        ▼
Run controlled experiments
        │
        ▼
Counterfactual evaluation
        │
        ▼
Cross-receiver experiments
        │
        ▼
Ablation studies
        │
        ▼
Failure analysis
        │
        ▼
Refine hypothesis
        │
        ▼
Final evaluation
        │
        ▼
Technical report
        │
        ▼
Open-source release
```

The architecture is explicitly allowed to change during this process.

---

# Expected Final Artifact

The final project may contain:

```text
Research Project
│
├── Memory architecture
│
├── Semantic encoder
│
├── Structural representation
│
├── Symbolic extraction
│
├── Adaptive router
│
├── Training pipeline
│
├── Evaluation framework
│
├── Benchmark dataset
│
├── Baselines
│
├── Counterfactual tests
│
├── Ablation studies
│
├── Experimental results
│
├── Failure analysis
│
├── Documentation
│
├── Technical report
│
└── Open-source release
```

A lightweight CLI or API may be added if the research results justify it.

The CLI is an application and demonstration layer, not the primary research contribution.

---

# What Success Looks Like

Success does not necessarily mean:

> "Our model beats every baseline."

A successful result could instead establish:

> Under the same information budget, heterogeneous memory preserves semantic, structural, and symbolic information more effectively than monolithic latent compression.

Or:

> Adaptive allocation provides a measurable improvement over static allocation at the same total budget.

Or:

> Semantic information benefits strongly from latent representations, while exact symbolic information is better preserved through deterministic representations.

Or:

> Progressive disclosure reduces average information consumption without significantly reducing answer quality.

Or:

> Heterogeneous memory provides no overall improvement, but reveals a strong and reproducible separation between information types.

Even a negative result can be valuable if the comparison is rigorous and reproducible.

---

# Limitations

The proposed approach may have significant limitations.

It may:

- require multiple encoders or processing stages;
- introduce routing overhead;
- be computationally more expensive than simple retrieval;
- fail to define a fair common information budget;
- produce incompatible representations;
- lose information during semantic compression;
- depend on receiver architecture;
- require language-specific static analysis;
- struggle with dynamic programming behavior;
- fail on unfamiliar repositories;
- provide worse latency than retrieval;
- require substantial training data.

These limitations will be explicitly measured and reported.

---

# Long-Term Vision

The broader question behind this project is:

> **Can structured knowledge be stored more efficiently when different kinds of information are represented according to their intrinsic properties rather than forced through a single learned representation?**

Code is an especially useful domain for studying this question because it contains:

- precise symbols;
- hierarchical structure;
- semantic relationships;
- dependency graphs;
- executable behavior;
- exact literals;
- long-range dependencies;
- both high-level and low-level information.

The project therefore sits at the intersection of:

```text
Code Intelligence
       +
Representation Learning
       +
Information Bottlenecks
       +
Learned Memory
       +
Neural Communication
```

The long-term goal is not simply to build a smaller context.

It is to understand **how different kinds of knowledge should be represented and communicated when information is limited**.

---

# Research Philosophy

The project follows several principles.

## 1. Evidence over intuition

Interesting ideas must be experimentally tested.

## 2. Baselines over isolated results

A number without a meaningful comparison is not enough.

## 3. Equal-budget comparisons

Methods should be compared under controlled information and computational constraints whenever possible.

## 4. Negative results are valuable

A failed hypothesis can reveal important properties of code representations and memory systems.

## 5. Reproducibility over spectacle

All important results should be reproducible.

## 6. Deterministic tools where appropriate

A neural network should not approximate information that deterministic program analysis can preserve exactly unless there is a research reason to do so.

## 7. Understanding over implementation speed

The project is also an educational research process.

## 8. No predetermined conclusion

We do not know whether adaptive heterogeneous memory will outperform existing methods.

The experiments determine the conclusion.

---

# Project Status

**Early research / conceptual stage**

No experimental results are claimed at this stage.

The exact memory representations, datasets, information-budget definition, routing mechanism, and evaluation methodology are expected to evolve as the research progresses.

---

# Roadmap

## Phase 1 — Foundations

- [ ] Study Transformer internals
- [ ] Study attention and KV-cache
- [ ] Study representation learning
- [ ] Study latent representations
- [ ] Study information bottlenecks
- [ ] Study code representations
- [ ] Study ASTs and static analysis
- [ ] Study graph representations
- [ ] Study context compression

## Phase 2 — Research Audit

- [ ] Review repository-level compression methods
- [ ] Review latent-vector compression
- [ ] Review code-specific compression
- [ ] Review graph-based code memory
- [ ] Review learned memory systems
- [ ] Review adaptive information allocation
- [ ] Identify the precise research gap
- [ ] Define the initial hypothesis

## Phase 3 — Baselines

- [ ] Build full-context evaluation
- [ ] Build retrieval baseline
- [ ] Build text-compression baseline
- [ ] Build monolithic latent baseline
- [ ] Define information-budget methodology

## Phase 4 — Heterogeneous Memory

- [ ] Implement semantic memory
- [ ] Implement structural memory
- [ ] Implement symbolic memory
- [ ] Build static hybrid baseline
- [ ] Establish information-type benchmark

## Phase 5 — Adaptive Memory

- [ ] Implement query-conditioned routing
- [ ] Implement adaptive budget allocation
- [ ] Compare adaptive vs static allocation
- [ ] Test different budget sizes
- [ ] Measure information efficiency

## Phase 6 — Advanced Experiments

- [ ] Progressive information disclosure
- [ ] Counterfactual evaluation
- [ ] Receiver-prior tests
- [ ] Latent interventions
- [ ] Cross-receiver transfer
- [ ] Cross-repository generalization

## Phase 7 — Analysis

- [ ] Ablation studies
- [ ] Failure-mode analysis
- [ ] Information-retention analysis
- [ ] Computational efficiency analysis
- [ ] Statistical significance / uncertainty analysis

## Phase 8 — Release

- [ ] Final evaluation
- [ ] Technical report
- [ ] Research documentation
- [ ] Reproducible training scripts
- [ ] Reproducible evaluation scripts
- [ ] Model / artifacts release where appropriate
- [ ] Open-source release

---

# Final Research Question

The project ultimately asks:

> **When the amount of information available to a language model is strictly limited, is it better to compress everything into one learned representation — or to represent semantic, structural, and symbolic knowledge differently and dynamically allocate the available information budget between them?**

The goal is not merely to build another code compressor.

The goal is to investigate whether **heterogeneous, adaptive memory can make information-limited code reasoning more efficient, more reliable, and more interpretable than monolithic compression.**

And regardless of the outcome, the project aims to produce a reproducible answer to that question.