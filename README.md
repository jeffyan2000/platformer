# platformer

#### Description
Keywords:
Sandbox, Online Multiplayer, Platformer, Adventure

#### Thread Structure
Client side: <br/>
Thread 1: fetch server udp packets, and update game instances <br/>
Thread 2: send tcp packet from tcp queue <br/>
Main Thread: render the game, get user inputs <br/>
<br/>
Server side: <br/>
Thread 1: listen to client tcp updates(usually user input commands) <br/>
Thread 2: update map <br/>
Main Thread: accept new connections <br/>

#### Installation

1.  python3，pygame1.9+

#### Running the Program

1. Start server_main.py first.
2. Then you can join the game by running client_main.py.

#### Collaboration

1. If you are interested in collaboration, please send email to 2000chrisyan@gmail.com
2. Or you can fork this repo, and leave a message on github

#### Current Features
- Sync server and client map
- Map generator
- Render map
- Player controls<br/>

#### In Progress
- Backpack
- Material collection and crafting

#### Planned
- Building construction
- Quest line
- Aggressive mobs
- Farming
- Chat
- SFX
- Reduce Packet size
- More map types
- Exploration
- Achievements
- Pets
- Weapon/Armor
- Abilities/Skills
