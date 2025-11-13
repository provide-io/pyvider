# Simulation Provider - Pyvider Example

A **novel** Terraform provider demonstrating that infrastructure-as-code can manage **any domain**, not just cloud resources. This provider enables agent-based simulation, emergent behavior modeling, and complex adaptive systems through declarative Terraform configuration.

## Why This Is Unique

Traditional Terraform providers manage cloud infrastructure (AWS, Azure, GCP) or SaaS platforms. This provider demonstrates that **Terraform's declarative model is ideal for ANY system requiring reproducible, versioned, stateful configuration** - including:

- **Agent-Based Modeling**: Multi-agent systems with autonomous behaviors
- **Game Mechanics**: Prototyping game AI, NPC behaviors, and emergent gameplay
- **Ecosystem Simulation**: Population dynamics, predator-prey models, disease spread
- **Social Systems**: Market dynamics, crowd behavior, information propagation
- **Complex Adaptive Systems**: Emergent patterns from simple rules

## Features Demonstrated

### Novel Use Cases

- **Predator-Prey Dynamics**: Classic Lotka-Volterra ecosystem modeling
- **Flocking Behavior**: Craig Reynolds' Boids algorithm (cohesion, separation, alignment)
- **Spatial Analysis**: Clustering, entropy, neighbor detection
- **Emergent Patterns**: Complex behaviors arising from simple rules
- **Reproducible Simulations**: Version-controlled simulation parameters

### Pyvider Framework Features

- **3 Resource Types**: Worlds (environments), Agents (entities), Rules (behaviors)
- **2 Data Sources**: Statistics (emergent metrics), Neighbors (spatial queries)
- **4 Provider Functions**: Distance, Entropy, Interpolation, Random generation
- **Type-Safe Configuration**: attrs-based data classes
- **Async/Await**: Efficient concurrent simulation
- **Complex State Management**: Spatial coordinates, velocities, emergent metrics

---

## Quick Start

### 1. Install Dependencies

```bash
cd examples/simulation-provider
pip install pyvider
```

Or using `uv`:
```bash
uv sync
```

### 2. Install the Provider

```bash
pyvider install
```

This creates a symlink in your Terraform plugins directory:
```
~/.terraform.d/plugins/local/provide/simulation/1.0.0/<platform>/
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Apply Configuration

```bash
terraform plan
terraform apply
```

### 5. Observe Emergent Behaviors

```bash
terraform output simulation_summary
```

Example output:
```
simulation_summary = {
  "emergent_behaviors" = {
    "flock_cohesion" = 0.87
    "population_balance" = 0.2
    "spatial_clustering" = 0.43
    "system_entropy" = 0.72
  }
  "health_indicators" = {
    "average_energy" = 65.3
    "total_energy" = 3916.0
    "velocity_variance" = 2.1
  }
  "worlds" = {
    "ecosystem" = {
      "agents" = 60
      "clustering" = 0.43
      "entropy" = 0.72
      "id" = "world-000001"
      "predators" = 10
      "prey" = 50
    }
    "flock" = {
      "agents" = 30
      "clustering" = 0.81
      "cohesion" = 0.87
      "id" = "world-000002"
    }
  }
}
```

---

## Example Scenarios

### 1. Predator-Prey Ecosystem

A classic Lotka-Volterra model demonstrating population cycles:

```hcl
resource "simulation_world" "ecosystem" {
  name       = "predator-prey"
  dimensions = [200.0, 200.0]
  topology   = "euclidean"

  resources = {
    food = 1000.0
  }
}

# Prey: seek food, flee predators, reproduce
resource "simulation_agent" "prey" {
  count      = 50
  world_id   = simulation_world.ecosystem.id
  agent_type = "prey"
  energy     = 70.0

  behaviors = [
    simulation_rule.prey_seek_food.id,
    simulation_rule.prey_flee_predator.id,
    simulation_rule.prey_reproduce.id,
  ]
}

