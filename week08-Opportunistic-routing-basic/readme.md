# Week 8: Opportunistic Routing Implementation

## Overview
Traditional routing relies on fixed paths, but opportunistic networking thrives on intermittent connectivity. 
This lab implements a system where nodes forward messages based on delivery probability rather than fixed routes.

## Learning Objectives
Students will implement a delivery probability table to track peer reliability over time. 
The lab focuses on adaptive decision-making and preventing message loops in a decentralized environment.

## Key Concepts
| Concept | Description |
| :--- | :--- |
| **Delivery Probability** | A dynamic score representing the likelihood of a peer successfully delivering a packet. |
| **Store-Carry-Forward** | A strategy where messages are queued locally until a suitable forwarding opportunity arises. |
| **Duplicate Suppression** | A mechanism using a "seen set" to prevent the same message from being forwarded indefinitely. |
| **Adaptive Decay** | The automatic reduction of a peer's reliability score following a failed transmission attempt. |

## System Parameters (`config.py`)
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `FORWARD_THRESHOLD` | `0.5` | Minimum probability score needed to attempt an opportunistic forward. |
| `UPDATE_INTERVAL` | `5` | The frequency in seconds at which the node checks its queue for forwarding. |
| `DECAY_FACTOR` | `0.8` | The multiplier applied to a peer's probability score after a failed attempt. |
| `BOOST_AMOUNT` | `0.1` | The constant added to a peer's probability score after a successful delivery. |

## Data Dictionary
| Component | Type | Description |
| :--- | :--- | :--- |
| `table` | `dict {int: float}` | Maps peer ports to their current calculated delivery probability scores. |
| `message_queue` | `list [str]` | Stores pending text messages waiting for a valid forwarding window. |
| `seen_messages` | `set {str}` | Tracks historical message content to prevent redundant processing and network loops. |

## Run Instructions
1. **Launch Nodes**: Open separate terminals and run `python node.py [port] [peer_ports]`.
   - Node A: `python node.py 9000 9001 9002`
   - Node B: `python node.py 9001 9000 9002`
   - Node C: `python node.py 9002 9000 9001`
2. **Interact**: Type a message to send it, or use `table` to view current scores.

## Expected Behaviour
The `seen_messages` set ensures that each unique message is only added to the forwarding queue once. 
If a node goes offline, its score will decay, causing messages to be stored until the node becomes reachable again.