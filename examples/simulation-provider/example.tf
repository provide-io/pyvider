# Simulation Provider - Comprehensive Example Terraform Configuration
#
# This example demonstrates agent-based simulation and emergent behavior modeling:
# - Predator-prey ecosystem dynamics
# - Flocking and social behaviors
# - Spatial analysis and clustering
# - Emergent pattern detection
# - Complex adaptive systems

terraform {
  required_providers {
    simulation = {
      source  = "local/provide/simulation"
      version = "1.0.0"
    }
  }
}

# ============================================================================
# Provider Configuration
# ============================================================================

provider "simulation" {
  simulation_speed = 1.0
  max_iterations   = 1000
  random_seed      = 42
}

# ============================================================================
# Simulation Worlds - Different Topologies
# ============================================================================

# Euclidean world for predator-prey ecosystem
resource "simulation_world" "ecosystem" {
  name       = "predator-prey-ecosystem"
  dimensions = [200.0, 200.0]
  topology   = "euclidean"

  gravity  = 0.0
  friction = 0.1

  resources = {
    food  = 1000.0
    water = 500.0
  }

  environment = {
    temperature = 20.0
    season      = "spring"
  }

  tags = {
    Type        = "ecosystem"
    Scenario    = "predator-prey"
    Environment = "development"
  }
}

# Toroidal world for flocking behavior (wrap-around edges)
resource "simulation_world" "flock" {
  name       = "flocking-simulation"
  dimensions = [150.0, 150.0]
  topology   = "toroidal"

  friction = 0.05

  tags = {
    Type     = "social-behavior"
    Scenario = "flocking"
  }
}

# Graph-based world for network dynamics
resource "simulation_world" "network" {
  name       = "social-network"
  dimensions = [1.0, 1.0]  # Graph topology doesn't use spatial dimensions
  topology   = "graph"

  tags = {
    Type     = "network"
    Scenario = "information-spread"
  }
}

# ============================================================================
# Behavior Rules - Emergent Dynamics
# ============================================================================

# Prey behavior: Seek food
resource "simulation_rule" "prey_seek_food" {
  name        = "prey-seek-food"
  world_id    = simulation_world.ecosystem.id
  rule_type   = "seek"
  priority    = 20

  conditions = {
    agent_type    = "prey"
    energy_below  = "50.0"
    resource_type = "food"
  }

  actions = {
    move_towards = "nearest_resource"
    speed        = "2.0"
  }

  effects = {
    energy_gain     = "10.0"
    resource_consume = "1.0"
  }
}

# Prey behavior: Flee from predators
resource "simulation_rule" "prey_flee_predator" {
  name        = "prey-flee-predator"
  world_id    = simulation_world.ecosystem.id
  rule_type   = "flee"
  priority    = 50  # Higher priority than seeking food

  conditions = {
    agent_type   = "prey"
    detect_type  = "predator"
    detect_range = "15.0"
  }

  actions = {
    move_away = "detected_agent"
    speed     = "3.0"
  }

  effects = {
    energy_cost = "0.5"
    fear_level  = "10.0"
  }
}

# Prey behavior: Reproduce
resource "simulation_rule" "prey_reproduce" {
  name        = "prey-reproduce"
  world_id    = simulation_world.ecosystem.id
  rule_type   = "reproduce"
  priority    = 10

  conditions = {
    agent_type   = "prey"
    energy_above = "80.0"
    population_below = "100"
  }

  actions = {
    spawn_agent = "prey"
    spawn_count = "1"
  }

  effects = {
    energy_cost = "40.0"
  }
}

# Predator behavior: Hunt prey
resource "simulation_rule" "predator_hunt" {
  name        = "predator-hunt-prey"
  world_id    = simulation_world.ecosystem.id
  rule_type   = "seek"
  priority    = 40

  conditions = {
    agent_type   = "predator"
    detect_type  = "prey"
    detect_range = "20.0"
  }

  actions = {
    move_towards = "nearest_prey"
    speed        = "2.5"
  }

  effects = {
    energy_cost = "0.3"
  }
}

# Predator behavior: Consume prey
resource "simulation_rule" "predator_consume" {
  name        = "predator-consume-prey"
  world_id    = simulation_world.ecosystem.id
  rule_type   = "consume"
  priority    = 60

  conditions = {
    agent_type     = "predator"
    distance_below = "1.0"
    target_type    = "prey"
  }

  actions = {
    consume_agent = "prey"
  }

  effects = {
    energy_gain = "30.0"
  }
}