# Predators: hunt prey, consume, wander
resource "simulation_agent" "predator" {
  count      = 10
  world_id   = simulation_world.ecosystem.id
  agent_type = "predator"
  energy     = 80.0

  behaviors = [
    simulation_rule.predator_hunt.id,
    simulation_rule.predator_consume.id,
    simulation_rule.predator_wander.id,
  ]
}
```

**Expected Emergent Behavior**: Population cycles where prey booms lead to predator booms, followed by prey crashes and predator crashes.

### 2. Flocking Birds (Boids)

Craig Reynolds' famous flocking algorithm with three simple rules:

```hcl
resource "simulation_world" "flock" {
  name       = "flocking-simulation"
  dimensions = [150.0, 150.0]
  topology   = "toroidal"  # Wrap-around edges
  friction   = 0.05
}

resource "simulation_agent" "bird" {
  count        = 30
  world_id     = simulation_world.flock.id
  agent_type   = "bird"
  vision_range = 15.0

  behaviors = [
    simulation_rule.flock_cohesion.id,    # Move towards flock center
    simulation_rule.flock_separation.id,   # Avoid crowding
    simulation_rule.flock_alignment.id,    # Match neighbors' velocity
  ]
}
```

**Expected Emergent Behavior**: Birds spontaneously form cohesive flocks with organic, flowing motion patterns.

### 3. Disease Spread Simulation

Model epidemic dynamics in a population:

```hcl
resource "simulation_world" "population" {
  name       = "disease-spread"
  dimensions = [100.0, 100.0]
  topology   = "euclidean"
}

# Susceptible agents
resource "simulation_agent" "susceptible" {
  count      = 90
  agent_type = "susceptible"
  # ... random wander behavior
}

# Initially infected agents
resource "simulation_agent" "infected" {
  count      = 10
  agent_type = "infected"
  # ... behavior to spread infection on contact
}

resource "simulation_rule" "infection_spread" {
  rule_type = "transmit"
  conditions = {
    distance_below = "2.0"  # Close contact
    agent_type     = "infected"
    target_type    = "susceptible"
  }
  effects = {
    convert_to_type = "infected"
    probability     = "0.3"
  }
}
```

**Expected Emergent Behavior**: SIR model dynamics showing infection waves and eventual equilibrium.

### 4. Traffic Flow Simulation

Model vehicle behavior and congestion:

```hcl
resource "simulation_world" "highway" {
  name       = "traffic-flow"
  dimensions = [1000.0, 10.0]  # Long, narrow highway
  topology   = "euclidean"
}

resource "simulation_agent" "vehicle" {
  count      = 100
  agent_type = "car"

  behaviors = [
    simulation_rule.maintain_speed.id,
    simulation_rule.follow_distance.id,
    simulation_rule.avoid_collision.id,
  ]
}
```

**Expected Emergent Behavior**: Phantom traffic jams forming from small perturbations.

### 5. Market Dynamics

Model trading behavior and price discovery:

```hcl
resource "simulation_world" "market" {
  name     = "stock-market"
  topology = "graph"  # Network-based, not spatial
}

resource "simulation_agent" "trader" {
  count      = 50
  agent_type = "trader"

  properties = {
    risk_tolerance = "0.7"
    capital        = "10000.0"
  }

  behaviors = [
    simulation_rule.buy_low.id,
    simulation_rule.sell_high.id,
    simulation_rule.follow_trend.id,
  ]
}
```

**Expected Emergent Behavior**: Price bubbles, crashes, and trending behavior from individual trading strategies.

---

## Architecture

### Component Overview

```
Terraform Configuration (HCL)
         ↓
   Provider Functions
    (distance, entropy, interpolate, random_point)
         ↓
   Simulation Provider
         ↓
    ┌────────────┬──────────────┬─────────────┐
    ↓            ↓              ↓             ↓
  World       Agent          Rule      Data Sources
