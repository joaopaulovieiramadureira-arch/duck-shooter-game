# Duck Shooter Game - 5 Phases Adventure

## How to Play

### Controls
- **W/A/S/D** - Move the duck around
- **Mouse** - Aim at enemies
- **Left Click** - Shoot fire projectiles
- **ESC** - Quit game

### Objective
Defeat all 5 phases of enemies to win the game!

### Phases

**Phase 1 - Garden (Brown Ground)**
- 2 Insects that wander randomly
- 1 Flying enemy that follows when close

**Phase 2 - Grassland (Green Ground)**
- 2 Flying bombers that drop sound bombs
- 1 Roller (sphere) that rolls back and forth with shield

**Phase 3 - Stone Arena (Gray Ground)**
- 2 Rollers on opposite sides
- 1 Flying bomber that drops bombs from above

**Phase 4 - Dark Theater (Dark Stone)**
- 1 Flying bomber
- 1 Big Roller (2x size, 58% chance to bounce off walls)

**Phase 5 - Theater (Theater Theme)**
- Boss Duck - Intelligent enemy that shoots back!

### Difficulty Scaling
After defeating Phase 5 once, you enter **Loop 2**:
- All enemies have **2x health**
- All enemies deal **1.4x damage**
- Beat the boss again to win!

### Game Stats
- **Player Health**: 130 HP
- **Player Damage**: 5 per shot
- **Enemy Health**: 30 HP (Rollers: 20, Big Roller: 35, Boss: 130)
- **Movement**: WASD
- **Aiming**: Mouse
- **Shooting**: Left Click

### Tips
- Insects don't follow - just walk around randomly
- Flying enemies follow when you're within 200 pixels
- Rollers have a shield while rolling - damage when paused!
- Big Roller has 58% chance to bounce instead of stopping
- Flying bombers drop bombs every 4 seconds
- The boss is intelligent and shoots back every 0.5 seconds
- You can't heal until you beat the final boss

## Installation

```bash
pip install -r requirements.txt
python main.py
```

Enjoy! 🎮🦆
