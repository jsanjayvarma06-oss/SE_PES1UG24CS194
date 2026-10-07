
"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    """
    Return True if the falling object overlaps the basket.

    The object is treated as a circle using its x, y and radius.
    """

    # Falling object's horizontal bounds
    obj_left = obj.x - obj.radius
    obj_right = obj.x + obj.radius

    # Falling object's vertical bounds
    obj_top = obj.y - obj.radius
    obj_bottom = obj.y + obj.radius

    # Check horizontal overlap
    horizontal_overlap = (
        obj_right >= basket_rect.left
        and obj_left <= basket_rect.right
    )

    # Check vertical overlap
    vertical_overlap = (
        obj_bottom >= basket_rect.top
        and obj_top <= basket_rect.bottom
    )

    return horizontal_overlap and vertical_overlap