# Predator behavior: Wander when no prey detected
resource "simulation_rule" "predator_wander" {
  name        = "predator-wander"
  world_id    = simulation_world.ecosystem.id
  rule_type   = "wander"
  priority    = 5  # Lowest priority - only when no other rules apply

  conditions = {
    agent_type = "predator"
    idle       = "true"
  }

  actions = {
    random_walk = "true"
    speed       = "1.0"
  }

  effects = {
    energy_cost = "0.1"
  }
}

# Flocking rule: Cohesion (move towards center of nearby flock)
resource "simulation_rule" "flock_cohesion" {
  name        = "flock-cohesion"
  world_id    = simulation_world.flock.id
  rule_type   = "seek"
  priority    = 30

  conditions = {
    agent_type   = "bird"
    neighbors_min = "3"
    range        = "15.0"
  }

  actions = {
    move_towards = "flock_center"
    speed        = "1.5"
    weight       = "0.3"
  }

  effects = {
    cohesion_force = "1.0"
  }
}

# Flocking rule: Separation (avoid crowding)
resource "simulation_rule" "flock_separation" {
  name        = "flock-separation"
  world_id    = simulation_world.flock.id
  rule_type   = "flee"
  priority    = 50

  conditions = {
    agent_type     = "bird"
    distance_below = "5.0"
  }

  actions = {
    move_away = "neighbors"
    speed     = "2.0"
    weight    = "0.5"
  }

  effects = {
    separation_force = "1.0"
  }
}

# Flocking rule: Alignment (match velocity of nearby flock)
resource "simulation_rule" "flock_alignment" {
  name        = "flock-alignment"
  world_id    = simulation_world.flock.id
  rule_type   = "align"
  priority    = 40

  conditions = {
    agent_type   = "bird"
    neighbors_min = "2"
    range        = "12.0"
  }

  actions = {
    match_velocity = "flock_average"
    weight         = "0.4"
  }

  effects = {
    alignment_force = "1.0"
  }
}

# ============================================================================
# Agents - Initial Population
# ============================================================================

# Prey population (herbivores)
resource "simulation_agent" "prey" {
  count = 50

  name     = "prey-${count.index + 1}"
  world_id = simulation_world.ecosystem.id

  agent_type = "prey"

  position = [
    provider::simulation::random_point(0, 200, count.index * 2),
    provider::simulation::random_point(0, 200, count.index * 2 + 1),
  ]

  velocity     = [0.0, 0.0]
  energy       = 70.0
  vision_range = 10.0

  behaviors = [
    simulation_rule.prey_seek_food.id,
    simulation_rule.prey_flee_predator.id,
    simulation_rule.prey_reproduce.id,
  ]

  properties = {
    max_energy = "100.0"
    age        = "0"
    species    = "herbivore"
  }

  tags = {
    Type = "prey"
    Role = "consumer"
  }
}

# Predator population (carnivores)
resource "simulation_agent" "predator" {
  count = 10

  name     = "predator-${count.index + 1}"
  world_id = simulation_world.ecosystem.id

  agent_type = "predator"

  position = [
    provider::simulation::random_point(0, 200, count.index * 100),
    provider::simulation::random_point(0, 200, count.index * 100 + 50),
  ]

  velocity     = [0.0, 0.0]
  energy       = 80.0
  vision_range = 20.0

  behaviors = [
    simulation_rule.predator_hunt.id,
    simulation_rule.predator_consume.id,
    simulation_rule.predator_wander.id,
  ]

  properties = {
    max_energy = "120.0"
    age        = "0"
    species    = "carnivore"
  }

  tags = {
    Type = "predator"
    Role = "apex-consumer"
  }
}

# Flocking birds
resource "simulation_agent" "bird" {
  count = 30

  name     = "bird-${count.index + 1}"
  world_id = simulation_world.flock.id

  agent_type = "bird"

  position = [
    provider::simulation::random_point(0, 150, count.index * 3),
    provider::simulation::random_point(0, 150, count.index * 3 + 1),
  ]

  velocity = [
    provider::simulation::random_point(-2, 2, count.index * 5),
    provider::simulation::random_point(-2, 2, count.index * 5 + 1),
  ]

  energy       = 100.0
  vision_range = 15.0

  behaviors = [
    simulation_rule.flock_cohesion.id,
    simulation_rule.flock_separation.id,
    simulation_rule.flock_alignment.id,
  ]

  properties = {
    flock_id = "${floor(count.index / 10)}"
  }
}

