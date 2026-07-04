# Milestones

## Milestone 1: Core Parser
Parsing raw GCC and linker output into structured diagnostic objects.

## Milestone 2: Classifier

## Milestone 3: Knowledge Base + Explainer
Build the knowledge base as structured data. Wire the classifier output to explanations.

## Milestone 4: FastAPI Layer
Expose the pipeline as a REST API. Define request/response contrats. Add OpenAPI documentation.

## Milestone 5: Frontend (React/Next.js)
Build UI that calls the API. Start with a text input field for pasting build logs.

## Milestone 6: File Upload
Accept uploaded build logs and source files. Persist sessions

## Milestone 7: Keyword Retrieval
Replace the lookup table with an indexed knowledge base, add search across ingested documentation.

## Milestone 8: Semantic Search
Evaluate whether embeddings improve retrieval quality over keyword search.