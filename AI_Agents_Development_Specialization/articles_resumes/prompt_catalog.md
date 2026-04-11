Prompt Pattern Catalog — Study Summary
> Based on: "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT"
---
🧠 TL;DR (Executive Summary)
Prompt engineering is essentially programming LLMs using natural language.
This paper introduces Prompt Patterns — reusable strategies (like design patterns in software engineering) that help you:
Control outputs
Improve accuracy
Automate workflows
Guide interactions
👉 Key idea:
> Better prompts = better results (not just better models)
---
🧩 What Are Prompt Patterns?
A prompt pattern is a reusable structure that:
Solves a recurring problem when interacting with LLMs
Encodes best practices
Can be adapted across domains
💡 Analogy:
Software Patterns → reusable code solutions
Prompt Patterns → reusable prompt strategies
---
🏗️ Pattern Structure (How to Think)
Each pattern follows:
Intent → what problem it solves
Motivation → why it matters
Structure → how to write it
Example → real prompt
Consequences → trade-offs
---
🧠 Core Categories of Patterns
1. Input Semantics
Control how the model understands your input
2. Output Customization
Control format, structure, and style
3. Error Identification
Reduce hallucinations
4. Prompt Improvement
Improve your own questions
5. Interaction Control
Change how conversation flows
6. Context Control
Define environment/context
---
🔥 Key Patterns (With Examples & Use Cases)
---
1. Meta Language Creation
Idea
Create your own "language" for the model.
Structure
When I say X, I mean Y
Example
"When I write A → B, treat it as a graph edge"
Use Case
Graph modeling
DSL (domain-specific languages)
Workflow commands
Insight
👉 You are literally creating a mini programming language for the AI.
---
2. Output Automater
Idea
Turn instructions into executable scripts.
Structure
If output has steps → generate script to automate them
Example
"Whenever you generate multi-file code, also create a Python script to generate those files"
Use Case
DevOps automation
File generation
Infrastructure setup
Insight
👉 Bridge between AI suggestions → real execution
---
3. Flipped Interaction
Idea
AI asks YOU questions instead of answering.
Structure
Ask me questions until goal X is achieved
Example
"Ask me questions until you can deploy my app to AWS"
Use Case
Requirements gathering
Learning
Debugging
Insight
👉 Turns ChatGPT into a consultant/interviewer
---
4. Persona Pattern
Idea
Force AI to think like a specific role.
Structure
Act as [persona]
Example
"Act as a senior security engineer reviewing this code"
Use Case
Code review
Business advice
UX critique
Insight
👉 You don't need to know WHAT to ask — just WHO to ask.
---
5. Question Refinement
Idea
AI improves your question before answering.
Structure
Suggest a better version of my question
Example
How to handle auth? → Better: secure FastAPI auth with XSS/CSRF
Use Case
Learning new domains
Avoiding vague prompts
Insight
👉 Helps you think like an expert.
---
6. Alternative Approaches
Idea
Force AI to show multiple solutions.
Structure
List alternative approaches + pros/cons
Example
Compare EC2 vs Lambda vs ECS for deployment
Use Case
Architecture decisions
Business strategy
Insight
👉 Breaks cognitive bias.
---
7. Cognitive Verifier
Idea
Break problem into sub-questions.
Structure
Generate sub-questions → combine answers
Use Case
Complex reasoning
System design
Insight
👉 Improves accuracy.
---
8. Fact Check List
Idea
List assumptions that must be verified.
Structure
List facts that need verification
Use Case
Critical systems
Research
Insight
👉 Anti-hallucination.
---
9. Template Pattern
Idea
Force strict output format.
Structure
Follow template with placeholders
Use Case
APIs
JSON
Insight
👉 Machine-friendly output.
---
10. Infinite Generation
Idea
Generate outputs continuously.
Structure
Generate until I say stop
Use Case
Brainstorming
---
11. Visualization Generator
Idea
Generate diagrams via tools.
Use Case
Architecture diagrams
---
⚠️ Key Lessons
Prompts = programming
Combine patterns
Context matters
Trade-offs exist
---
🚀 Cheat Sheet
Better answers → Cognitive Verifier + Question Refinement  
Structured output → Template  
Automation → Output Automater  
Accuracy → Fact Check List
---
🧠 Final Insight
Prompt engineering = designing systems, not asking questions.