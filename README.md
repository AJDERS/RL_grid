# RL_grid

Train an agent to navigate in a grid with traps and walls, with no prior knowledge of the grid layout. The grid size i variable. The agent is trained using TD-learning,
with the Monte Carlo method. The model is positively rewarded when it enter the finishing state, negatively when it enters a
state with a trap, or if it navigates to a previously visited state.

## Example Simulation

![](new_plot.gif)

### TODO

- Variable learning rate.
- Variable exploration rate.
- Indicate from which game, it wins.
