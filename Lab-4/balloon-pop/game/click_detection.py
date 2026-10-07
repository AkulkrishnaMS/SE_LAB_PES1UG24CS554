def check_pop(balloons, click_pos):
    """
    Returns the balloon that was clicked, or None if the click missed
    every balloon.
    """
    for balloon in balloons:
        dx = click_pos[0] - balloon.x
        dy = click_pos[1] - balloon.y
        # Calculate the actual linear distance by taking the square root
        distance = (dx * dx + dy * dy) ** 0.5
        
        if distance <= balloon.radius:
            return balloon
    return None