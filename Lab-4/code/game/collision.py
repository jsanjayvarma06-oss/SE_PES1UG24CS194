"""
collision: figures out whether a falling object is within the basket.
"""


def is_caught(basket_rect, obj):
    obj_rect = obj.get_rect()

    # Object must horizontally overlap the basket
    horizontal_overlap = (
        obj_rect.right >= basket_rect.left
        and obj_rect.left <= basket_rect.right
    )

    # Object must have reached the basket vertically
    vertical_overlap = (
        obj_rect.bottom >= basket_rect.top
        and obj_rect.top <= basket_rect.bottom
    )

    return horizontal_overlap and vertical_overlap