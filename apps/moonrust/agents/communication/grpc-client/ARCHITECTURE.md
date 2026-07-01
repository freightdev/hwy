# gRPC Client

## Identity
I am **grpc-client**. I make gRPC calls to services.

## Purpose
I send unary, server-streaming, client-streaming, and bidirectional-streaming gRPC calls.

## Interface
in: {service, method, request, metadata?} / out: {response, trailing_metadata?, status}

## Configuration
protoset_dir, deadline, max_retries, tls, load_balance

## Dependencies
rpc-caller, service-mesh, connection-pooler

## Wake Sequence
On wake, I load my configuration, verify my dependencies are available, register my capabilities with the orchestrator, and await instructions.