(environ)  (entities)    (behaviors)   (analysis)
    ↓            ↓              ↓             ↓
         Simulation Engine
         (emergent behaviors)
```

### State Management

```
Config (HCL) → Terraform → Provider → Simulation State
                              ↓
                    Agent Positions & Velocities
                    World Resources & Physics
                    Emergent Metrics
                              ↓
                    Private State (encrypted)
                              ↓
                       msgpack + AES-256
```

### Emergent Behavior Detection

The provider calculates emergent properties from individual agent behaviors:

- **Clustering Coefficient**: Measures spatial grouping
- **Entropy**: Measures system disorder/uniformity
- **Velocity Variance**: Measures activity levels
- **Population Dynamics**: Tracks type counts over time
- **Spatial Statistics**: Distribution, nearest neighbors, density

---

## Project Structure

```
simulation-provider/
├── provider.py          # Provider implementation (3 resources, 2 data sources, 4 functions)
├── pyproject.toml       # Python project configuration
├── pyvider.toml         # Pyvider runtime configuration
├── example.tf           # Comprehensive Terraform examples
└── README.md            # This file
```

---

## API Reference

### Provider Configuration

```hcl
provider "simulation" {
  simulation_speed = 1.0      # Simulation time scale
  max_iterations   = 1000     # Maximum simulation steps
  random_seed      = 42       # Reproducibility
}
```

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `simulation_speed` | number | No | Time scale multiplier (default: 1.0) |
| `max_iterations` | number | No | Maximum simulation steps (default: 1000) |
| `random_seed` | number | No | Random seed for reproducibility |

### Resources

#### simulation_world

Defines a simulation environment with spatial dimensions and physics.

```hcl
resource "simulation_world" "example" {
  name       = "my-world"
  dimensions = [200.0, 200.0]
  topology   = "euclidean"  # euclidean, toroidal, graph

  gravity  = 0.0
  friction = 0.1

  resources = {
    food  = 1000.0
    water = 500.0
  }

  environment = {
    temperature = 20.0
  }

  tags = {
    Type = "ecosystem"
  }
}
```

**Attributes:**

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `id` | string | No | Yes | World ID |
| `name` | string | Yes | No | World name |
| `dimensions` | list(number) | No | No | Spatial dimensions (default: [100, 100]) |
| `topology` | string | No | No | Spatial topology (default: euclidean) |
| `gravity` | number | No | No | Gravity strength (default: 0.0) |
| `friction` | number | No | No | Friction coefficient (default: 0.0) |
| `resources` | map(number) | No | No | Available resources |
| `environment` | map(string) | No | No | Environment variables |
| `tags` | map(string) | No | No | Tags |
| `created_at` | string | No | Yes | Creation timestamp |

**Topologies:**
- `euclidean`: Standard 2D plane with distance = √(dx² + dy²)
- `toroidal`: Wrap-around edges (like Pac-Man)
- `graph`: Network topology (non-spatial)

#### simulation_agent

Defines an autonomous agent with position, velocity, and behaviors.

```hcl
resource "simulation_agent" "example" {
  name     = "agent-001"
  world_id = simulation_world.example.id

  agent_type   = "prey"
  position     = [50.0, 50.0]
  velocity     = [1.0, 0.0]
  energy       = 100.0
  vision_range = 10.0

  behaviors = [
    simulation_rule.seek_food.id,
    simulation_rule.flee_predator.id,
  ]

  properties = {
    max_energy = "150.0"
    species    = "herbivore"
  }

  tags = {
    Type = "prey"
  }
}
```

**Attributes:**

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `id` | string | No | Yes | Agent ID |
| `name` | string | Yes | No | Agent name |
| `world_id` | string | Yes | No | Parent world ID |
| `agent_type` | string | Yes | No | Agent type/class |
| `position` | list(number) | No | No | Spatial position (default: [0, 0]) |
| `velocity` | list(number) | No | No | Velocity vector (default: [0, 0]) |
| `energy` | number | No | No | Energy level (default: 100.0) |
| `vision_range` | number | No | No | Detection range (default: 10.0) |
| `behaviors` | list(string) | No | No | Rule IDs to apply |
| `properties` | map(string) | No | No | Custom properties |
| `tags` | map(string) | No | No | Tags |
| `state` | string | No | Yes | Current state |
| `created_at` | string | No | Yes | Creation timestamp |

#### simulation_rule

Defines behavior rules with conditions, actions, and effects.

```hcl
resource "simulation_rule" "seek_food" {
  name      = "prey-seek-food"
  world_id  = simulation_world.example.id
  rule_type = "seek"
  priority  = 20

  conditions = {
    agent_type   = "prey"
    energy_below = "50.0"
  }

  actions = {
    move_towards = "nearest_resource"
    speed        = "2.0"
  }

  effects = {
    energy_gain = "10.0"
  }
}
```

**Attributes:**

| Attribute | Type | Required | Computed | Description |
|-----------|------|----------|----------|-------------|
| `id` | string | No | Yes | Rule ID |
| `name` | string | Yes | No | Rule name |
| `world_id` | string | Yes | No | Parent world ID |
| `rule_type` | string | Yes | No | Rule type (seek, flee, wander, consume, reproduce, align, transmit) |
| `priority` | number | No | No | Execution priority (default: 10) |
| `conditions` | map(string) | No | No | Activation conditions |
| `actions` | map(string) | No | No | Actions to perform |
| `effects` | map(string) | No | No | State changes |
| `enabled` | bool | No | Yes | Rule enabled status |
| `created_at` | string | No | Yes | Creation timestamp |

**Rule Types:**
- `seek`: Move towards target
- `flee`: Move away from target
- `wander`: Random walk
- `consume`: Remove/convert target
- `reproduce`: Spawn new agent
- `align`: Match velocity with neighbors
- `transmit`: Transfer state to target

### Data Sources

#### simulation_statistics

Query emergent behavior metrics for a world.

```hcl
data "simulation_statistics" "stats" {
  world_id = simulation_world.example.id
}

