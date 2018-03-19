# Guillotine Backend
## Serialization of GameStates
#### Requirements
1. Minimize space
2. Human readable
3. Compress archived games

- new lines not allowed in userIds
playerId(0)\nplayerId(1)\nplayerId(2)\nplayerId(3)\r\n
12,13,14\n

