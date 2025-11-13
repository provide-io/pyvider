"""
Simulation Provider for Pyvider - Behavior Simulation as Infrastructure

A novel provider demonstrating that Terraform can manage ANY domain, not just cloud infrastructure.
This provider models agent-based simulations, emergent behaviors, and complex systems.

Use cases:
- Game mechanics prototyping
- Social system modeling
- Ecosystem simulations
- Market dynamics
- Disease spread modeling
- Traffic flow analysis
"""

from pyvider.providers import BaseProvider, ProviderMetadata, register_provider
from pyvider.resources import BaseResource, ResourceContext, register_resource
from pyvider.data_sources import register_data_source
from pyvider.data_sources.base import BaseDataSource
from pyvider.functions import BaseFunction, FunctionParameter, FunctionReturnType, register_function
from pyvider.schema import (
    s_provider,
    s_resource,
    s_data_source,
    s_function,
    a_str,
    a_num,
    a_bool,
    a_list,
    a_map,
)
from pyvider.cty import CtyString, CtyNumber, CtyBool, CtyList, CtyMap
from attrs import define, field
from typing import Any
import json
import time
import random
import math


# ============================================================================
# Provider Definition
# ============================================================================

@register_provider("simulation")
class SimulationProvider(BaseProvider):
    """
    Behavior Simulation Provider - Model complex systems as infrastructure.

    This provider enables Infrastructure-as-Code for:
    - Agent-based modeling
    - Emergent behavior systems
    - Rule-based simulations
    - Complex adaptive systems
    """

    def __init__(self) -> None:
        super().__init__(
            metadata=ProviderMetadata(
                name="simulation",
                version="1.0.0",
                protocol_version="6",
            )
        )

    @classmethod
    def get_schema(cls):
        return s_provider({
            "seed": a_num(
                required=False,
                description="Random seed for reproducible simulations",
            ),
            "tick_rate": a_num(
                required=False,
                description="Simulation ticks per second (for real-time sims)",
            ),
            "enable_recording": a_bool(
                required=False,
                description="Record simulation state history",
            ),
        })


# ============================================================================
# Resource: simulation_world
# ============================================================================

@register_resource("world")
class SimulationWorld(BaseResource):
    """
    Defines a simulation world/environment where agents exist.

    Worlds can have:
    - Spatial dimensions
    - Physical properties
    - Environmental conditions
    - Resource availability
    """

    _worlds = {}
    _next_id = 1

    @define
    class Config:
        name: str
        dimensions: list[float] = field(factory=lambda: [100.0, 100.0])  # [width, height, depth?]
        topology: str = "euclidean"  # euclidean, toroidal, graph
        gravity: float = 0.0
        friction: float = 0.1
        resources: dict[str, float] = field(factory=dict)  # resource_name -> amount
        properties: dict[str, str] = field(factory=dict)

    @define
    class State:
        id: str
        name: str
        dimensions: list[float]
        topology: str
        gravity: float
        friction: float
        resources: dict[str, float]
        properties: dict[str, str]
        # Computed
        volume: float
        created_at: str
        tick_count: int

    @classmethod
    def get_schema(cls):
        return s_resource({
            "id": a_str(computed=True, description="World identifier"),
            "name": a_str(required=True, description="World name"),
            "dimensions": a_list(a_num(), optional=True, description="Spatial dimensions [x, y, z]"),
            "topology": a_str(optional=True, description="Space topology (euclidean, toroidal, graph)"),
            "gravity": a_num(optional=True, description="Gravitational force"),
            "friction": a_num(optional=True, description="Friction coefficient"),
            "resources": a_map(a_num(), optional=True, description="Available resources"),
            "properties": a_map(a_str(), optional=True, description="Custom world properties"),
            # Computed
            "volume": a_num(computed=True, description="World volume"),
            "created_at": a_str(computed=True, description="Creation timestamp"),
            "tick_count": a_num(computed=True, description="Simulation ticks elapsed"),
        })

    async def _create_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        world_id = f"world-{self._next_id:06d}"
        self._next_id += 1

        # Calculate volume
        volume = 1.0
        for dim in ctx.config.dimensions:
            volume *= dim

        world_data = {
            "id": world_id,
            "name": ctx.config.name,
            "dimensions": ctx.config.dimensions,
            "topology": ctx.config.topology,
            "gravity": ctx.config.gravity,
            "friction": ctx.config.friction,
            "resources": ctx.config.resources,
            "properties": ctx.config.properties,
            "volume": volume,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tick_count": 0,
        }

        self._worlds[world_id] = world_data
        return self.State(**world_data), None

    async def read(self, ctx: ResourceContext) -> Any:
        world_id = ctx.state.id
        if world_id not in self._worlds:
            return None
        return self.State(**self._worlds[world_id])

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        world_id = ctx.state.id
        world_data = self._worlds[world_id]

        # Recalculate volume if dimensions changed
        volume = 1.0
        for dim in ctx.config.dimensions:
            volume *= dim

        world_data.update({
            "gravity": ctx.config.gravity,
            "friction": ctx.config.friction,
            "resources": ctx.config.resources,
            "properties": ctx.config.properties,
            "volume": volume,
        })

        return self.State(**world_data), None

    async def delete(self, ctx: ResourceContext) -> None:
        world_id = ctx.state.id
        if world_id in self._worlds:
            del self._worlds[world_id]