output "entropy" {
  value = data.simulation_statistics.stats.entropy
}
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `world_id` | string | World to analyze (required) |
| `id` | string | Statistics ID (computed) |
| `total_agents` | number | Total agent count (computed) |
| `agent_counts` | map(number) | Count per agent type (computed) |
| `average_energy` | number | Mean energy across all agents (computed) |
| `total_energy` | number | Sum of all agent energy (computed) |
| `spatial_variance` | number | Position distribution variance (computed) |
| `clustering_coefficient` | number | Spatial clustering measure 0-1 (computed) |
| `average_neighbor_distance` | number | Mean nearest neighbor distance (computed) |
| `entropy` | number | Shannon entropy of type distribution (computed) |
| `velocity_variance` | number | Velocity distribution variance (computed) |

**Emergent Metrics Explained:**

- **Clustering Coefficient**: 0 = uniformly dispersed, 1 = highly clustered
- **Entropy**: 0 = all one type (ordered), higher = mixed types (disordered)
- **Spatial Variance**: Low = concentrated, high = spread out
- **Velocity Variance**: Low = static/uniform motion, high = chaotic movement

#### simulation_neighbors

Query neighboring agents within a radius.

```hcl
data "simulation_neighbors" "nearby" {
  world_id    = simulation_world.example.id
  agent_id    = simulation_agent.prey[0].id
  radius      = 15.0
  filter_type = "predator"
}

output "predator_count" {
  value = length(data.simulation_neighbors.nearby.neighbors)
}
```

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `world_id` | string | World to query (required) |
| `agent_id` | string | Center agent ID (required) |
| `radius` | number | Search radius (required) |
| `filter_type` | string | Filter by agent type (optional) |
| `id` | string | Query ID (computed) |
| `neighbors` | list(object) | Neighboring agents (computed) |
| `count` | number | Neighbor count (computed) |

