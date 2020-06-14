import json
import re
from pathlib import Path

from src.model.levels.runtime.Fleet import Fleet
from src.model.levels.runtime.Level import Level
from src.model.levels.specs.TargetSpecs import TargetSpecs
from src.model.levels.specs.TargetsGroupSpecs import TargetsGroupSpecs, EmptyTargetsGroupSpecs
from src.model.levels.specs.TargetsRowSpecs import TargetsRowSpecs, EmptyTargetsRowSpecs

LEVELS_PATH = "..\\levels"

KEY_LEVEL_FLEET = "fleet"

KEY_FLEET_SPACING = "spacing"
KEY_FLEET_HORIZONTAL_PADDING = "horizontal_padding"
KEY_FLEET_INITIALLY_VISIBLE_ROWS_COUNT = "initially_visible_rows_count"
KEY_FLEET_SLIDE_DOWN_TIME_GAP = "slide_down_time_gap"
KEY_FLEET_ROWS = "rows"

KEY_FLEET_INITIALLY_VISIBLE_ROWS_COUNT_ALL = "all"

KEY_ROW_TYPE = "row_type"

KEY_ROW_TYPE_NORMAL = "normal"
KEY_ROW_TYPE_EMPTY = "empty"

KEY_NORMAL_ROW_SPACING = "spacing"
KEY_NORMAL_ROW_GROUPS = "groups"

KEY_GROUP_TYPE = "group_type"

KEY_GROUP_TYPE_NORMAL = "normal"
KEY_GROUP_TYPE_EMPTY = "empty"

KEY_NORMAL_GROUP_SPACING = "spacing"
KEY_NORMAL_GROUP_SIZE = "size"
KEY_NORMAL_GROUP_TARGET_SPECS = "target_specs"

KEY_EMPTY_GROUP_SPACING = "spacing"
KEY_EMPTY_GROUP_SIZE = "size"
KEY_EMPTY_GROUP_TARGET_WIDTH = "target_width"

KEY_TARGET_WIDTH = "width"
KEY_TARGET_HEIGHT = "height"
KEY_TARGET_COLOR = "color"


def load_levels():
    """
    Loads all the levels

    Levels matching this regex '^[0-9]+-.+$', ie '2-Arrested' are added in
     the order specified in their name, for `2-Arrested' it's 2 (index 1).

    If multiple levels with the same orders are present, the are added following each
     other and all the levels with higher order are added after them.

    Levels with no order in their name are added to the end of the list
    :return: A list containing all the levels objects
    """
    levels_files = [p for p in Path(LEVELS_PATH).iterdir() if p.is_file() and p.suffix.lower() == ".json"]

    ordered_levels = []
    unordered_levels = []

    for path in levels_files:
        if re.search("^[0-9]+-.+$", path.stem) is not None:
            ordered_levels.append(path.stem.split(sep="-", maxsplit=1))
        else:
            unordered_levels.append(path.stem)

    ordered_levels.sort(key=lambda lev: int(lev[0]))
    ordered_levels = [Level(lev[1], f"{lev[0]}-{lev[1]}", index) for index, lev in enumerate(ordered_levels)]

    unordered_levels = [Level(stem, stem, index) for index, stem in enumerate(unordered_levels)]

    return ordered_levels + unordered_levels


def parse_level(window, level):
    """
    Parses a level and returns its fleet
    :param window: the window the level is going to be rendered in
    :param level: the level to parse
    :return: The fleet of this level
    """
    p = Path(f"{LEVELS_PATH}\\{level.file_name}.json")
    level_root = json.load(p.open())
    return _parse_fleet(window, level_root[KEY_LEVEL_FLEET])


def _parse_fleet(window, fleet_root):
    """
    Parses a fleet
    :param window: the window the fleet is going to be rendered in
    :param fleet_root: the root of the fleet in the json tree
    :return: The fleet
    """
    spacing = fleet_root[KEY_FLEET_SPACING]
    horizontal_padding = fleet_root[KEY_FLEET_HORIZONTAL_PADDING]
    initially_visible_rows_count = fleet_root[KEY_FLEET_INITIALLY_VISIBLE_ROWS_COUNT]
    rows_specs = _parse_all_rows_specs(fleet_root[KEY_FLEET_ROWS])

    if initially_visible_rows_count == KEY_FLEET_INITIALLY_VISIBLE_ROWS_COUNT_ALL:
        initially_visible_rows_count = len(rows_specs)
        slide_down_time_gap = 100
    else:
        slide_down_time_gap = fleet_root[KEY_FLEET_SLIDE_DOWN_TIME_GAP]

    return Fleet.from_specs(
        window,
        spacing,
        horizontal_padding,
        initially_visible_rows_count,
        slide_down_time_gap,
        *rows_specs
    )


def _parse_all_rows_specs(rows_array):
    """
    Parses all the rows in a fleet
    :param rows_array: the array containing all the rows in the json tree
    :return: A list containing all the rows specs
    """
    return [_parse_row_specs(row_root) for row_root in rows_array]


def _parse_row_specs(row_root):
    """
    Parses a row
    :param row_root: the root of the row in the json tree
    :return: The row specs
    """

    def parse_normal_row():
        spacing = row_root[KEY_NORMAL_ROW_SPACING]
        groups = _parse_all_groups_specs(row_root[KEY_NORMAL_ROW_GROUPS])
        return TargetsRowSpecs(
            spacing,
            *groups
        )

    def parse_empty_row():
        return EmptyTargetsRowSpecs()

    row_type = row_root[KEY_ROW_TYPE].lower()

    if row_type == KEY_ROW_TYPE_NORMAL:
        return parse_normal_row()
    elif row_type == KEY_ROW_TYPE_EMPTY:
        return parse_empty_row()


def _parse_all_groups_specs(groups_array):
    """
    Parses all the groups in a row
    :param groups_array: the array containing all the groups in the json tree
    :return: A list containing all the groups specs
    """
    return [_parse_group_specs(group_root) for group_root in groups_array]


def _parse_group_specs(group_root):
    """
    Parses a group
    :param group_root: the root of the group in the json tree
    :return: The group specs
    """

    def parse_normal_group():
        spacing = group_root[KEY_NORMAL_GROUP_SPACING]
        size = group_root[KEY_NORMAL_GROUP_SIZE]
        target_specs = _parse_target_specs(group_root[KEY_NORMAL_GROUP_TARGET_SPECS])
        return TargetsGroupSpecs(
            target_specs,
            spacing,
            size
        )

    def parse_empty_group():
        spacing = group_root[KEY_EMPTY_GROUP_SPACING]
        size = group_root[KEY_EMPTY_GROUP_SIZE]
        target_width = group_root[KEY_EMPTY_GROUP_TARGET_WIDTH]
        return EmptyTargetsGroupSpecs(
            spacing,
            size,
            target_width
        )

    group_type = group_root[KEY_GROUP_TYPE].lower()

    if group_type == KEY_GROUP_TYPE_NORMAL:
        return parse_normal_group()
    elif group_type == KEY_GROUP_TYPE_EMPTY:
        return parse_empty_group()


def _parse_target_specs(target_root):
    """
    Parses the targets specs of a group
    :param target_root: the root of the target specs in the json tree
    :return: The target specs
    """
    width = target_root[KEY_TARGET_WIDTH]
    height = target_root[KEY_TARGET_HEIGHT]
    color = tuple(element / 255 for element in target_root[KEY_TARGET_COLOR])
    return TargetSpecs(
        width,
        height,
        color
    )
