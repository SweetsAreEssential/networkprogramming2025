# Week 8: Opportunistic Routing Implementation

## Overview
Traditional routing relies on fixed paths, but opportunistic networking thrives on intermittent connectivity. 
This lab implements a system where nodes forward messages based on the best available opportunity and delivery probability.

## Learning Objectives
Students will implement a delivery probability table to track peer reliability over time. 
The lab focuses on adaptive decision-making and the store-carry-forward mechanism used in delay-tolerant networks.

## Key Concepts
| Concept | Description |
| :--- | :--- |
| **Delivery Probability** | A dynamic score representing the likelihood of a peer successfully delivering a packet. |
| **Forward Threshold** | The minimum probability required to attempt a transmission, avoiding unreliable routes. |
| **Store-Carry-Forward** | A strategy where messages are queued locally until a suitable forwarding opportunity arises. |
| **Adaptive Learning** | The process of updating peer reliability scores based on real-time connection outcomes. |

## System Parameters (`config.py`)
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `FORWARD_THRESHOLD` | `0.5` | Minimum probability score needed to trigger an opportunistic forward. |
| `UPDATE_INTERVAL` | `5` | The frequency in seconds at which the node checks its queue for forwarding. |
| `DECAY_FACTOR` | `0.8` | The multiplier applied to a peer's probability score after a failed attempt. |
| `BOOST_AMOUNT` | `0.1` | The constant added to a peer's probability score after a successful delivery. |

## Data Dictionary
| Component | Type | Description |
| :--- | :--- | :--- |
| `DeliveryTable.table` | `dict {int: float}` | Maps peer ports to their current calculated delivery probability scores. |
| `message_queue` | `list [str]` | Stores pending text messages that are waiting for a valid forwarding window. |
| `q_lock` | `threading.Lock` | Ensures thread-safe access to the shared message queue and delivery table. |

## Repository Structure
The project is divided into `config.py` for parameters, `delivery_table.py` for scoring logic, and `node.py` for network operations.
This separation ensures that the routing algorithm is decoupled from the underlying socket communication.

## Run Instructions
1. **Initial Setup**: Open three or more separate terminal windows to simulate different network nodes on your local machine.
2. **Launch Nodes**: Execute the script using `python node.py [port] [peer_ports]`. 
   - Node A: `python node.py 9000 9001 9002`
   - Node B: `python node.py 9001 9000 9002`
   - Node C: `python node.py 9002 9000 9001`
3. **Send Messages**: Type any text in the terminal to queue a message for delivery. 
4. **Monitor State**: Use the command `table` to view current probability scores or `queue` to see messages waiting in the local buffer.

## Expected Behaviour
When a peer goes offline, its probability score will gradually decrease, causing the sender to store messages in a local queue.
Once the peer recovers and a successful connection is made, the score will increase and queued messages will be delivered.