**Neighbor Object:**
```hcl
{
  id       = "agent-000123"
  type     = "predator"
  distance = 8.3
  position = [45.2, 67.8]
}
```

### Functions

#### provider::simulation::distance

Calculate distance between two points using various metrics.

```hcl
locals {
  euclidean_dist = provider::simulation::distance(
    [10.0, 20.0],
    [40.0, 60.0],
    "euclidean"
  )

  manhattan_dist = provider::simulation::distance(
    [10.0, 20.0],
    [40.0, 60.0],
    "manhattan"
  )
}
```

**Parameters:**
- `point1` (list(number)) - First point coordinates
- `point2` (list(number)) - Second point coordinates
- `metric` (string) - Distance metric: "euclidean", "manhattan", "chebyshev"

**Returns:** number

**Metrics:**
- `euclidean`: √((x₂-x₁)² + (y₂-y₁)²)
- `manhattan`: |x₂-x₁| + |y₂-y₁|
- `chebyshev`: max(|x₂-x₁|, |y₂-y₁|)

#### provider::simulation::entropy

Calculate Shannon entropy of a probability distribution.

```hcl
locals {
  # Entropy of a fair coin flip
  coin_entropy = provider::simulation::entropy([0.5, 0.5])  # 1.0

  # Entropy of a biased coin
  biased_entropy = provider::simulation::entropy([0.9, 0.1])  # 0.469

  # Entropy of uniform distribution
  uniform_entropy = provider::simulation::entropy([0.25, 0.25, 0.25, 0.25])  # 2.0
}
```

**Parameters:**
- `probabilities` (list(number)) - Probability distribution (must sum to 1.0)

**Returns:** number (entropy in bits)

**Formula:** H = -Σ(p * log₂(p))

**Interpretation:**
- 0 = perfect order (one outcome certain)
- Higher = more disorder/uncertainty
- Maximum = log₂(n) for n equally likely outcomes

#### provider::simulation::interpolate

Interpolate between two points with easing functions.

```hcl
locals {
  # Linear interpolation (50% between points)
  linear_pos = provider::simulation::interpolate(
    [0.0, 0.0],
    [100.0, 100.0],
    0.5,
    "linear"
  )  # [50.0, 50.0]

  # Ease-in (slow start, fast end)
  ease_in_pos = provider::simulation::interpolate(
    [0.0, 0.0],
    [100.0, 100.0],
    0.5,
    "ease_in"
  )

  # Ease-out (fast start, slow end)
  ease_out_pos = provider::simulation::interpolate(
    [0.0, 0.0],
    [100.0, 100.0],
    0.5,
    "ease_out"
  )
}
```

**Parameters:**
- `start` (list(number)) - Starting point
- `end` (list(number)) - Ending point
- `t` (number) - Interpolation factor (0.0 to 1.0)
- `easing` (string) - Easing function: "linear", "ease_in", "ease_out", "ease_in_out"

**Returns:** list(number)

**Easing Functions:**
- `linear`: t
- `ease_in`: t²
- `ease_out`: 1 - (1-t)²
- `ease_in_out`: t < 0.5 ? 2t² : 1 - 2(1-t)²

#### provider::simulation::random_point

Generate random point within a range (deterministic from seed).

```hcl
locals {
  # Generate random x coordinate
  random_x = provider::simulation::random_point(0, 200, 12345)

  # Generate random y coordinate (different seed)
  random_y = provider::simulation::random_point(0, 200, 67890)

  # Use in agent position
  position = [
    provider::simulation::random_point(0, 200, count.index * 2),
    provider::simulation::random_point(0, 200, count.index * 2 + 1),
  ]
}
```

**Parameters:**
- `min` (number) - Minimum value
- `max` (number) - Maximum value
- `seed` (number) - Random seed (same seed = same output)

**Returns:** number

**Note:** Uses deterministic pseudo-random generation for reproducibility.

