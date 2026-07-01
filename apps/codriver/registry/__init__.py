"""
HWY CoDriver — Actor Registry

CoDriver "does not need to know how every actor works internally. It only
needs to know what each actor owns." This registry is that boundary made
concrete: a lookup table of ActorManifests, plus the in-process handlers
Direct Dispatch will actually invoke.
"""

from __future__ import annotations

from typing import Protocol

from ..models import ActorContext, ActorManifest, ActorResponse, FlowSpec
from .actor_manifest_schema import ActorManifestDraft
from .agent_manifest_schema import AgentManifestDraft
from .load_agent_manifests import load_agent_manifest_file, load_agent_manifests
from .load_manifests import load_actor_manifests, load_actor_manifest_file


class ActorHandler(Protocol):
    def handle(self, flow_id: str, payload: dict, context: ActorContext) -> ActorResponse: ...


class ActorRegistry:
    def __init__(self) -> None:
        self._manifests: dict[str, ActorManifest] = {}
        self._handlers: dict[str, ActorHandler] = {}
        self._flows: dict[str, FlowSpec] = {}

    def register_actor(self, manifest: ActorManifest, handler: ActorHandler) -> None:
        self._manifests[manifest.name] = manifest
        self._handlers[manifest.name] = handler

    def register_flow(self, flow: FlowSpec) -> None:
        self._flows[flow.flow_id] = flow

    def manifest(self, actor_name: str) -> ActorManifest:
        if actor_name not in self._manifests:
            raise KeyError(f"No actor registered: {actor_name}")
        return self._manifests[actor_name]

    def handler(self, actor_name: str) -> ActorHandler:
        if actor_name not in self._handlers:
            raise KeyError(f"No handler registered for actor: {actor_name}")
        return self._handlers[actor_name]

    def flow(self, flow_id: str) -> FlowSpec:
        if flow_id not in self._flows:
            raise KeyError(f"No flow registered: {flow_id}")
        return self._flows[flow_id]

    def actor_owning_flow(self, flow_id: str) -> str:
        return self.flow(flow_id).owner_actor

    def all_actors(self) -> list[ActorManifest]:
        return list(self._manifests.values())

    def all_flows(self) -> list[FlowSpec]:
        return list(self._flows.values())


__all__ = [
    "ActorHandler",
    "ActorManifestDraft",
    "ActorRegistry",
    "AgentManifestDraft",
    "load_actor_manifest_file",
    "load_actor_manifests",
    "load_agent_manifest_file",
    "load_agent_manifests",
]
