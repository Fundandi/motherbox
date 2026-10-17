"""Colour + pill-shape per nutrient, kept from the original Motherbox design."""

_STYLES = {
    'folat':     {'dot': '#5A9E7A', 'bg': '#EDF7F2', 'shape': 'oval',    'p1': '#8ACBA8', 'p2': '#3D7A58'},
    'folsyre':   {'dot': '#5A9E7A', 'bg': '#EDF7F2', 'shape': 'oval',    'p1': '#8ACBA8', 'p2': '#3D7A58'},
    'b6':        {'dot': '#D4A847', 'bg': '#FDF8EC', 'shape': 'capsule', 'p1': '#F0D88C', 'p2': '#B88020'},
    'ingefær':   {'dot': '#A0785A', 'bg': '#F7F0EB', 'shape': 'capsule', 'p1': '#D4B896', 'p2': '#7A5030'},
    'd-vitamin': {'dot': '#E09840', 'bg': '#FEF6EC', 'shape': 'softgel', 'p1': '#F5CC70', 'p2': '#C07010'},
    'dha':       {'dot': '#5A88C8', 'bg': '#EBF3FC', 'shape': 'softgel', 'p1': '#C87840', 'p2': '#6A2808'},
    'omega':     {'dot': '#5A88C8', 'bg': '#EBF3FC', 'shape': 'softgel', 'p1': '#C87840', 'p2': '#6A2808'},
    'jod':       {'dot': '#6BAA7A', 'bg': '#EEF7F1', 'shape': 'oval',    'p1': '#C8E8D0', 'p2': '#488858'},
    'jern':      {'dot': '#C05A5A', 'bg': '#FDEEEE', 'shape': 'oval',    'p1': '#D88080', 'p2': '#882020'},
    'c-vitamin': {'dot': '#7AAE5A', 'bg': '#EFF7EA', 'shape': 'oval',    'p1': '#F0A050', 'p2': '#C05808'},
    'calcium':   {'dot': '#9090A0', 'bg': '#F4F4F6', 'shape': 'oval',    'p1': '#E8E8F0', 'p2': '#A0A0B0'},
    'magnesium': {'dot': '#6A7EC8', 'bg': '#EEF0FB', 'shape': 'oval',    'p1': '#C0C8F0', 'p2': '#3848A8'},
    'zink':      {'dot': '#4AABB0', 'bg': '#EBF7F8', 'shape': 'oval',    'p1': '#90D8DC', 'p2': '#207880'},
    'b12':       {'dot': '#C07898', 'bg': '#FAECF2', 'shape': 'capsule', 'p1': '#E8A0C0', 'p2': '#904060'},
    'k2':        {'dot': '#C87850', 'bg': '#FAF0EA', 'shape': 'softgel', 'p1': '#F0C080', 'p2': '#906020'},
    'selen':     {'dot': '#909850', 'bg': '#F5F6E8', 'shape': 'oval',    'p1': '#D8D888', 'p2': '#686830'},
    'probiotika':{'dot': '#B08AC0', 'bg': '#F5EEF8', 'shape': 'capsule', 'p1': '#D8C0E4', 'p2': '#7A5090'},
    'multi':     {'dot': '#C07859', 'bg': '#FAF5EE', 'shape': 'oval',    'p1': '#E0B090', 'p2': '#904030'},
}
_DEFAULT = {'dot': '#C07859', 'bg': '#FAF5EE', 'shape': 'oval', 'p1': '#E0B090', 'p2': '#904030'}


def nutrient_style(nutrient: str) -> dict:
    n = (nutrient or '').lower()
    for key, style in _STYLES.items():
        if key in n:
            return style
    return _DEFAULT
