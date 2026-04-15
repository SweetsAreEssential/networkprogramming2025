# Week 10: Quantum-Inspired Networking (Conceptual)

## Overview
This lab simulates fundamental quantum principles within a network environment using Python. 
The system focuses on non-clonable messages that undergo state collapse upon reading or transmission.

## Key Concepts
| Concept | Description |
| :--- | :--- |
| **No-Cloning Theorem** | Enforces that a message cannot be copied; once sent, the original is consumed or destroyed. |
| **State Collapse** | The act of reading or forwarding a token permanently changes its state to "CONSUMED". |
| **Decoherence (TTL)** | Messages are ephemeral and will expire (state: EXPIRED) if not delivered within a time limit. |
| **One-Time Read** | A security concept where data exists in a valid state only until its first observation. |

## System Parameters (`config.py`)
| Parameter | Default | Description |
| :--- | :--- | :--- |
| `TOKEN_TTL` | `30` | Duration in seconds before a pending token becomes invalid (EXPIRED). |
| `UPDATE_INTERVAL` | `1` | Frequency in seconds for checking the queue to reduce communication latency. |
| `STRICT_NO_CLONE` | `True` | If enabled, any failed delivery attempt results in the immediate destruction of the token. |

## Data Dictionary
| Component | Type | Description |
| :--- | :--- | :--- |
| `token_queue` | `list [QuantumToken]` | Active buffer for tokens that are currently valid and awaiting transmission. |
| `token_vault` | `dict {str: Token}` | Historical registry of all tokens processed by the node for auditing and loop prevention. |
| `QuantumToken.state` | `Enum/String` | Tracks the lifecycle of a message: PENDING, CONSUMED, EXPIRED, or DESTROYED. |

## Run Instructions
1. Open three terminals and initialize the quantum nodes:
   - Node A: `python node.py 11000 11001 11002`
   - Node B: `python node.py 11001 11000 11002`
   - Node C: `python node.py 11002 11000 11001`
2. Enter a message to create a unique quantum token.
3. Use the `history` command to see the collapsed states of all tokens.

## Expected Behaviour
Due to the "No-Cloning" rule, once Node A successfully sends a token to Node B, the message is removed from Node A. 
If Node B reads the message, it collapses into a "CONSUMED" state and can never be forwarded to Node C.