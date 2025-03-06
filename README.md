# Flappy Bird Game

A Python implementation of the classic Flappy Bird game using Pygame.

## Description

This is a recreation of the popular Flappy Bird game where players control a bird and navigate it through pipes. The game features smooth animations, collision detection, and score tracking.

## Features

- Smooth bird animation with rotation
- Pipe obstacles with random heights
- Score tracking
- Game over screen
- Background graphics
- Collision detection with forgiving hitboxes

## Requirements

- Python 3.x
- Pygame 2.5.2

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```
   python main.py
   ```
2. Press SPACE to make the bird jump
3. Navigate through the pipes without hitting them
4. Try to achieve the highest score possible
5. When game is over, press SPACE to restart

## Controls

- SPACE: Make the bird jump/flap
- SPACE (on game over): Restart the game

## Game Mechanics

- The bird constantly falls due to gravity
- Pressing SPACE makes the bird jump
- Pipes appear at regular intervals
- Score increases when passing through pipes
- Game ends when the bird hits a pipe or the ground/ceiling

## Project Structure

- `main.py`: Main game file containing all game logic
- `requirements.txt`: List of Python dependencies
- `flapp-removebg-preview.png`: Bird sprite image
- `pipe-removebg-preview.png`: Pipe sprite image
- `images.png`: Background image

## Credits

This implementation is inspired by the original Flappy Bird game created by Dong Nguyen.