---

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=provider

# Run specific test
pytest -k test_agent_movement
```

### Type Checking

```bash
mypy provider.py
```

### Linting

```bash
ruff check provider.py
ruff format provider.py
```

### Debugging

Enable debug logging in `pyvider.toml`:

```toml
[logging]
level = "DEBUG"
format = "json"
```

Or set environment variable:

```bash
export PYVIDER_LOG_LEVEL=DEBUG
terraform plan
```

---

## Advanced Use Cases

### 1. Multi-World Simulations

Run multiple independent simulations:

```hcl
resource "simulation_world" "scenario_a" {
  name = "high-gravity"
  gravity = 9.8
}

resource "simulation_world" "scenario_b" {
  name = "low-gravity"
  gravity = 1.6
}

# Compare emergent behaviors across scenarios
data "simulation_statistics" "stats_a" {
  world_id = simulation_world.scenario_a.id
}

data "simulation_statistics" "stats_b" {
  world_id = simulation_world.scenario_b.id
}
```

### 2. Dynamic Behavior Rules

Use Terraform variables to configure simulation parameters:

```hcl
variable "predator_count" {
  type    = number
  default = 10
}

variable "prey_reproduction_rate" {
  type    = number
  default = 40.0  # Energy cost to reproduce
}

resource "simulation_agent" "predator" {
  count = var.predator_count
  # ...
}

resource "simulation_rule" "prey_reproduce" {
  effects = {
    energy_cost = "${var.prey_reproduction_rate}"
  }
}
```

### 3. Simulation Versioning

Use Terraform workspaces for different simulation iterations:

```bash
# Create experimental workspace
terraform workspace new experiment-1

# Test new behavior rules
terraform apply

# Compare with baseline
terraform workspace select default
```

### 4. A/B Testing Behaviors

Test different rule configurations:

```hcl
locals {
  aggressive_hunting = var.experiment == "aggressive"
}