# ============================================================================
# Resource: simulation_agent
# ============================================================================

@register_resource("agent")
class SimulationAgent(BaseResource):
    """
    Defines an autonomous agent with behaviors and state.

    Agents can:
    - Move through worlds
    - Interact with other agents
    - Follow behavior rules
    - Consume/produce resources
    - Evolve over time
    """

    _agents = {}
    _next_id = 1

    @define
    class Config:
        name: str
        world_id: str
        agent_type: str
        position: list[float] = field(factory=lambda: [0.0, 0.0])
        velocity: list[float] = field(factory=lambda: [0.0, 0.0])
        energy: float = 100.0
        vision_range: float = 10.0
        speed: float = 1.0
        behaviors: list[str] = field(factory=list)  # behavior rule IDs
        attributes: dict[str, float] = field(factory=dict)

    @define
    class State:
        id: str
        name: str
        world_id: str
        agent_type: str
        position: list[float]
        velocity: list[float]
        energy: float
        vision_range: float
        speed: float
        behaviors: list[str]
        attributes: dict[str, float]
        # Computed
        age_ticks: int
        distance_traveled: float
        interactions: int
        status: str
        created_at: str

    @classmethod
    def get_schema(cls):
        return s_resource({
            "id": a_str(computed=True, description="Agent identifier"),
            "name": a_str(required=True, description="Agent name"),
            "world_id": a_str(required=True, description="World this agent exists in"),
            "agent_type": a_str(required=True, description="Agent type/species"),
            "position": a_list(a_num(), optional=True, description="Position in world [x, y, z]"),
            "velocity": a_list(a_num(), optional=True, description="Velocity vector [vx, vy, vz]"),
            "energy": a_num(optional=True, description="Agent energy level"),
            "vision_range": a_num(optional=True, description="How far agent can perceive"),
            "speed": a_num(optional=True, description="Maximum speed"),
            "behaviors": a_list(a_str(), optional=True, description="Behavior rule IDs"),
            "attributes": a_map(a_num(), optional=True, description="Custom attributes"),
            # Computed
            "age_ticks": a_num(computed=True, description="Age in simulation ticks"),
            "distance_traveled": a_num(computed=True, description="Total distance traveled"),
            "interactions": a_num(computed=True, description="Number of interactions"),
            "status": a_str(computed=True, description="Agent status"),
            "created_at": a_str(computed=True, description="Creation timestamp"),
        })

    async def _create_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        agent_id = f"agent-{self._next_id:06d}"
        self._next_id += 1

        agent_data = {
            "id": agent_id,
            "name": ctx.config.name,
            "world_id": ctx.config.world_id,
            "agent_type": ctx.config.agent_type,
            "position": ctx.config.position,
            "velocity": ctx.config.velocity,
            "energy": ctx.config.energy,
            "vision_range": ctx.config.vision_range,
            "speed": ctx.config.speed,
            "behaviors": ctx.config.behaviors,
            "attributes": ctx.config.attributes,
            "age_ticks": 0,
            "distance_traveled": 0.0,
            "interactions": 0,
            "status": "active",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        self._agents[agent_id] = agent_data
        return self.State(**agent_data), None

    async def read(self, ctx: ResourceContext) -> Any:
        agent_id = ctx.state.id
        if agent_id not in self._agents:
            return None
        return self.State(**self._agents[agent_id])

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        agent_id = ctx.state.id
        agent_data = self._agents[agent_id]

        # Update mutable fields
        agent_data.update({
            "position": ctx.config.position,
            "velocity": ctx.config.velocity,
            "energy": ctx.config.energy,
            "vision_range": ctx.config.vision_range,
            "speed": ctx.config.speed,
            "behaviors": ctx.config.behaviors,
            "attributes": ctx.config.attributes,
        })

        return self.State(**agent_data), None

    async def delete(self, ctx: ResourceContext) -> None:
        agent_id = ctx.state.id
        if agent_id in self._agents:
            del self._agents[agent_id]


# ============================================================================
# Resource: simulation_rule
# ============================================================================

@register_resource("rule")
class SimulationRule(BaseResource):
    """
    Defines a behavior rule that agents can follow.

    Rules specify:
    - When to trigger (conditions)
    - What to do (actions)
    - Priority (rule ordering)
    - Side effects (resource consumption, state changes)
    """

    _rules = {}
    _next_id = 1

    @define
    class Config:
        name: str
        description: str
        rule_type: str  # seek, flee, wander, consume, reproduce, attack
        priority: int = 10
        conditions: dict[str, str] = field(factory=dict)  # condition_name -> expression
        parameters: dict[str, float] = field(factory=dict)
        effects: dict[str, float] = field(factory=dict)  # stat_name -> change_amount

    @define
    class State:
        id: str
        name: str
        description: str
        rule_type: str
        priority: int
        conditions: dict[str, str]
        parameters: dict[str, float]
        effects: dict[str, float]
        # Computed
        activation_count: int
        average_effect: float
        created_at: str

    @classmethod
    def get_schema(cls):
        return s_resource({
            "id": a_str(computed=True, description="Rule identifier"),
            "name": a_str(required=True, description="Rule name"),
            "description": a_str(required=True, description="Rule description"),
            "rule_type": a_str(required=True, description="Rule type (seek, flee, wander, etc)"),
            "priority": a_num(optional=True, description="Execution priority (higher = first)"),
            "conditions": a_map(a_str(), optional=True, description="Trigger conditions"),
            "parameters": a_map(a_num(), optional=True, description="Rule parameters"),
            "effects": a_map(a_num(), optional=True, description="Stat modifications"),
            # Computed
            "activation_count": a_num(computed=True, description="Times rule activated"),
            "average_effect": a_num(computed=True, description="Average effect magnitude"),
            "created_at": a_str(computed=True, description="Creation timestamp"),
        })

    async def _create_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        rule_id = f"rule-{self._next_id:06d}"
        self._next_id += 1

        rule_data = {
            "id": rule_id,
            "name": ctx.config.name,
            "description": ctx.config.description,
            "rule_type": ctx.config.rule_type,
            "priority": ctx.config.priority,
            "conditions": ctx.config.conditions,
            "parameters": ctx.config.parameters,
            "effects": ctx.config.effects,
            "activation_count": 0,
            "average_effect": 0.0,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        self._rules[rule_id] = rule_data
        return self.State(**rule_data), None

    async def read(self, ctx: ResourceContext) -> Any:
        rule_id = ctx.state.id
        if rule_id not in self._rules:
            return None
        return self.State(**self._rules[rule_id])

    async def _update_apply(self, ctx: ResourceContext) -> tuple[Any, Any]:
        rule_id = ctx.state.id
        rule_data = self._rules[rule_id]

        rule_data.update({
            "description": ctx.config.description,
            "priority": ctx.config.priority,
            "conditions": ctx.config.conditions,
            "parameters": ctx.config.parameters,
            "effects": ctx.config.effects,
        })

        return self.State(**rule_data), None

    async def delete(self, ctx: ResourceContext) -> None:
        rule_id = ctx.state.id
        if rule_id in self._rules:
            del self._rules[rule_id]


# ============================================================================
# Data Source: simulation_statistics
# ============================================================================

@register_data_source("statistics")
class SimulationStatistics(BaseDataSource):
    """
    Query simulation-wide statistics and emergent behaviors.

    Provides metrics on:
    - Population dynamics
    - Resource distribution
    - Spatial patterns
    - Behavioral frequencies
    """

    @define
    class Config:
        world_id: str
        metric: str  # population, diversity, clustering, resource_flow

    @define
    class State:
        world_id: str
        metric: str
        # Computed metrics
        total_agents: int
        unique_types: int
        average_energy: float
        spatial_variance: float
        clustering_coefficient: float
        entropy: float
        computed_at: str

    @classmethod
    def get_schema(cls):
        return s_data_source({
            "world_id": a_str(required=True, description="World to analyze"),
            "metric": a_str(required=True, description="Metric type to compute"),
            # Results
            "total_agents": a_num(computed=True, description="Total agent count"),
            "unique_types": a_num(computed=True, description="Number of unique agent types"),
            "average_energy": a_num(computed=True, description="Average agent energy"),
            "spatial_variance": a_num(computed=True, description="Spatial distribution variance"),
            "clustering_coefficient": a_num(computed=True, description="Agent clustering measure"),
            "entropy": a_num(computed=True, description="System entropy"),
            "computed_at": a_str(computed=True, description="Computation timestamp"),
        })

    async def read(self, ctx) -> Any:
        world_id = ctx.config.world_id

        # Find all agents in this world
        agents_in_world = [
            a for a in SimulationAgent._agents.values()
            if a.get("world_id") == world_id
        ]

        total_agents = len(agents_in_world)
        unique_types = len(set(a.get("agent_type", "unknown") for a in agents_in_world))

        if total_agents > 0:
            average_energy = sum(a.get("energy", 0.0) for a in agents_in_world) / total_agents

            # Calculate spatial variance
            positions = [a.get("position", [0, 0]) for a in agents_in_world]
            if positions:
                mean_x = sum(p[0] for p in positions) / len(positions)
                mean_y = sum(p[1] for p in positions if len(p) > 1) / len(positions)
                spatial_variance = sum(
                    (p[0] - mean_x)**2 + (p[1] - mean_y)**2
                    for p in positions
                ) / len(positions)
            else:
                spatial_variance = 0.0

            # Simple clustering coefficient (percentage within vision range of others)
            in_range = 0
            for i, agent_i in enumerate(agents_in_world):
                pos_i = agent_i.get("position", [0, 0])
                vision = agent_i.get("vision_range", 10.0)
                for j, agent_j in enumerate(agents_in_world):
                    if i != j:
                        pos_j = agent_j.get("position", [0, 0])
                        dist = math.sqrt(sum((a - b)**2 for a, b in zip(pos_i, pos_j)))
                        if dist <= vision:
                            in_range += 1
                            break
            clustering_coefficient = in_range / total_agents if total_agents > 0 else 0.0

            # Shannon entropy of type distribution
            type_counts = {}
            for agent in agents_in_world:
                agent_type = agent.get("agent_type", "unknown")
                type_counts[agent_type] = type_counts.get(agent_type, 0) + 1

            entropy = 0.0
            for count in type_counts.values():
                p = count / total_agents
                entropy -= p * math.log2(p) if p > 0 else 0
        else:
            average_energy = 0.0
            spatial_variance = 0.0
            clustering_coefficient = 0.0
            entropy = 0.0

        return self.State(
            world_id=world_id,
            metric=ctx.config.metric,
            total_agents=total_agents,
            unique_types=unique_types,
            average_energy=average_energy,
            spatial_variance=spatial_variance,
            clustering_coefficient=clustering_coefficient,
            entropy=entropy,
            computed_at=time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    async def _validate_config(self, config) -> list[str]:
        return []


# ============================================================================
# Data Source: simulation_neighbors
# ============================================================================

@register_data_source("neighbors")
class SimulationNeighbors(BaseDataSource):
    """
    Query agents near a specific position or agent.

    Useful for:
    - Finding nearby agents
    - Collision detection
    - Interaction candidates
    - Local density analysis
    """

    @define
    class Config:
        world_id: str
        center_position: list[float] = field(factory=list)
        center_agent_id: str = ""
        radius: float = 10.0
        agent_type_filter: str = ""

    @define
    class State:
        world_id: str
        center: list[float]
        radius: float
        # Results
        neighbor_ids: list[str]
        neighbor_count: int
        average_distance: float
        nearest_distance: float

    @classmethod
    def get_schema(cls):
        return s_data_source({
            "world_id": a_str(required=True, description="World to search"),
            "center_position": a_list(a_num(), optional=True, description="Center position [x, y]"),
            "center_agent_id": a_str(optional=True, description="Center on this agent"),
            "radius": a_num(required=True, description="Search radius"),
            "agent_type_filter": a_str(optional=True, description="Filter by agent type"),
            # Results
            "center": a_list(a_num(), computed=True, description="Actual center used"),
            "neighbor_ids": a_list(a_str(), computed=True, description="Neighbor agent IDs"),
            "neighbor_count": a_num(computed=True, description="Number of neighbors"),
            "average_distance": a_num(computed=True, description="Average distance to neighbors"),
            "nearest_distance": a_num(computed=True, description="Distance to nearest neighbor"),
        })

    async def read(self, ctx) -> Any:
        world_id = ctx.config.world_id
        radius = ctx.config.radius

        # Determine center
        if ctx.config.center_agent_id:
            center_agent = SimulationAgent._agents.get(ctx.config.center_agent_id)
            if center_agent:
                center = center_agent.get("position", [0, 0])
            else:
                center = [0, 0]
        else:
            center = ctx.config.center_position if ctx.config.center_position else [0, 0]

        # Find neighbors
        neighbors = []
        distances = []

        for agent_id, agent in SimulationAgent._agents.items():
            if agent.get("world_id") != world_id:
                continue

            if ctx.config.agent_type_filter and agent.get("agent_type") != ctx.config.agent_type_filter:
                continue

            pos = agent.get("position", [0, 0])
            dist = math.sqrt(sum((a - b)**2 for a, b in zip(center, pos)))

            if dist <= radius and dist > 0:  # Exclude self (dist=0)
                neighbors.append(agent_id)
                distances.append(dist)

        avg_dist = sum(distances) / len(distances) if distances else 0.0
        nearest_dist = min(distances) if distances else 0.0

        return self.State(
            world_id=world_id,
            center=center,
            radius=radius,
            neighbor_ids=neighbors,
            neighbor_count=len(neighbors),
            average_distance=avg_dist,
            nearest_distance=nearest_dist,
        )

    async def _validate_config(self, config) -> list[str]:
        return []


# ============================================================================
# Function: simulation_distance
# ============================================================================

@register_function("distance")
class SimulationDistance(BaseFunction):
    """
    Calculate distance between two points in space.

    Supports multiple distance metrics:
    - Euclidean (straight line)
    - Manhattan (grid-based)
    - Chebyshev (diagonal)
    """

    @classmethod
    def get_schema(cls):
        return s_function(
            description="Calculate distance between two points",
            parameters=[
                FunctionParameter(
                    name="point1",
                    description="First point [x, y, z]",
                    type=CtyList(CtyNumber()),
                ),
                FunctionParameter(
                    name="point2",
                    description="Second point [x, y, z]",
                    type=CtyList(CtyNumber()),
                ),
                FunctionParameter(
                    name="metric",
                    description="Distance metric (euclidean, manhattan, chebyshev)",
                    type=CtyString(),
                ),
            ],
            return_type=FunctionReturnType(type=CtyNumber()),
        )

    async def call(self, point1: list[float], point2: list[float], metric: str = "euclidean") -> float:
        if metric == "euclidean":
            return math.sqrt(sum((a - b)**2 for a, b in zip(point1, point2)))
        elif metric == "manhattan":
            return sum(abs(a - b) for a, b in zip(point1, point2))
        elif metric == "chebyshev":
            return max(abs(a - b) for a, b in zip(point1, point2))
        else:
            return 0.0


# ============================================================================
# Function: simulation_entropy
# ============================================================================

@register_function("entropy")
class SimulationEntropy(BaseFunction):
    """
    Calculate Shannon entropy of a distribution.

    Measures disorder/unpredictability in a system.
    Higher entropy = more random/diverse
    Lower entropy = more ordered/uniform
    """

    @classmethod
    def get_schema(cls):
        return s_function(
            description="Calculate Shannon entropy of a distribution",
            parameters=[
                FunctionParameter(
                    name="probabilities",
                    description="Probability distribution (must sum to 1.0)",
                    type=CtyList(CtyNumber()),
                ),
            ],
            return_type=FunctionReturnType(type=CtyNumber()),
        )

    async def call(self, probabilities: list[float]) -> float:
        entropy = 0.0
        for p in probabilities:
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy


# ============================================================================
# Function: simulation_interpolate
# ============================================================================

@register_function("interpolate")
class SimulationInterpolate(BaseFunction):
    """
    Interpolate between two values.

    Useful for:
    - Smooth transitions
    - Easing functions
    - Animation curves
    """

    @classmethod
    def get_schema(cls):
        return s_function(
            description="Interpolate between two values",
            parameters=[
                FunctionParameter(
                    name="start",
                    description="Start value",
                    type=CtyNumber(),
                ),
                FunctionParameter(
                    name="end",
                    description="End value",
                    type=CtyNumber(),
                ),
                FunctionParameter(
                    name="t",
                    description="Interpolation factor (0.0 to 1.0)",
                    type=CtyNumber(),
                ),
                FunctionParameter(
                    name="easing",
                    description="Easing function (linear, ease_in, ease_out, ease_in_out)",
                    type=CtyString(),
                ),
            ],
            return_type=FunctionReturnType(type=CtyNumber()),
        )

    async def call(self, start: float, end: float, t: float, easing: str = "linear") -> float:
        # Clamp t to [0, 1]
        t = max(0.0, min(1.0, t))

        # Apply easing
        if easing == "ease_in":
            t = t * t
        elif easing == "ease_out":
            t = 1 - (1 - t) * (1 - t)
        elif easing == "ease_in_out":
            t = 3 * t * t - 2 * t * t * t

        # Linear interpolation
        return start + (end - start) * t


# ============================================================================
# Function: simulation_random_point
# ============================================================================

@register_function("random_point")
class SimulationRandomPoint(BaseFunction):
    """
    Generate a random point within bounds.

    Useful for:
    - Spawning agents
    - Random events
    - Procedural generation
    """

    @classmethod
    def get_schema(cls):
        return s_function(
            description="Generate random point within bounds",
            parameters=[
                FunctionParameter(
                    name="min_bounds",
                    description="Minimum bounds [x_min, y_min, z_min]",
                    type=CtyList(CtyNumber()),
                ),
                FunctionParameter(
                    name="max_bounds",
                    description="Maximum bounds [x_max, y_max, z_max]",
                    type=CtyList(CtyNumber()),
                ),
                FunctionParameter(
                    name="seed",
                    description="Random seed (use same seed for reproducible results)",
                    type=CtyNumber(),
                ),
            ],
            return_type=FunctionReturnType(type=CtyList(CtyNumber())),
        )

    async def call(self, min_bounds: list[float], max_bounds: list[float], seed: float = 0) -> list[float]:
        if seed != 0:
            random.seed(int(seed))

        return [
            random.uniform(min_b, max_b)
            for min_b, max_b in zip(min_bounds, max_bounds)
        ]