# ============================================================================
# Data Sources - Emergent Behavior Analysis
# ============================================================================

# Ecosystem statistics
data "simulation_statistics" "ecosystem_stats" {
  world_id = simulation_world.ecosystem.id

  depends_on = [
    simulation_agent.prey,
    simulation_agent.predator,
  ]
}

# Flocking statistics
data "simulation_statistics" "flock_stats" {
  world_id = simulation_world.flock.id

  depends_on = [
    simulation_agent.bird,
  ]
}

# Spatial neighbors for a specific prey agent
data "simulation_neighbors" "prey_neighbors" {
  world_id = simulation_world.ecosystem.id
  agent_id = simulation_agent.prey[0].id
  radius   = 15.0

  filter_type = "predator"
}

# Find flockmates for first bird
data "simulation_neighbors" "bird_flockmates" {
  world_id = simulation_world.flock.id
  agent_id = simulation_agent.bird[0].id
  radius   = 12.0

  filter_type = "bird"
}

# ============================================================================
# Local Values - Using Provider Functions
# ============================================================================

locals {
  # Distance calculations between agents
  prey_predator_distance = provider::simulation::distance(
    simulation_agent.prey[0].position,
    simulation_agent.predator[0].position,
    "euclidean"
  )

  manhattan_distance = provider::simulation::distance(
    [10.0, 20.0],
    [40.0, 60.0],
    "manhattan"
  )

  # Entropy analysis for population distribution
  # Calculate probabilities from agent type counts
  total_agents = data.simulation_statistics.ecosystem_stats.total_agents
  prey_count   = data.simulation_statistics.ecosystem_stats.agent_counts["prey"]
  pred_count   = data.simulation_statistics.ecosystem_stats.agent_counts["predator"]

  prey_probability = local.prey_count / local.total_agents
  pred_probability = local.pred_count / local.total_agents

  population_entropy = provider::simulation::entropy([
    local.prey_probability,
    local.pred_probability,
  ])

  # Interpolation for smooth animations
  interpolated_position = provider::simulation::interpolate(
    [0.0, 0.0],
    [100.0, 100.0],
    0.5,  # 50% between start and end
    "ease_in_out"
  )

  # Random spawning points
  spawn_point_1 = provider::simulation::random_point(0, 200, 12345)
  spawn_point_2 = provider::simulation::random_point(0, 200, 67890)
}

# ============================================================================
# Outputs - Simulation Insights
# ============================================================================

# World Information
output "ecosystem_id" {
  description = "Ecosystem world ID"
  value       = simulation_world.ecosystem.id
}

output "ecosystem_dimensions" {
  description = "World dimensions"
  value       = simulation_world.ecosystem.dimensions
}

output "ecosystem_topology" {
  description = "World topology type"
  value       = simulation_world.ecosystem.topology
}

# Population Statistics
output "total_agents" {
  description = "Total number of agents in ecosystem"
  value       = data.simulation_statistics.ecosystem_stats.total_agents
}

output "agent_type_counts" {
  description = "Count of each agent type"
  value       = data.simulation_statistics.ecosystem_stats.agent_counts
}

output "prey_count" {
  description = "Number of prey agents"
  value       = local.prey_count
}

output "predator_count" {
  description = "Number of predator agents"
  value       = local.pred_count
}

output "predator_prey_ratio" {
  description = "Ratio of predators to prey"
  value       = local.pred_count / local.prey_count
}

# Energy Metrics
output "average_energy" {
  description = "Average energy across all agents"
  value       = data.simulation_statistics.ecosystem_stats.average_energy
}

output "total_energy" {
  description = "Total energy in the system"
  value       = data.simulation_statistics.ecosystem_stats.total_energy
}

# Spatial Metrics
output "spatial_variance" {
  description = "Spatial distribution variance (clustering measure)"
  value       = data.simulation_statistics.ecosystem_stats.spatial_variance
}

output "clustering_coefficient" {
  description = "Clustering coefficient (0=dispersed, 1=clustered)"
  value       = data.simulation_statistics.ecosystem_stats.clustering_coefficient
}

output "average_neighbor_distance" {
  description = "Average distance to nearest neighbor"
  value       = data.simulation_statistics.ecosystem_stats.average_neighbor_distance
}