resource "simulation_rule" "predator_hunt" {
  priority = local.aggressive_hunting ? 60 : 40

  actions = {
    speed = local.aggressive_hunting ? "3.0" : "2.5"
  }
}
```

---

## Performance Considerations

### Simulation Scale

| Agents | Rules | Performance |
|--------|-------|-------------|
| < 100 | < 20 | Excellent |
| 100-500 | 20-50 | Good |
| 500-1000 | 50-100 | Moderate |
| > 1000 | > 100 | Consider optimization |

### Optimization Tips

1. **Spatial Partitioning**: Use smaller world dimensions or multiple worlds
2. **Rule Priority**: Higher priority rules execute first, can short-circuit lower priority
3. **Vision Range**: Reduce `vision_range` to minimize neighbor queries
4. **Topology**: `graph` topology is faster than `euclidean` for non-spatial simulations

---

## Comparison with Traditional Approaches

### vs. NetLogo

| Feature | NetLogo | Simulation Provider |
|---------|---------|---------------------|
| Language | Custom DSL | HCL (Terraform) |
| Version Control | Manual | Git-native |
| Reproducibility | Manual seeds | Declarative state |
| Deployment | Desktop app | CLI/CI/CD |
| Integration | Limited | Terraform ecosystem |

### vs. Python Simulation Libraries

| Feature | Python (Mesa, SimPy) | Simulation Provider |
|---------|----------------------|---------------------|
| Flexibility | High | High |
| Infrastructure | Custom code | Declarative config |
| State Management | Manual | Automatic (Terraform) |
| Collaboration | Code reviews | Terraform workflows |
| Visualization | Custom | External (use outputs) |

### vs. Game Engines (Unity, Unreal)

| Feature | Game Engine | Simulation Provider |
|---------|-------------|---------------------|
| Graphics | Built-in | None (data-focused) |
| Physics | Advanced | Simple |
| Scripting | C#/C++ | HCL |
| Version Control | Assets + code | Configuration only |
| CI/CD | Complex | Native Terraform |

---

## Troubleshooting

### Provider Not Found

**Error:**
```
Error: Failed to query available provider packages
```

**Solution:**
```bash
pyvider install
ls -la ~/.terraform.d/plugins/local/provide/simulation/
```

### Agent Collisions

**Issue:** Agents overlap or collide unrealistically.

**Solution:** Add separation rule with higher priority:
```hcl
resource "simulation_rule" "avoid_collision" {
  priority = 100  # Highest priority
  rule_type = "flee"

  conditions = {
    distance_below = "1.0"
  }
}
```

### Population Extinction

**Issue:** All prey or all predators die out.

**Solution:** Adjust reproduction rates and energy costs:
```hcl
resource "simulation_rule" "prey_reproduce" {
  conditions = {
    energy_above = "60.0"  # Lower threshold
  }
  effects = {
    energy_cost = "30.0"  # Lower cost
  }
}
```

### Simulation Divergence

**Issue:** Same configuration produces different results.

**Solution:** Set explicit random seed:
```hcl
provider "simulation" {
  random_seed = 42  # Reproducible results
}
```

---

## Philosophical Implications

### Infrastructure as Code → System as Code

This provider demonstrates that **any system with state** can be managed declaratively:

- Traditional IaC: "What cloud resources should exist?"
- Simulation IaC: "What agents and behaviors should exist?"
- Future possibilities:
  - **ML Models as Code**: Declare neural network architectures
  - **Workflows as Code**: Business process orchestration
  - **Organizations as Code**: Team structures and roles
  - **Curriculum as Code**: Learning paths and dependencies

### Emergent Behavior from Declarative Rules

The provider shows how:
- **Simple rules** (seek, flee, align) produce **complex patterns** (flocking, cycles)
- **Local interactions** create **global properties** (clustering, entropy)
- **Declarative configuration** enables **reproducible complexity**

This mirrors how Terraform's declarative cloud infrastructure produces emergent system behaviors (scalability, resilience, cost patterns).

---

## Future Enhancements

Potential additions to make the simulation provider production-ready:

1. **Visualization**: Export agent positions as CSV/JSON for external rendering
2. **Real-time Updates**: WebSocket server for live simulation observation
3. **Performance**: Spatial partitioning (quadtrees) for large-scale simulations
4. **Advanced Physics**: Collision detection, momentum, energy fields
5. **Machine Learning**: Train agent behaviors using reinforcement learning
6. **Time Series**: Track metrics over time for trend analysis
7. **Multi-threading**: Parallel agent updates for large populations

---

## Resources

### Agent-Based Modeling

- [NetLogo Documentation](https://ccl.northwestern.edu/netlogo/docs/)
- [Mesa: Agent-Based Modeling in Python](https://mesa.readthedocs.io/)
- [Complexity Explorer](https://www.complexityexplorer.org/)

### Emergent Behavior

- [Boids Algorithm](http://www.red3d.com/cwr/boids/) - Craig Reynolds
- [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) - Conway
- [Lotka-Volterra Equations](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)

### Pyvider Framework

- [Pyvider Documentation](https://foundry.provide.io/pyvider/)
- [Terraform Provider Protocol](https://developer.hashicorp.com/terraform/plugin/terraform-plugin-protocol)

---

## Contributing

Ideas for additional scenarios:

- **Forest Fire Spread**: Cellular automaton with wind and moisture
- **Ant Colony Optimization**: Pheromone trails and path finding
- **Prisoner's Dilemma**: Game theory and cooperation evolution
- **Segregation Model**: Schelling's segregation dynamics
- **Epidemic Models**: SEIR models with vaccination strategies

---

## License

Apache 2.0 - See [LICENSE](../../LICENSE) for details.

---

**Made with ❤️ using [Pyvider](https://github.com/provide-io/pyvider)**

*Demonstrating that Terraform can manage ANY domain, not just cloud infrastructure.*
