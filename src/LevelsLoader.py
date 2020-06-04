import json
import re
from pathlib import Path

from src.model.core.Level import Level
from src.model.targets.Fleet import Fleet
from src.model.targets.specs.TargetSpecs import TargetSpecs
from src.model.targets.specs.TargetsGroupSpecs import TargetsGroupSpecs, EmptyTargetsGroupSpecs
from src.model.targets.specs.TargetsRowSpecs import TargetsRowSpecs, EmptyTargetsRowSpecs

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

KEY_EMPTY_ROW_SEALED_BALLS = "sealed_balls"

KEY_GROUP_TYPE = "group_type"

KEY_GROUP_TYPE_NORMAL = "normal"
KEY_GROUP_TYPE_EMPTY = "empty"

KEY_NORMAL_GROUP_SPACING = "spacing"
KEY_NORMAL_GROUP_SIZE = "size"
KEY_NORMAL_GROUP_TARGET_SPECS = "target_specs"

KEY_EMPTY_GROUP_SPACING = "spacing"
KEY_EMPTY_GROUP_SIZE = "size"
KEY_EMPTY_GROUP_TARGET_WIDTH = "target_width"
KEY_EMPTY_GROUP_SEALED_BALLS = "sealed_balls"

KEY_TARGET_WIDTH = "width"
KEY_TARGET_HEIGHT = "height"
KEY_TARGET_COLOR = "color"


def load_levels():
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
    p = Path(f"{LEVELS_PATH}\\{level.file_name}.json")
    level_root = json.load(p.open())
    return _parse_fleet(window, level_root[KEY_LEVEL_FLEET])


def _parse_fleet(window, fleet_root):
    spacing = fleet_root[KEY_FLEET_SPACING]
    horizontal_padding = fleet_root[KEY_FLEET_HORIZONTAL_PADDING]
    initially_visible_rows_count = fleet_root[KEY_FLEET_INITIALLY_VISIBLE_ROWS_COUNT]
    slide_down_time_gap = fleet_root[KEY_FLEET_SLIDE_DOWN_TIME_GAP]
    rows_specs = _parse_all_rows_specs(fleet_root[KEY_FLEET_ROWS])

    if initially_visible_rows_count == KEY_FLEET_INITIALLY_VISIBLE_ROWS_COUNT_ALL:
        initially_visible_rows_count = len(rows_specs)

    return Fleet.from_specs(
        window,
        spacing,
        horizontal_padding,
        initially_visible_rows_count,
        slide_down_time_gap,
        *rows_specs
    )


def _parse_all_rows_specs(rows_array):
    return [_parse_row_specs(row_root) for row_root in rows_array]


def _parse_row_specs(row_root):
    def parse_normal_row():
        spacing = row_root[KEY_NORMAL_ROW_SPACING]
        groups = _parse_all_groups_specs(row_root[KEY_NORMAL_ROW_GROUPS])
        return TargetsRowSpecs(
            spacing,
            *groups
        )

    def parse_empty_row():
        sealed_balls = row_root[KEY_EMPTY_ROW_SEALED_BALLS]
        return EmptyTargetsRowSpecs(sealed_balls)

    row_type = row_root[KEY_ROW_TYPE].lower()

    if row_type == KEY_ROW_TYPE_NORMAL:
        return parse_normal_row()
    elif row_type == KEY_ROW_TYPE_EMPTY:
        return parse_empty_row()


def _parse_all_groups_specs(groups_array):
    return [_parse_group_specs(group_root) for group_root in groups_array]


def _parse_group_specs(group_root):
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
        sealed_balls = group_root[KEY_EMPTY_GROUP_SEALED_BALLS]
        return EmptyTargetsGroupSpecs(
            spacing,
            size,
            target_width,
            sealed_balls
        )

    group_type = group_root[KEY_GROUP_TYPE].lower()

    if group_type == KEY_GROUP_TYPE_NORMAL:
        return parse_normal_group()
    elif group_type == KEY_GROUP_TYPE_EMPTY:
        return parse_empty_group()


def _parse_target_specs(target_root):
    width = target_root[KEY_TARGET_WIDTH]
    height = target_root[KEY_TARGET_HEIGHT]
    color = tuple(target_root[KEY_TARGET_COLOR])
    return TargetSpecs(
        width,
        height,
        color
    )
