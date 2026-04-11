# Prompt Patterns for Software Engineering — Study Summary

> Based on: "ChatGPT Prompt Patterns for Improving Code Quality, Refactoring, Requirements Elicitation, and Software Design" fileciteturn1file0

---

# 🧠 TL;DR

Prompt engineering can be used to **automate the entire software lifecycle**:
- Requirements
- Architecture
- API design
- Code quality
- Refactoring

👉 Prompts = programming interface for software engineering tasks

---

# 🧩 Core Idea

Prompt patterns are reusable instructions that:
- Improve code quality
- Reduce ambiguity
- Accelerate design
- Enable simulation of systems

---

# 🏗️ Pattern Categories

## 1. Requirements & Design
- Requirements Simulator
- Specification Disambiguation
- API Generator
- API Simulator
- DSL Creation
- Architectural Possibilities
- Change Request Simulation

## 2. Code Quality
- Code Clustering
- Intermediate Abstraction
- Principled Code
- Hidden Assumptions

## 3. Refactoring
- Pseudo-code Refactoring
- Data-guided Refactoring

## 4. Learning / Context
- Few-shot Example Generator

---

# 🔥 Key Patterns (With Examples)

---

# 1. Requirements Simulator

## Idea
Simulate system behavior based on requirements.

## Example
"Act as the system. Tell me if I can do X. If not, generate missing requirements."

## Use Case
- Validate requirements early
- Discover missing features

---

# 2. Specification Disambiguation

## Idea
Find ambiguities in requirements.

## Example
"Point out ambiguous parts and improve clarity."

## Use Case
- Product → Dev handoff
- Avoid misunderstandings

---

# 3. API Generator

## Idea
Generate API from requirements.

## Example
"Generate an OpenAPI spec from these requirements"

## Use Case
- Rapid prototyping
- API-first design

---

# 4. API Simulator

## Idea
Simulate API behavior.

## Example
"I send HTTP request → you return response"

## Use Case
- Test API before coding
- Validate design

---

# 5. Architectural Possibilities

## Idea
Generate multiple architectures.

## Example
"Give 3 architectures for this system"

## Use Case
- Explore monolith vs microservices
- Compare designs

---

# 6. Change Request Simulation

## Idea
Estimate impact of changes.

## Example
"What changes if I add field X?"

## Use Case
- Scope estimation
- Risk analysis

---

# 7. Code Clustering

## Idea
Separate code by responsibility.

## Example
"Separate business logic from side-effects"

## Use Case
- Clean architecture
- Testability

---

# 8. Intermediate Abstraction

## Idea
Add abstraction layers.

## Example
"Wrap 3rd-party libs with abstraction"

## Use Case
- Decoupling
- Replace dependencies

---

# 9. Principled Code

## Idea
Apply known design principles.

## Example
"Follow SOLID principles"

## Use Case
- Maintainability
- Clean code

---

# 10. Hidden Assumptions

## Idea
Expose assumptions in code.

## Example
"List assumptions and how hard to change them"

## Use Case
- Avoid technical debt
- Refactoring planning

---

# 11. Pseudo-code Refactoring

## Idea
Refactor based on pseudo-code.

## Example
"Refactor code to match this structure"

## Use Case
- High-level control
- Faster iteration

---

# 12. Data-guided Refactoring

## Idea
Refactor based on data format.

## Example
"Adapt code to this new JSON schema"

## Use Case
- API changes
- Data migrations

---

# 13. Few-shot Example Generator

## Idea
Generate examples to reuse later.

## Example
"Create 10 usage examples"

## Use Case
- Teach LLM context
- Work around token limits

---

# ⚠️ Lessons

- LLMs need **clear constraints**
- Prompt quality = output quality
- Human validation is still required
- Combine patterns for best results

---

# 🚀 Cheat Sheet

Requirements → Simulator + Disambiguation  
Architecture → Possibilities + API Generator  
Code Quality → Clustering + SOLID  
Refactoring → Pseudo-code + Data-guided  

---

# 🧠 Final Insight

Prompt engineering is a **full-stack engineering skill**:
You are not coding systems directly —  
you are designing how AI builds them.

---