# Emergent Behavior Metrics
output "system_entropy" {
  description = "Shannon entropy of agent type distribution"
  value       = data.simulation_statistics.ecosystem_stats.entropy
}

output "population_entropy" {
  description = "Calculated population entropy (local)"
  value       = local.population_entropy
}

output "velocity_variance" {
  description = "Variance in agent velocities (activity measure)"
  value       = data.simulation_statistics.ecosystem_stats.velocity_variance
}

# Neighbor Analysis
output "prey_nearby_predators" {
  description = "Predators near first prey agent"
  value       = length(data.simulation_neighbors.prey_neighbors.neighbors)
}

output "prey_danger_level" {
  description = "Danger assessment for prey"
  value = length(data.simulation_neighbors.prey_neighbors.neighbors) > 0 ? "HIGH" : "LOW"
}

output "bird_flockmates" {
  description = "Number of flockmates near first bird"
  value       = length(data.simulation_neighbors.bird_flockmates.neighbors)
}

# Distance Calculations
output "prey_predator_distance" {
  description = "Distance between first prey and first predator"
  value       = local.prey_predator_distance
}

output "manhattan_distance_example" {
  description = "Example Manhattan distance calculation"
  value       = local.manhattan_distance
}

# Flocking Statistics
output "flock_agent_count" {
  description = "Number of birds in flock simulation"
  value       = data.simulation_statistics.flock_stats.total_agents
}

output "flock_clustering" {
  description = "Flock clustering coefficient"
  value       = data.simulation_statistics.flock_stats.clustering_coefficient
}

output "flock_cohesion" {
  description = "Flock cohesion measure"
  value       = 1.0 - data.simulation_statistics.flock_stats.spatial_variance
}

# Agent Details
output "sample_prey_agent" {
  description = "Details of first prey agent"
  value = {
    id           = simulation_agent.prey[0].id
    name         = simulation_agent.prey[0].name
    position     = simulation_agent.prey[0].position
    energy       = simulation_agent.prey[0].energy
    vision_range = simulation_agent.prey[0].vision_range
    behaviors    = length(simulation_agent.prey[0].behaviors)
  }
}

output "sample_predator_agent" {
  description = "Details of first predator agent"
  value = {
    id           = simulation_agent.predator[0].id
    name         = simulation_agent.predator[0].name
    position     = simulation_agent.predator[0].position
    energy       = simulation_agent.predator[0].energy
    vision_range = simulation_agent.predator[0].vision_range
    behaviors    = length(simulation_agent.predator[0].behaviors)
  }
}

# Behavior Rules Summary
output "active_rules" {
  description = "Summary of active behavior rules"
  value = {
    ecosystem_rules = [
      simulation_rule.prey_seek_food.name,
      simulation_rule.prey_flee_predator.name,
      simulation_rule.prey_reproduce.name,
      simulation_rule.predator_hunt.name,
      simulation_rule.predator_consume.name,
      simulation_rule.predator_wander.name,
    ]
    flock_rules = [
      simulation_rule.flock_cohesion.name,
      simulation_rule.flock_separation.name,
      simulation_rule.flock_alignment.name,
    ]
  }
}

# System Summary
output "simulation_summary" {
  description = "Complete simulation summary"
  value = {
    worlds = {
      ecosystem = {
        id         = simulation_world.ecosystem.id
        agents     = data.simulation_statistics.ecosystem_stats.total_agents
        prey       = local.prey_count
        predators  = local.pred_count
        entropy    = data.simulation_statistics.ecosystem_stats.entropy
        clustering = data.simulation_statistics.ecosystem_stats.clustering_coefficient
      }
      flock = {
        id         = simulation_world.flock.id
        agents     = data.simulation_statistics.flock_stats.total_agents
        clustering = data.simulation_statistics.flock_stats.clustering_coefficient
        cohesion   = 1.0 - data.simulation_statistics.flock_stats.spatial_variance
      }
    }
    emergent_behaviors = {
      population_balance = local.pred_count / local.prey_count
      system_entropy     = local.population_entropy
      spatial_clustering = data.simulation_statistics.ecosystem_stats.clustering_coefficient
      flock_cohesion     = 1.0 - data.simulation_statistics.flock_stats.spatial_variance
    }
    health_indicators = {
      total_energy       = data.simulation_statistics.ecosystem_stats.total_energy
      average_energy     = data.simulation_statistics.ecosystem_stats.average_energy
      velocity_variance  = data.simulation_statistics.ecosystem_stats.velocity_variance
    }
  }
}
