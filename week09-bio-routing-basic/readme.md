# Week 9: Bio-Inspired Networking (Ant Colony Routing)

## Overview
This lab implements a self-optimizing network inspired by the foraging behavior of ant colonies. 
[cite_start]Nodes discover and maintain optimal paths by reinforcing successful routes with "pheromones".

## Key Concepts
| Concept | Description |
| :--- | :--- |
| **Pheromone Reinforcement** | [cite_start]Increasing the weight of a path after a successful message delivery[cite: 23]. |
| **Pheromone Decay** | [cite_start]The gradual reduction of path strength over time to forget obsolete routes[cite: 23]. |
| **Adaptive Path Selection** | Nodes prioritize forwarding to neighbors with the highest pheromone concentration. |
| **Loop Prevention** | Implementation of a "seen cache" to prevent broadcast storms in dense meshes. |

## Data Dictionary
| Component | Type | Description |
| :--- | :--- | :--- |
| `ph_manager.table` | `dict {int: float}` | Stores the current pheromone intensity for each known peer port. |
| `msg_queue` | `list [str]` | Buffer for unique messages awaiting a strong enough path for forwarding. |
| `seen_cache` | `set {str}` | Prevents redundant processing of messages that have already passed through this node. |

## Run Instructions
1. Open multiple terminals and launch nodes with unique ports:
   - `python node.py 13000 13001 13002`
2. Type a message to initiate pheromone-based forwarding. 
3. Use the `status` command to monitor the real-time decay and reinforcement of paths.

## Expected Behavior
The network will naturally "forget" unreachable nodes as their pheromone values evaporate below the `PHEROMONE_THRESHOLD`.
Successful transmissions will strengthen paths, creating a self-healing and adaptive routing infrastructure.