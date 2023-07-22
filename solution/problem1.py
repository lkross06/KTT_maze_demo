from logic import Logic

logic = Logic()
logic.load_maze1()

'''
=== HELPFUL FUNCTIONS ===

logic.turn_left()       Turns the player 90 degrees left.
logic.turn_right()      Turns the player 90 degrees right.
logic.move_forward()    Moves the player forward 1 space in their current direction.
logic.wall_in_front()   Returns [True] if the player is facing a wall, [False] otherwise.

=========================
'''
#TODO: mainloop sucks
#Use this space to solve maze 1 :)
logic.move_forward()
logic.turn_left()
logic.move_forward()
logic.move_forward()
logic.turn_right()
logic.move_forward()
logic.move_forward()
logic.turn_left()
logic.move_forward()
logic.move_forward()
logic.turn_left()
logic.move_forward()
logic.turn_right()
logic.move_forward()
logic.turn_left()
logic.move_forward()
logic.move_forward()
logic.move_forward()