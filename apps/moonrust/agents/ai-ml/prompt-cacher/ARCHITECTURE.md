# Prompt Cacher

## Identity
I am **prompt-cacher**. I cache LLM responses for identical or similar prompts.

## Purpose
I cache LLM responses keyed by prompt, model, and params. I support exact-match and semantic-similarity cache.

## Interface
in: {op: get|set|invalidate, prompt, model?} / out: {hit, response?, cache_key, age?}

## Configuration
backend: memory|redis|database, default_ttl, similarity_threshold, max_cache_size

## Dependencies
llm-request, text-embedder, cache-operator

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
