#!python3.9

#  Trick Surf Data Dump
#
#  Copyright (C) 2024  anominy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from typing import Final, Optional, Union, Any, TextIO
from types import MappingProxyType
from argparse import ArgumentParser, Namespace as ArgumentNamespace
from subprocess import Popen
from re import RegexFlag
from datetime import datetime

import sys
import requests
import re
import os
import json
import shutil
import string
import ciso8601
import time


_TIME_ZONE_OFFSET: Final[int] = time.timezone

_STD_OUT_STREAM: Final[TextIO] = sys.stdout
_STD_ERR_STREAM: Final[TextIO] = sys.stderr

_OPEN_FILE_WRITE_FLAG: Final[str] = 'w'
_OPEN_FILE_READ_FLAG: Final[str] = 'r'

_REGEX_MULTILINE_FLAG: Final[RegexFlag] = re.MULTILINE

_CURRENT_PATH: Final[str] = os.path.dirname(__file__)
_PARENT_PATH: Final[str] = os.path.join(_CURRENT_PATH, '..')
_LICENSE_PATH: Final[str] = os.path.join(_PARENT_PATH, 'COPYING')


_TAG_SEPARATOR: Final[str] = ' :: '

_STEP_DUMP_TRICK_GXDS_NAME: Final[str] = 'TrickGxds'
_STEP_DUMP_TRICK_SURF_NAME: Final[str] = 'TrickSurf'

_SUCCESS_MESSAGE_PREFIX: Final[str] = 'SUCCESS'

_SUCCESS_MESSAGE_DUMP_DATA: Final[str] = 'Created & wrote data dumps to JSON files'
_SUCCESS_MESSAGE_DUMP_DATA_FMT: Final[str] = f'{_SUCCESS_MESSAGE_PREFIX}{_TAG_SEPARATOR}%s{_TAG_SEPARATOR}{_SUCCESS_MESSAGE_DUMP_DATA}'

_SUCCESS_MESSAGE_DUMP_TRICK_GXDS_DATA: Final[str] = _SUCCESS_MESSAGE_DUMP_DATA_FMT % _STEP_DUMP_TRICK_GXDS_NAME
_SUCCESS_MESSAGE_DUMP_TRICK_SURF_DATA: Final[str] = _SUCCESS_MESSAGE_DUMP_DATA_FMT % _STEP_DUMP_TRICK_SURF_NAME

_FAILURE_MESSAGE_PREFIX: Final[str] = '-- FAILURE'

_FAILURE_MESSAGE_DUMP_DATA: Final[str] = 'Couldn\'t create & write data dumps to JSON files'
_FAILURE_MESSAGE_DUMP_DATA_FMT: Final[str] = f'{_FAILURE_MESSAGE_PREFIX}{_TAG_SEPARATOR}%s{_TAG_SEPARATOR}{_FAILURE_MESSAGE_DUMP_DATA}'

_FAILURE_MESSAGE_DUMP_TRICK_GXDS_DATA: Final[str] = _FAILURE_MESSAGE_DUMP_DATA_FMT % _STEP_DUMP_TRICK_GXDS_NAME
_FAILURE_MESSAGE_DUMP_TRICK_SURF_DATA: Final[str] = _FAILURE_MESSAGE_DUMP_DATA_FMT % _STEP_DUMP_TRICK_SURF_NAME


_DUMP_UNIFIED_DIRECTORY_NAME: Final[str] = 'unified'
_DUMP_TRICK_GXDS_DIRECTORY_NAME: Final[str] = 'trick-gxds'
_DUMP_TRICK_SURF_DIRECTORY_NAME: Final[str] = 'trick-surf'

_DUMP_UNIFIED_PATH: Final[str] = os.path.join(_PARENT_PATH, _DUMP_UNIFIED_DIRECTORY_NAME)
_DUMP_TRICK_GXDS_PATH: Final[str] = os.path.join(_PARENT_PATH, _DUMP_TRICK_GXDS_DIRECTORY_NAME)
_DUMP_TRICK_SURF_PATH: Final[str] = os.path.join(_PARENT_PATH, _DUMP_TRICK_SURF_DIRECTORY_NAME)

_DUMP_UNIFIED_NAME: Final[str] = 'ski2-gxds-tricks'
_DUMP_UNIFIED_ORIGINAL_NAME: Final[str] = f'{_DUMP_UNIFIED_NAME}~original'
_DUMP_UNIFIED_SIFTED_NAME: Final[str] = f'{_DUMP_UNIFIED_NAME}~sifted'

_DUMP_JSON_FILE_EXT: Final[str] = '.json'
_DUMP_JSON_FILE_MIN_EXT: Final[str] = f'.min{_DUMP_JSON_FILE_EXT}'
_DUMP_JSON_FILE_ENCODING: Final[str] = 'utf-8'


_TRICK_GXDS_PLAYER_TABLE_NAME: Final[str] = 'players'
_TRICK_GXDS_ROUTE_TABLE_NAME: Final[str] = 'routes'
_TRICK_GXDS_TRICK_TABLE_NAME: Final[str] = 'tricks'
_TRICK_GXDS_TRIGGER_TABLE_NAME: Final[str] = 'triggers'

_TRICK_GXDS_TABLE_FILE_EXT: Final[str] = '.sql'

_TRICK_GXDS_PLAYER_TABLE_FILE_NAME: Final[str] = _TRICK_GXDS_PLAYER_TABLE_NAME + _TRICK_GXDS_TABLE_FILE_EXT
_TRICK_GXDS_ROUTE_TABLE_FILE_NAME: Final[str] = _TRICK_GXDS_ROUTE_TABLE_NAME + _TRICK_GXDS_TABLE_FILE_EXT
_TRICK_GXDS_TRICK_TABLE_FILE_NAME: Final[str] = _TRICK_GXDS_TRICK_TABLE_NAME + _TRICK_GXDS_TABLE_FILE_EXT
_TRICK_GXDS_TRIGGER_TABLE_FILE_NAME: Final[str] = _TRICK_GXDS_TRIGGER_TABLE_NAME + _TRICK_GXDS_TABLE_FILE_EXT

_TRICK_GXDS_TABLE_BASE_URL: Final[str] = f'https://raw.githubusercontent.com/anominy/trick-surf-data-dump/main/{_DUMP_TRICK_GXDS_DIRECTORY_NAME}/'

_TRICK_GXDS_PLAYER_TABLE_URL: Final[str] = _TRICK_GXDS_TABLE_BASE_URL + _TRICK_GXDS_PLAYER_TABLE_FILE_NAME
_TRICK_GXDS_ROUTE_TABLE_URL: Final[str] = _TRICK_GXDS_TABLE_BASE_URL + _TRICK_GXDS_ROUTE_TABLE_FILE_NAME
_TRICK_GXDS_TRICK_TABLE_URL: Final[str] = _TRICK_GXDS_TABLE_BASE_URL + _TRICK_GXDS_TRICK_TABLE_FILE_NAME
_TRICK_GXDS_TRIGGER_TABLE_URL: Final[str] = _TRICK_GXDS_TABLE_BASE_URL + _TRICK_GXDS_TRIGGER_TABLE_FILE_NAME

# language=PythonRegExp
_TRICK_GXDS_PLAYER_TABLE_ROW_REGEX: Final[str] = r'^.*\((?P<id>\d+),\s?\'(?P<steam_id2>STEAM_[0-5]:[0-1]:\d+)\',\s?\'?(?P<steam_id64>\d{17})\'?,\s?\'(?P<name>.*?)\',\s?(?:\'https://steamcommunity\.com/id/(?P<steam_vanity_url>[a-zA-Z0-9_-]{2,32})/?\'|NULL),\s?(?:\'(?P<avatar_url>.*?)\'|NULL),\s?(?:\'(?P<avatar_custom_url>.*?)\'|NULL),\s?(?:\'(?P<dashboard_url>.*?)\'|NULL),\s?(?:\'(?P<join_date>.*?)\'|NULL),\s?(?:\'(?P<last_site_login_date>.*?)\'|NULL),\s?(?:\'(?P<last_server_login_date>.*?)\'|NULL),\s?(?:\'(?P<role>.*?)\'|NULL)\),?.*$'

# language=PythonRegExp
_TRICK_GXDS_ROUTE_TABLE_ROW_REGEX: Final[str] = r'^.*\((?P<id>\d+),\s?(?P<trick_id>\d+),\s?(?P<trigger_id>\d+)\),?.*$'

# language=PythonRegExp
_TRICK_GXDS_TRICK_TABLE_ROW_REGEX: Final[str] = r'^.*\((?P<id>\d+),\s?\'(?P<name>.*?)\',\s?(?P<points>\d+),\s?(?P<velocity>\d+),\s?(?:\'(?P<create_date>.*?)\'|NULL),\s?(?P<author_id>\d+),\s?1\),?.*$'

# language=PythonRegExp
_TRICK_GXDS_TRIGGER_TABLE_ROW_REGEX: Final[str] = r'^.*\((?P<id>\d+),\s?\'(?P<name>.*?)\',\s?(?:\'(?P<alt_name>.*?)\'|NULL),\s?(?:(?P<x>-?\d+|-?\d+\.\d+)|NULL),\s?(?:(?P<y>-?\d+|-?\d+\.\d+)|NULL),\s?(?:(?P<z>-?\d+|-?\d+\.\d+)|NULL),\s?1,\s?(?:\'(?P<image_url>.*?)\'|NULL)\),?.*$'

_TRICK_GXDS_PLAYER_TABLE_ID_COLUMN_INDEX: Final[int] = 0
_TRICK_GXDS_PLAYER_TABLE_STEAM_ID2_COLUMN_INDEX: Final[int] = 1
_TRICK_GXDS_PLAYER_TABLE_STEAM_ID64_COLUMN_INDEX: Final[int] = 2
_TRICK_GXDS_PLAYER_TABLE_NAME_COLUMN_INDEX: Final[int] = 3
_TRICK_GXDS_PLAYER_TABLE_STEAM_VANITY_URL_COLUMN_INDEX: Final[int] = 4
_TRICK_GXDS_PLAYER_TABLE_AVATAR_URL_COLUMN_INDEX: Final[int] = 5
_TRICK_GXDS_PLAYER_TABLE_AVATAR_CUSTOM_URL_COLUMN_INDEX: Final[int] = 6
_TRICK_GXDS_PLAYER_TABLE_DASHBOARD_URL_COLUMN_INDEX: Final[int] = 7
_TRICK_GXDS_PLAYER_TABLE_JOIN_DATE_COLUMN_INDEX: Final[int] = 8
_TRICK_GXDS_PLAYER_TABLE_LAST_SITE_LOGIN_COLUMN_INDEX: Final[int] = 9
_TRICK_GXDS_PLAYER_TABLE_LAST_SERVER_LOGIN_COLUMN_INDEX: Final[int] = 10
_TRICK_GXDS_PLAYER_TABLE_ROLE_COLUMN_INDEX: Final[int] = 11

_TRICK_GXDS_ROUTE_TABLE_ID_COLUMN_INDEX: Final[int] = 0
_TRICK_GXDS_ROUTE_TABLE_TRICK_ID_COLUMN_INDEX: Final[int] = 1
_TRICK_GXDS_ROUTE_TABLE_TRIGGER_ID_COLUMN_INDEX: Final[int] = 2

_TRICK_GXDS_TRICK_TABLE_ID_COLUMN_INDEX: Final[int] = 0
_TRICK_GXDS_TRICK_TABLE_NAME_COLUMN_INDEX: Final[int] = 1
_TRICK_GXDS_TRICK_TABLE_POINTS_COLUMN_INDEX: Final[int] = 2
_TRICK_GXDS_TRICK_TABLE_VELOCITY_COLUMN_INDEX: Final[int] = 3
_TRICK_GXDS_TRICK_TABLE_CREATE_DATE_COLUMN_INDEX: Final[int] = 4
_TRICK_GXDS_TRICK_TABLE_AUTHOR_ID_COLUMN_INDEX: Final[int] = 5

_TRICK_GXDS_TRIGGER_TABLE_ID_COLUMN_INDEX: Final[int] = 0
_TRICK_GXDS_TRIGGER_TABLE_NAME_COLUMN_INDEX: Final[int] = 1
_TRICK_GXDS_TRIGGER_TABLE_ALT_NAME_COLUMN_INDEX: Final[int] = 2
_TRICK_GXDS_TRIGGER_TABLE_X_COLUMN_INDEX: Final[int] = 3
_TRICK_GXDS_TRIGGER_TABLE_Y_COLUMN_INDEX: Final[int] = 4
_TRICK_GXDS_TRIGGER_TABLE_Z_COLUMN_INDEX: Final[int] = 5
_TRICK_GXDS_TRIGGER_TABLE_IMAGE_URL_COLUMN_INDEX: Final[int] = 6

_TRICK_GXDS_TRIGGER_NAMES: Final[dict[str, Optional[str]]] = MappingProxyType({
    't_spawn': 'T-Spawn (G: 0)',  # @CONFIRMED
    'main_ramp': 'Main Ramp (G: 0)',  # @CONFIRMED
    'tower_top': 'Tower Top (G: 0)',  # @CONFIRMED
    'banana_ramp': 'Banana Ramp (G: 0)',  # @CONFIRMED
    'banana_hole': 'Banana Hole (G: 1)',  # @CONFIRMED
    'tower_platform': 'Tower Platform (G: 0)',  # @CONFIRMED
    'jail_wall_02': 'Jail Wall (G: 0)',  # @CONFIRMED
    'jail_floor_02': 'Jail Floor (G: 0)',  # @CONFIRMED
    'long_ramp': 'Long Ramp (G: 0)',  # @CONFIRMED
    't2_tower_platform': 'T2 Tower Platform (G: 0)',  # @CONFIRMED
    't2_right_hole': 'T2 Right Hole (G: 1)',  # @CONFIRMED
    't2_left_wing': 'T2 Left Wing (G: 0)',  # @CONFIRMED
    't2_right_wing': 'T2 Right Wing (G: 0)',  # @CONFIRMED
    'spawn_roof_water': 'Spawn Roof Water (G: 0)',  # @CONFIRMED
    'ski_sign': 'Ski Sign (G: 0)',  # @CONFIRMED
    'left_wedge': 'Left Wing (G: 0)',  # @CONFIRMED
    'middle_wing': 'Middle Wing (G: 0)',  # @CONFIRMED
    'main_blunt_ramp': 'Center Wedge (G: 0)',  # @CONFIRMED
    'healbot_platform': 'Healbot Platform (G: 0)',  # @CONFIRMED
    'section_ramp': 'Section Ramp (G: 0)',  # @CONFIRMED
    'section_slant': 'Section Slant (G: 0)',  # @CONFIRMED
    'mini_ramp_spine': 'Mini Ramp Tip (G: 0)',  # @CONFIRMED
    'mini_ramp02': 'Mini Ramp (G: 0)',  # @CONFIRMED
    'sriracha': 'Sriracha (G: 0)',  # @CONFIRMED
    'tower_base_water': 'Tower Run-up Water (G: 0)',  # @CONFIRMED
    'triomino_2': 'Triomino 2 (G: 0)',   # @CONFIRMED
    'mario_room_teleport': 'Mario Room Teleporter (G: 0)',  # @CONFIRMED
    't_spawn_hole_front': 'T-Spawn Hole Front (G: 1)',  # @CONFIRMED
    'gun_room': 'Gun Room (G: 0)',  # @CONFIRMED
    'center_wedge_platform': 'Center Wedge Platform (G: 0)',  # @CONFIRMED
    'main_wings': 'Center Wings (G: 0)',  # @CONFIRMED
    'main_drag': 'Center Ramp (G: 0)',  # @CONFIRMED
    't2_center_platform': 'T2 Center Platform (G: 0)',  # @CONFIRMED
    'through_t2_tower': 'Through T2 Tower (G: 0)',  # @CONFIRMED
    'fish_ramp': 'Fish Hook Ramp (G: 0)',  # @CONFIRMED
    'awp_platform': 'Awp Platform (G: 0)',  # @CONFIRMED
    'healbot_sign': 'Healbot Sign (G: 0)',  # @CONFIRMED
    'awp_ramp': 'Awp Ramp (G: 0)',  # @CONFIRMED
    # 'tower_water': None,  # @UNUSED
    'behind_main_ramp_trigger': 'Behind Main Ramp (G: 1)',  # @CONFIRMED
    'fish_hook_wedge': 'Fish Hook Wedge (G: 0)',  # @CONFIRMED
    'elevator_mid_entrance': 'Elevator Hole (G: 1)',  # @CONFIRMED
    'behind_long_ramp': 'Behind Long Ramp (G: 1)',  # @CONFIRMED
    't_spawn_water': 'T-Spawn Water (G: 0)',  # @CONFIRMED
    'behind_t2_tower_wedge': 'Rear T2 Tower Wedge (G: 0)',  # @CONFIRMED
    'through_t2_back_left': 'Through T2 Back Left (G: 0)',  # @CONFIRMED
    'through_t2_back_right': 'Through T2 Back Right (G: 0)',  # @CONFIRMED
    'through_t2_front_right': 'Through T2 Front Right (G: 1)',  # @CONFIRMED
    'rear_spawn_ramp': 'Rear Spawn Ramp (G: 0)',  # @CONFIRMED
    'gun_room_ramp': 'Gun Room Ramp (G: 0)',   # @CONFIRMED
    'ct_spawn_teleporter': 'CT-Spawn Teleporter (G: 0)',  # @CONFIRMED
    'tower_sign': 'Tower Sign (G: 0)',  # @CONFIRMED
    't_spawn_hole_back': 'T-Spawn Hole Back (G: 1)',  # @CONFIRMED
    'healbot_ramp': 'Healbot Ramp (G: 0)',  # @CONFIRMED
    'ct_spawn': 'CT-Spawn (G: 0)',  # @CONFIRMED
    'side_spawn_ladder': 'Side Spawn Ladder (G: 0)',  # @CONFIRMED
    'elevator': 'Elevator (G: 1)',  # @CONFIRMED
    'elevator_exit': 'Elevator Exit (G: 0)',  # @CONFIRMED
    'tower_box1': 'Tower Box 1 (G: 0)',  # @CONFIRMED
    'banana_platform': 'Banana Slant (G: 0)',  # @CONFIRMED
    'triomino2': 'Triomino 2 (G: 0)',  # @CONFIRMED
    't1_ladder': 'T1 Ladder (G: 0)',  # @CONFIRMED
    'triomino1': 'Triomino 1 (G: 0)',  # @CONFIRMED
    'triomino3': 'Triomino 3 (G: 0)',  # @CONFIRMED
    # 'sw': None,  # @UNUSED
    't1_right_platform': 'T1 Right Platform (G: 0)',  # @CONFIRMED
    'bonus_platform': 'Bonus Platform (G: 0)',  # @CONFIRMED
    'letter_t1': 'Letter T1 Top (G: 0)',  # @CONFIRMED
    't_spawn_slant': 'T-Spawn Slant (G: 0)',  # @CONFIRMED
    'ct_scout_pad': 'CT Scout Pad (G: 0)',  # @CONFIRMED
    'jail_box_1': 'Jail Box 1 (G: 0)',  # @CONFIRMED
    'right_wedge': 'Right Wing (G: 0)',  # @CONFIRMED
    'behind_spawn': 'Behind Spawn (G: 1)',  # @CONFIRMED
    'jail_booster_tip': 'Jail Booster Tip (G: 0)',  # @CONFIRMED
    # 'telepad_water': None,  # @UNUSED
    'long_ramp_slant': 'Long Ramp Slant (G: 0)',  # @CONFIRMED
    'kevin_ramp': 'Kevin Ramp (G: 0)',  # @CONFIRMED
    'keith_ramp': 'Keith Ramp (G: 0)',  # @CONFIRMED
    'diddy_platform': 'Diddy Ramp Platform (G: 0)',  # @CONFIRMED
    'behind_mario_tower': 'Behind Tower (G: 0)',  # @CONFIRMED
    'elevator_entrance': 'Elevator Entrance (G: 0)',  # @CONFIRMED
    'ct_spawn_hole_front': 'CT-Spawn Hole Front (G: 1)',  # @CONFIRMED
    'ct_spawn_hole_back': 'CT-Spawn Hole Back (G: 1)',  # @CONFIRMED
    't1_right_rail': 'T1 Right Rail (G: 0)',  # @CONFIRMED
    'spawn_roof_platform': 'Spawn Roof Platform (G: 0)',  # @CONFIRMED
    'hamburger': 'Humburger (G: 0)',  # @CONFIRMED
    'telepad': 'Telepad Water (G: 0)',  # @CONFIRMED
    'jail_ledge02': 'Jail Ledge (G: 0)',  # @CONFIRMED
    'under_awp': 'Under Awp Ramp (G: 1)',  # @CONFIRMED
    't2_big_water': 'T2 Big Water (G: 0)',  # @CONFIRMED
    'ct_spawn_slant': 'CT-Spawn Slant (G: 0)',  # @CONFIRMED
    'kevin_ramp_tip': 'Kevin Ramp Tip (G: 0)',  # @CONFIRMED
    't2_left_box_2': 'T2 Top Left Block (G: 0)',  # @CONFIRMED
    'jail_box_3': 'Jail Box 3 (G: 0)',  # @CONFIRMED
    'north_east_booster_platform': 'North East Booster Platform (G: 0)',  # @CONFIRMED
    'north_east_booster': 'North East Booster (G: 0)',  # @CONFIRMED
    'ramp_horn': 'Bonus Ramp (G: 0)',  # @CONFIRMED
    'bonus_cube': 'Bonus Cube (G: 0)',  # @CONFIRMED
    'bonus_rear_slant': 'Bonus Rear Slant (G: 0)',  # @CONFIRMED
    't2_tower_water02': 'T2 Tower Water (G: 0)',  # @CONFIRMED
    'reset': 'Healbot Leader (G: 0)',  # @CONFIRMED
    'behind_t2_tower_wedge_t': 'Rear T2 Tower Wedge Tip (G: 0)',  # @CONFIRMED
    't2_left_hole': 'T2 Left Hole (G: 1)',  # @CONFIRMED
    'section_ramp_tip': 'Section Ramp Tip (G: 0)',  # @CONFIRMED
    'left_wedge_tip': 'Left Wing Tip (G: 0)',  # @CONFIRMED
    'side_spawn_lower_platform': 'Side Spawn Lower Platform (G: 0)',  # @CONFIRMED
    't1_water': 'T1 Water (G: 0)',  # @CONFIRMED
    'under_blunt': 'Under Center Ramps (G: 1)',  # @CONFIRMED
    'tower_run_up_w': 'Tower Base Water (G: 0)',  # @CONFIRMED
    'gun_room_sign': 'Gun Room Sign (G: 0)',  # @CONFIRMED
    # 'jail_floor_03': None,  # @UNUSED
    'under_rear': 'Under Rear Spawn Ramp (G: 1)',  # @CONFIRMED
    # 'jail_teleporter': None,  # @UNUSED
    'jail_side_rail': 'Jail Side Rail (G: 0)',  # @CONFIRMED
    'starlight': 'Starlight North (G: 0)',  # @CONFIRMED
    't2_right_box_2': 'T2 Top Right Block (G: 0)',  # @CONFIRMED
    'under_t2_right_wing': 'Under T2 Right Wing (G: 1)',  # @CONFIRMED
    't_spawn_teleporter': 'T-Spawn Teleporter (G: 0)',  # @CONFIRMED
    'spawn_divide': 'Spawn Divide (G: 0)',  # @CONFIRMED
    'ground_teleporter': 'Ground Teleporter (G: 0)',
    'spawn_roof_booster': 'Spawn Roof Booster (G: 0)',
    'through_t2_front_left': 'Through T2 Front Left (G: 1)',  # @CONFIRMED
    'side_spawn_platform': 'Side Spawn Upper Platform (G: 0)',  # @CONFIRMED
    't1_left_platform': 'T1 Left Platform (G: 0)',  # @CONFIRMED
    't1_left_rail': 'T1 Left Rail (G: 0)',  # @CONFIRMED
    # 'spawn_roof_ramp': None,  # @UNUSED
    'healbot_ramp_tip': 'Healbot Ramp Tip (G: 0)',  # @CONFIRMED
    'idk': 'Diddy Rampz (G: 0)',  # @CONFIRMED
    't2_left_window': 'T2 Left Window (G: 1)',  # @CONFIRMED
    'north_east_ramp': 'North East Booster (G: 0)',  # @CONFIRMED
    'under_lower_boost': 'Rear Spawn Mini Hole (G: 1)',  # @CONFIRMED
    'telepad_derevo': 'Telepad Tower (G: 0)',  # @CONFIRMED
    't1_bashnya': 'Totem (G: 0)',  # @CONFIRMED
    'nlo_platform': 'UFO Roof (G: 0)',  # @CONFIRMED
    't2_right_window': 'T2 Right Window (G: 1)',  # @CONFIRMED
    't2_big_water_outskirts': 'T2 Big Water Outskirts (G: 0)',  # @CONFIRMED
    't2_ladder': 'Healbot Ladder (G: 0)',  # @CONFIRMED
    'lower_platform_push': 'Side Spawn Booster (G: 0)',  # @CONFIRMED
    'hamburger_slant': 'Hamburger Slant (G: 0)',  # @CONFIRMED
    'halisha_throne_upper': 'Trickgxds Title (G: 0)',  # @CONFIRMED
    'halisha_throne_lower': 'Trickgxds Throne (G: 0)',  # @CONFIRMED
    # 'telepad_box_3': None,  # @NOTPRESENT
    'under_t2_left_wing': 'Under T2 Left Wing (G: 1)',  # @CONFIRMED
    'fish_booster': 'Low Fish Booster (G: 0)',  # @CONFIRMED
    'fish_platform': 'Fish Platform (G: 0)',  # @CONFIRMED
    'fish_ramp_wedge': 'Fish Hook Wedge (G: 0)',  # @CONFIRMED
    'j_teleporter': 'Jail Teleporter (G: 0)',  # @CONFIRMED
    'main_drag_tip': 'Center Ramp Tip (G: 0)',  # @CONFIRMED
    'middle_awp_platform': 'Middle Awp Ground (G: 0)',  # @CONFIRMED
    # 'middle_wing_tip': None,  # @UNUSED
    # 'player_boost': None,  # @UNUSED
    # 'push_spawn_roof_ramp': None,  # @UNUSED
    'spawn_divide_top': 'Spawn Divide Top (G: 0)',  # @CONFIRMED
    't1_middle_ramp_lower': 'T1 Middle Lower Ramp (G: 0)',  # @CONFIRMED
    't2_big_hole_left': 'T2 Big Left Hole (G: 1)',  # @CONFIRMED
    '\\nt2_big_hole_left': 'T2 Big Left Hole (G: 1)',  # @CONFIRMED
    't2_big_hole_right': 'T2 Big Right Hole (G: 1)',  # @CONFIRMED
    't2_left_box_1': 'T2 Bottom Left Block (G: 0)',  # @CONFIRMED
    't2_right_box_1': 'T2 Bottom Right Block (G: 0)',  # @CONFIRMED
    't2_spawn_teleporter': 'T2 Teleporter (G: 0)',  # @CONFIRMED
    # 'telepad_box': None,  # @NOTPRESENT
    # 'telepad_box_2': None,  # @NOTPRESENT
    'throw_middle_awp': 'Through Middle Awp (G: 1)',  # @CONFIRMED
    'tower_middle_plarform': 'Tower Left Middle Platform (G: 0)|Tower Right Middle Platform (G: 0)',  # @CONFIRMED
    'tower_middle_ramp': 'Tower Middle Ramp (G: 0)',  # @CONFIRMED
    # 'tower_platfrom': None,  # @UNUSED
    'ground_ramp': 'Ground Ramp (G: 0)',  # @CONFIRMED
    't1_middle_hole': 'T1 Middle Hole (G: 1)',  # @CONFIRMED
    'fish_booster_bigger': 'Bigger Fish Booster (G: 0)',  # @CONFIRMED
    'fish_booster_middle': 'Middle Fish Booster (G: 0)',  # @CONFIRMED
    't2_center_down_ramp': 'T2 Center Down Left Ramp (G: 0)|T2 Center Down Right Ramp (G: 0)',  # @CONFIRMED
    't2_center_down_platform': 'T2 Center Down Platform (G: 0)',  # @CONFIRMED
    'w_bezdna': 'Weapon Abyss (G: 0)',  # @CONFIRMED
    'w_bezdna_lower': 'Weapon Lower Abyss (G: 0)',  # @CONFIRMED
    # 'bridge_platform': None,  # @UNUSED
    't1_bezdna': 'T1 Abyss Tower (G: 0)',  # @CONFIRMED
    't1_bezdna_lower': 'T1 Abyss (G: 0)',  # @CONFIRMED
    't1_middle_ramp_upper': 'T1 Middle Ramp Upper (G: 0)',  # @CONFIRMED
    # 'tower_under_middle_ramp': None,  # @UNUSED
    # 'elevator_mid_entrance_floor': None,  # @UNUSED
    'tower_lower_box_1': 'Tower Lower Box 1 (G: 0)',  # @CONFIRMED
    # 'ivan_divan': None,  # @UNUSED
    # 'healbot_ramp_slant': None,  # @UNUSED
    # 'trigger_push': None,  # @UNUSED
    # 'elevator_window_entrance': None,  # @UNUSED
    'fish_ramp_tip': 'Fish Hook Ramp Tip (G: 0)',  # @CONFIRMED
    # 'telepad_box_1': None,  # @NOTPRESENT
    'jail_box_2': 'Jail Box 2 (G: 0)',  # @CONFIRMED
    'tower_box3': 'Tower Box 3 (G: 0)',  # @CONFIRMED
    'tower_box2': 'Tower Box 2 (G: 0)',  # @CONFIRMED
    'telepad_jtct_ramp': 'Telepad J T CT Ramp (G: 0)',  # @CONFIRMED
    'telepad_t2_t1_ramp': 'Telepad T2 T1 Ramp (G: 0)',  # @CONFIRMED
    # 'telepad_platform': None,  # @UNUSED
    # 'telepad_tip': None,  # @NOTPRESENT
    # 'telepad_derevo_leaves': None,  # @UNUSED
    # 'push_starlight': None,  # @UNUSED
    'jail_box_4': 'Jail Box 4 (G: 0)',  # @CONFIRMED
    # 'awp_under_left_platform': None,  # @UNUSED
    # 't2_center_down_boost': None,  # @UNUSED
    # 't1_middle_platform': None,  # @UNUSED
    # 'awp_under_right_platform': None,  # @UNUSED
    't_spawn_hole': 'T-Spawn Hole (G: 1)',  # @CONFIRMED
    'elevator_mid_tip': 'Elevator Hole Tip (G: 0)',  # @CONFIRMED
    't2_big_hole_right_platform': 'T2 Big Right Hole Ground (G: 0)',  # @CONFIRMED
    # 'grob_platform': None,  # @UNUSED
    'tower_derevo': 'Tower Tree (G: 0)',  # @CONFIRMED
    # 'w_tip': None,  # @UNUSED
    # 't_spawn_hole_floor': None,  # @UNUSED
    # 't1_middle_rail': None,  # @UNUSED
    # 'tower_beam': None,  # @UNUSED
    't2_big_hole_left_platform': 'T2 Big Left Hole Ground (G: 0)',  # @CONFIRMED
    # 'ct_spawn_hole_floor': None,  # @UNUSED
    'elevator_window_tip': 'Elevator Window Tip (G: 0)',  # @CONFIRMED
    't2_left_window_platform': 'T2 Left Window Ground (G: 0)',  # @CONFIRMED
    # 'elevator_window_entrance_floor': None,  # @UNUSED
    't2_right_window_platform': 'T2 Right Window Ground (G: 0)',  # @CONFIRMED
    'ground_ramp_reverse': 'Ground Ramp Reverse (G: 0)',  # @CONFIRMED
    'ct_spawn_hole': 'CT-Spawn Hole (G: 1)',  # @CONFIRMED
    'awp_tower_tip': 'Front Awp Window Tip (G: 0)|Rear Awp Window Tip (G: 0)',  # @CONFIRMED
    't2_right_window_tip': 'T2 Right Window Tip (G: 0)',  # @CONFIRMED
    't2_left_window_tip': 'T2 Left Window Tip (G: 0)',  # @CONFIRMED
    'ring': 'Ring (G: 1)',  # @CONFIRMED
    'tower_box': 'T2 Tower Box (G: 0)',  # @CONFIRMED
    # 'grob_booster': None,  # @NOTPRESENT
    't2_big_water_ramp': 'T2 Big Water Ramp (G: 0)',  # @CONFIRMED
    'w_bezdna_lower_ramp': 'Weapon Lower Abyss Ramp (G: 0)',  # @CONFIRMED
    'tower_scout_platform': 'Scout Platform (G: 0)',  # @CONFIRMED
    # 'ct_spawn_water': None,  # @UNUSED
    't_scout_pad': 'T Scout Pad (G: 0)',  # @CONFIRMED
    # 'shrink_lower_beam': None,  # @UNUSED
    # 'parta_home_floor': None,  # @UNUSED
    # 'parta_home_exit': None,  # @UNUSED
    'fish_mini_ramp': 'Fish Mini Ramp (G: 0)',  # @CONFIRMED
    'tower_lower_box_2': 'Tower Lower Box 2 (G: 0)',  # @CONFIRMED
    'sriracha_tip': 'Sriracha Tip (G: 0)'  # @CONFIRMED
})

_TRICK_GXDS_PLAYER_NAMES: Final[dict[str, str]] = MappingProxyType({
    'ÐŸÐ¾Ð²ÐµÐ»Ð¸Ñ‚ÐµÐ»ÑŒ Ñ‚Ñ€ÑŽÐ³Ðµ': 'Evvvai',
    'Using 5 fingers? - Ð¿Ð¸Ð´Ð¾Ñ€Ð°': 'Parta',
    'Autostrafing issues': 'Halisha',
    'xpuctoc': 'Halisha',
    'Insomniac King': 'KingYoshi',
    'games are just waste of time': 'Abyss',
    'Ñ€Ð°Ñ€Ð¸': 'Rari',
    'yakiness': 'Yakiness',
    'cykaeblanishevlagalishe': 'Tsye',
    'ghostie': 'Ghostie'
})

_TRICK_GXDS_PLAYER_ID64S: Final[dict[str, str]] = MappingProxyType({
    '76561198059585682': '76561198279987304',
    '76561198058934072': '76561198150200931'
})


_TRICK_SURF_TIER_POINTS_LIMITS_OLD: Final[tuple[int, ...]] = (
    1300,   # Tier 8
    1225,   # Tier 7
    1000,   # Tier 6
    800,    # Tier 5
    500,    # Tier 4
    200,    # Tier 3
    100,    # Tier 2
    0       # Tier 1
)

_TRICK_SURF_TIER_POINTS_LIMITS_NEW: Final[tuple[int, ...]] = (
    4500,   # Tier 9
    3600,   # Tier 8
    2800,   # Tier 7
    2100,   # Tier 6
    1500,   # Tier 5
    1000,   # Tier 4
    600,    # Tier 3
    300,    # Tier 2
    100     # Tier 1
)

_TRICK_SURF_TIER_POINTS_LIMITS_OLD_LENGTH: Final[int] = len(_TRICK_SURF_TIER_POINTS_LIMITS_OLD)
_TRICK_SURF_TIER_POINTS_LIMITS_NEW_LENGTH: Final[int] = len(_TRICK_SURF_TIER_POINTS_LIMITS_NEW)


_DEFAULT_TRICK_GXDS_SIFT_ENTRIES: Final[bool] = True
_DEFAULT_TRICK_GXDS_USE_NEW_POINTS_SYSTEM: Final[bool] = False
_DEFAULT_TRICK_GXDS_TITLE_CASE_NAMES: Final[bool] = False

_DEFAULT_TRICK_SURF_USE_NEW_POINTS_SYSTEM: Final[bool] = False
_DEFAULT_TRICK_SURF_TITLE_CASE_NAMES: Final[bool] = False


_JSON_INDENT: Final[int] = 4
_JSON_SEPARATORS: Final[tuple[str, str]] = (',', ':')

_ESCAPE_ENCODING: Final[str] = 'unicode-escape'


_ARGUMENT_POINTS_SYSTEM_OLD: Final[str] = 'old'
_ARGUMENT_POINTS_SYSTEM_NEW: Final[str] = 'new'

_NEW_POINTS_SYSTEM_BOOL: Final[dict[str, bool]] = MappingProxyType({
    _ARGUMENT_POINTS_SYSTEM_OLD: False,
    _ARGUMENT_POINTS_SYSTEM_NEW: True
})

_BOOL_VALUES: Final[tuple[bool, bool]] = (False, True)
_BOOL_TRUE_NAMES: Final[tuple[str, ...]] = ('y', 'yes', 't', 'true', 'on', '1')
_BOOL_FALSE_NAMES: Final[tuple[str, ...]] = ('n', 'no', 'f', 'false', 'off', '0')

_CHOICES_ARGUMENT_POINTS_SYSTEM: Final[tuple[str, ...]] = (_ARGUMENT_POINTS_SYSTEM_OLD, _ARGUMENT_POINTS_SYSTEM_NEW)
_CHOICES_ARGUMENT_TRICK_GXDS_POINTS_SYSTEM: Final[tuple[str, ...]] = _CHOICES_ARGUMENT_POINTS_SYSTEM
_CHOICES_ARGUMENT_TRICK_SURF_POINTS_SYSTEM: Final[tuple[str, ...]] = _CHOICES_ARGUMENT_POINTS_SYSTEM
_CHOICES_ARGUMENT_TITLE_CASE_TRICK_NAMES: Final[tuple[bool, ...]] = _BOOL_VALUES
_CHOICES_ARGUMENT_TRICK_GXDS_TITLE_CASE_TRICK_NAMES: Final[tuple[bool, ...]] = _BOOL_VALUES
_CHOICES_ARGUMENT_TRICK_SURF_TITLE_CASE_TRICK_NAMES: Final[tuple[bool, ...]] = _BOOL_VALUES

_DEFAULT_ARGUMENT_LICENSE: Final[bool] = False
_DEFAULT_ARGUMENT_DUMP_TRICK_GXDS_DATA: Final[bool] = False
_DEFAULT_ARGUMENT_DUMP_TRICK_SURF_DATA: Final[bool] = False
_DEFAULT_ARGUMENT_POINTS_SYSTEM: Final[Optional[str]] = None
_DEFAULT_ARGUMENT_TRICK_GXDS_POINTS_SYSTEM: Final[Optional[str]] = None
_DEFAULT_ARGUMENT_TRICK_SURF_POINTS_SYSTEM: Final[Optional[str]] = None
_DEFAULT_ARGUMENT_TITLE_CASE_TRICK_NAMES: Final[Optional[bool]] = None
_DEFAULT_ARGUMENT_TRICK_GXDS_TITLE_CASE_TRICK_NAMES: Final[Optional[bool]] = None
_DEFAULT_ARGUMENT_TRICK_SURF_TITLE_CASE_TRICK_NAMES: Final[Optional[bool]] = None

_CONST_ARGUMENT_LICENSE: Final[bool] = not _DEFAULT_ARGUMENT_LICENSE
_CONST_ARGUMENT_DUMP_TRICK_GXDS_DATA: Final[bool] = not _DEFAULT_ARGUMENT_DUMP_TRICK_GXDS_DATA
_CONST_ARGUMENT_DUMP_TRICK_SURF_DATA: Final[bool] = not _DEFAULT_ARGUMENT_DUMP_TRICK_SURF_DATA


def _unescape(s: Optional[str]) -> Optional[str]:
    if not s:
        return s

    # Fix unicode escaped characters.
    return s.encode(_ESCAPE_ENCODING) \
        .replace(b'\\\\u', b'\\u') \
        .decode(_ESCAPE_ENCODING)


def _get_url_text(url: Optional[str]) -> Optional[str]:
    if not url:
        return None

    return requests.get(url) \
        .text


def _get_url_json(url: Optional[str]) -> Optional[Any]:
    if not url:
        return None

    return requests.get(url) \
        .json()


def _dump_json(
    file_path: Optional[str],
    file_name: Optional[str],
    json_object: Optional[Any]
) -> bool:
    if file_path is None \
            or not json_object:
        return False

    file_path = os.path.normpath(file_path)

    if not file_name:
        if not file_path:
            return False

        file_base_name: Final[str] = os.path.basename(file_path)
        file_split_ext: Final[tuple[str, str]] = os.path.splitext(file_base_name)

        file_path = os.path.dirname(file_path)
        file_name = file_split_ext[0]

    if file_path \
            and not os.path.exists(file_path):
        os.makedirs(file_path)

    dump_path: Final[str] = os.path.join(file_path, file_name)

    with open(dump_path + _DUMP_JSON_FILE_EXT, _OPEN_FILE_WRITE_FLAG, encoding=_DUMP_JSON_FILE_ENCODING) as file:
        file.write(_unescape(json.dumps(json_object, indent=_JSON_INDENT)))

    with open(dump_path + _DUMP_JSON_FILE_MIN_EXT, _OPEN_FILE_WRITE_FLAG, encoding=_DUMP_JSON_FILE_ENCODING) as file:
        file.write(_unescape(json.dumps(json_object, separators=_JSON_SEPARATORS)))

    return True


def _trick_surf_find_tier(
    trick_points_limits: Optional[Union[list[int], tuple[int, ...]]],
    trick_points: Optional[int]
) -> Optional[int]:
    if not trick_points_limits \
            or trick_points is None:
        return None

    trick_tier: int = len(trick_points_limits)
    for points_limit in trick_points_limits:
        if trick_points >= points_limit:
            return trick_tier

        trick_tier -= 1

    if trick_tier > 0:
        return trick_tier

    return None


def _trick_gxds_find_author(
    player_table_rows: Optional[list[tuple[Any, ...]]],
    player_id: Optional[int],
    sift_entries: Optional[bool] = None
) -> Optional[dict[str, Any]]:
    if not player_table_rows \
            or player_id is None:
        return None

    if sift_entries is None:
        sift_entries = _DEFAULT_TRICK_GXDS_SIFT_ENTRIES

    for player_row in player_table_rows:
        if player_row[_TRICK_GXDS_PLAYER_TABLE_ID_COLUMN_INDEX] == player_id:
            player_name: str = player_row[_TRICK_GXDS_PLAYER_TABLE_NAME_COLUMN_INDEX]
            player_id64: str = player_row[_TRICK_GXDS_PLAYER_TABLE_STEAM_ID64_COLUMN_INDEX]

            if sift_entries:
                player_name = _TRICK_GXDS_PLAYER_NAMES.get(player_name, player_name)
                player_id64 = _TRICK_GXDS_PLAYER_ID64S.get(player_id64, player_id64)

            return {
                'PlayerName': player_name,
                'ProfileURL': f'https://steamcommunity.com/profiles/{player_id64}'
            }

    return None


def _trick_gxds_find_route(
    route_table_rows: Optional[list[tuple[Any, ...]]],
    trigger_table_rows: Optional[list[tuple[Any, ...]]],
    trick_id: Optional[int],
    sift_entries: Optional[bool] = None
) -> Optional[list[str]]:
    if not route_table_rows \
            or not trigger_table_rows \
            or trick_id is None:
        return None

    trigger_ids: list[int] = []
    for route_row in route_table_rows:
        if route_row[_TRICK_GXDS_ROUTE_TABLE_TRICK_ID_COLUMN_INDEX] != trick_id:
            continue

        trigger_ids.append(route_row[_TRICK_GXDS_ROUTE_TABLE_TRIGGER_ID_COLUMN_INDEX])

    if not trigger_ids:
        return None

    if sift_entries is None:
        sift_entries = _DEFAULT_TRICK_GXDS_SIFT_ENTRIES

    trigger_names: list[str] = []
    for trigger_id in trigger_ids:
        trigger_name: Optional[str] = None

        for trigger_row in trigger_table_rows:
            if trigger_row[_TRICK_GXDS_TRIGGER_TABLE_ID_COLUMN_INDEX] == trigger_id:
                trigger_name = trigger_row[_TRICK_GXDS_TRIGGER_TABLE_NAME_COLUMN_INDEX]
                if sift_entries:
                    trigger_name = _TRICK_GXDS_TRIGGER_NAMES.get(trigger_name)

                break

        if not trigger_name:
            return None

        trigger_names.append(trigger_name)

    if not trigger_names:
        return None

    return trigger_names


def _trick_gxds_merge_data(
    player_table_rows: Optional[list[tuple[Any, ...]]],
    route_table_rows: Optional[list[tuple[Any, ...]]],
    trick_table_rows: Optional[list[tuple[Any, ...]]],
    trigger_table_rows: Optional[list[tuple[Any, ...]]],
    use_new_points_system: Optional[bool] = None,
    title_case_trick_names: Optional[bool] = None,
    sift_entries: Optional[bool] = None,
) -> Optional[Any]:
    if not player_table_rows \
            or not route_table_rows \
            or not trick_table_rows \
            or not trigger_table_rows:
        return None

    if sift_entries is None:
        sift_entries = _DEFAULT_TRICK_GXDS_SIFT_ENTRIES

    if use_new_points_system is None:
        use_new_points_system = _DEFAULT_TRICK_GXDS_USE_NEW_POINTS_SYSTEM

    if title_case_trick_names is None:
        title_case_trick_names = _DEFAULT_TRICK_GXDS_TITLE_CASE_NAMES

    #   [
    #       {
    #           "Name": "<TRICK-NAME>",
    #           "Points": <TRICK-POINTS>,
    #           "Tier": <TRICK-TIER>,
    #           "PreSpeedLock": <IS-PRE-SPEED-LOCKED?>,
    #           "CreateDate": "<TRICK-CREATE-DATE>",
    #           "UpdateDate": "<TRICK-UPDATE-DATE>",
    #           "CreateTimestamp": <TRICK-CREATE-TIMESTAMP>,
    #           "UpdateTimestamp": <TRICK-UPDATE-TIMESTAMP>,
    #           "Author": {
    #               "PlayerName": "<PLAYER-NAME>",
    #               "ProfileURL": "<PROFILE-URL>"
    #           },
    #           "RoutePath": [
    #               "<TRIGGER-NAME-0>",
    #               "<TRIGGER-NAME-1>",
    #               ...
    #               "<TRIGGER-NAME-N>"
    #           ]
    #       }
    #   ]

    tricks: Final[list[dict[str, Any]]] = []
    for trick_row in trick_table_rows:
        trick_route: Optional[list[str]] \
            = _trick_gxds_find_route(route_table_rows, trigger_table_rows, trick_row[_TRICK_GXDS_TRICK_TABLE_ID_COLUMN_INDEX], sift_entries)

        if not trick_route:
            continue

        trick_points: int = int(trick_row[_TRICK_GXDS_TRICK_TABLE_POINTS_COLUMN_INDEX])
        trick_tier: Optional[int] = _trick_surf_find_tier(_TRICK_SURF_TIER_POINTS_LIMITS_OLD, trick_points)
        if trick_tier is None:
            continue

        if trick_tier > _TRICK_SURF_TIER_POINTS_LIMITS_NEW_LENGTH:
            trick_tier = _TRICK_SURF_TIER_POINTS_LIMITS_NEW_LENGTH

        if sift_entries and use_new_points_system:
            trick_points = _TRICK_SURF_TIER_POINTS_LIMITS_NEW[_TRICK_SURF_TIER_POINTS_LIMITS_NEW_LENGTH - trick_tier]

        trick_name: str = trick_row[_TRICK_GXDS_TRICK_TABLE_NAME_COLUMN_INDEX]
        if sift_entries and title_case_trick_names:
            trick_name = string.capwords(trick_name)

        trick_pre_speed_lock: bool = not int(trick_row[_TRICK_GXDS_TRICK_TABLE_VELOCITY_COLUMN_INDEX]) == 1
        trick_date: str = trick_row[_TRICK_GXDS_TRICK_TABLE_CREATE_DATE_COLUMN_INDEX]

        trick_datetime: datetime = ciso8601.parse_datetime(trick_date)
        trick_timestamp: int = int(time.mktime(trick_datetime.timetuple())) - _TIME_ZONE_OFFSET

        trick_author: Optional[dict[str, Any]] \
            = _trick_gxds_find_author(player_table_rows, trick_row[_TRICK_GXDS_TRICK_TABLE_AUTHOR_ID_COLUMN_INDEX], sift_entries)

        tricks.append({
            'Name': trick_name,
            'Points': trick_points,
            'Tier': trick_tier,
            'PreSpeedLock': trick_pre_speed_lock,
            'CreateDate': trick_date,
            'UpdateDate': trick_date,
            'CreateTimestamp': trick_timestamp,
            'UpdateTimestamp': trick_timestamp,
            'Author': trick_author,
            'RoutePath': trick_route
        })

    if not tricks:
        return None

    return tricks


def _trick_gxds_dump_data(
    use_new_points_system: Optional[bool] = None,
    title_case_trick_names: Optional[bool] = None
) -> bool:
    # TrickGxds' player table & its rows.
    player_table_text: Optional[str] \
        = _get_url_text(_TRICK_GXDS_PLAYER_TABLE_URL)

    player_table_rows: Final[list[tuple[Any, ...]]] \
        = re.findall(_TRICK_GXDS_PLAYER_TABLE_ROW_REGEX, player_table_text, _REGEX_MULTILINE_FLAG)

    if not player_table_rows:
        return False

    # TrickGxds' route table & its rows.
    route_table_text: Optional[str] \
        = _get_url_text(_TRICK_GXDS_ROUTE_TABLE_URL)

    route_table_rows: Final[list[tuple[Any, ...]]] \
        = re.findall(_TRICK_GXDS_ROUTE_TABLE_ROW_REGEX, route_table_text, _REGEX_MULTILINE_FLAG)

    if not route_table_rows:
        return False

    # TrickGxds' trick table & its rows.
    trick_table_text: Optional[str] \
        = _get_url_text(_TRICK_GXDS_TRICK_TABLE_URL)

    trick_table_rows: Final[list[tuple[Any, ...]]] \
        = re.findall(_TRICK_GXDS_TRICK_TABLE_ROW_REGEX, trick_table_text, _REGEX_MULTILINE_FLAG)

    if not trick_table_rows:
        return False

    # TrickGxds' trigger table & its rows.
    trigger_table_text: Optional[str] \
        = _get_url_text(_TRICK_GXDS_TRIGGER_TABLE_URL)

    trigger_table_rows: Final[list[tuple[Any, ...]]] \
        = re.findall(_TRICK_GXDS_TRIGGER_TABLE_ROW_REGEX, trigger_table_text, _REGEX_MULTILINE_FLAG)

    if not trigger_table_rows:
        return False

    # TrickGxds' merged JSON w/ original entries.
    original_json: Final[Optional[Any]] \
        = _trick_gxds_merge_data(
            player_table_rows,
            route_table_rows,
            trick_table_rows,
            trigger_table_rows,
            use_new_points_system,
            title_case_trick_names,
            sift_entries=False,
        )

    # TrickGxds' merged JSON w/ sifted entries.
    sifted_json: Final[Optional[Any]] \
        = _trick_gxds_merge_data(
            player_table_rows,
            route_table_rows,
            trick_table_rows,
            trigger_table_rows,
            use_new_points_system,
            title_case_trick_names,
            sift_entries=True
        )

    return _dump_json(_DUMP_UNIFIED_PATH, _DUMP_UNIFIED_ORIGINAL_NAME, original_json) \
        and _dump_json(_DUMP_UNIFIED_PATH, _DUMP_UNIFIED_SIFTED_NAME, sifted_json)


# noinspection PyUnusedLocal
def _trick_surf_dump_data(
    use_new_points_system: Optional[bool] = None,
    title_case_trick_names: Optional[bool] = None
) -> bool:
    if use_new_points_system is None:
        use_new_points_system = _DEFAULT_TRICK_SURF_USE_NEW_POINTS_SYSTEM

    if title_case_trick_names is None:
        title_case_trick_names = _DEFAULT_TRICK_SURF_TITLE_CASE_NAMES

    return False


def _str_to_bool(
    val: Optional[Any],
) -> bool:
    if val is None:
        return False

    if isinstance(val, bool):
        return val

    lower_val = str(val) \
        .lower()

    if lower_val in _BOOL_TRUE_NAMES:
        return True

    if lower_val in _BOOL_FALSE_NAMES:
        return False

    raise ValueError(f'Couldn\'t convert "{val}" to a boolean value')


def _main() -> None:
    arg_parser: Final[ArgumentParser] = ArgumentParser()

    arg_parser.add_argument(
        '-l',
        '--license',
        help='show the project license and exit',
        dest='is_license_flag',
        action='store_const',
        const=_CONST_ARGUMENT_LICENSE,
        default=_DEFAULT_ARGUMENT_LICENSE
    )

    arg_parser.add_argument(
        '--dump-trick-gxds-data',
        help='dump trick gxds data to json files',
        dest='is_dump_trick_gxds_data_flag',
        action='store_const',
        const=_CONST_ARGUMENT_DUMP_TRICK_GXDS_DATA,
        default=_DEFAULT_ARGUMENT_DUMP_TRICK_GXDS_DATA
    )

    arg_parser.add_argument(
        '--dump-trick-surf-data',
        help='dump trick surf data to json files',
        dest='is_dump_trick_surf_data_flag',
        action='store_const',
        const=_CONST_ARGUMENT_DUMP_TRICK_SURF_DATA,
        default=_DEFAULT_ARGUMENT_DUMP_TRICK_SURF_DATA
    )

    arg_parser.add_argument(
        '--points-system',
        help='type of points system to use for all data dump',
        dest='points_system',
        action='store',
        choices=_CHOICES_ARGUMENT_POINTS_SYSTEM,
        default=_DEFAULT_ARGUMENT_POINTS_SYSTEM
    )

    arg_parser.add_argument(
        '--trick-gxds-points-system',
        help='type of points system to use for trick gxds data dumps',
        dest='trick_gxds_points_system',
        action='store',
        choices=_CHOICES_ARGUMENT_TRICK_GXDS_POINTS_SYSTEM,
        default=_DEFAULT_ARGUMENT_TRICK_GXDS_POINTS_SYSTEM
    )

    arg_parser.add_argument(
        '--trick-surf-points-system',
        help='type of points system to use for trick surf data dumps',
        dest='trick_surf_points_system',
        action='store',
        choices=_CHOICES_ARGUMENT_TRICK_SURF_POINTS_SYSTEM,
        default=_DEFAULT_ARGUMENT_TRICK_SURF_POINTS_SYSTEM
    )

    arg_parser.add_argument(
        '--title-case-trick-names',
        type=_str_to_bool,
        help='convert trick names to title case for all data dumps',
        dest='title_case_trick_names',
        action='store',
        choices=_CHOICES_ARGUMENT_TITLE_CASE_TRICK_NAMES,
        default=_DEFAULT_ARGUMENT_TITLE_CASE_TRICK_NAMES
    )

    arg_parser.add_argument(
        '--trick-gxds-title-case-trick-names',
        type=_str_to_bool,
        help='convert trick names to title case for trick gxds data dumps',
        dest='trick_gxds_title_case_trick_names',
        action='store',
        choices=_CHOICES_ARGUMENT_TRICK_GXDS_TITLE_CASE_TRICK_NAMES,
        default=_DEFAULT_ARGUMENT_TRICK_GXDS_TITLE_CASE_TRICK_NAMES
    )

    arg_parser.add_argument(
        '--trick-surf-title-case-trick-names',
        type=_str_to_bool,
        help='convert trick names to title case for trick surf data dumps',
        dest='trick_surf_title_case_trick_names',
        action='store',
        choices=_CHOICES_ARGUMENT_TRICK_SURF_TITLE_CASE_TRICK_NAMES,
        default=_DEFAULT_ARGUMENT_TRICK_SURF_TITLE_CASE_TRICK_NAMES
    )

    args: Final[ArgumentNamespace] = arg_parser.parse_args()

    if args.is_license_flag:
        more_path: Final[Optional[str]] = shutil.which('more')
        if not more_path:
            with open(_LICENSE_PATH, _OPEN_FILE_READ_FLAG) as file:
                print(file.read())

            return

        more_process: Final[Popen] = Popen([more_path, _LICENSE_PATH])
        more_process.wait()

        return

    use_new_points_system: Final[Optional[bool]] \
        = _NEW_POINTS_SYSTEM_BOOL.get(args.points_system)

    if use_new_points_system is not None:
        if args.trick_gxds_points_system is None:
            args.trick_gxds_points_system = args.points_system

        if args.trick_surf_points_system is None:
            args.trick_surf_points_system = args.points_system

    trick_gxds_use_new_points_system: Final[Optional[bool]] \
        = _NEW_POINTS_SYSTEM_BOOL.get(args.trick_gxds_points_system)

    trick_surf_use_new_points_system: Final[Optional[bool]] \
        = _NEW_POINTS_SYSTEM_BOOL.get(args.trick_surf_points_system)

    if args.title_case_trick_names is not None:
        if args.trick_gxds_title_case_trick_names is None:
            args.trick_gxds_title_case_trick_names = args.title_case_trick_names

        if args.trick_surf_title_case_trick_names is None:
            args.trick_surf_title_case_trick_names = args.title_case_trick_names

    trick_gxds_title_case_trick_names: Final[Optional[bool]] = \
        args.trick_gxds_title_case_trick_names

    trick_surf_title_case_trick_names: Final[Optional[bool]] = \
        args.trick_surf_title_case_trick_names

    # noinspection PyUnusedLocal
    is_success: Optional[bool] = None

    if args.is_dump_trick_gxds_data_flag:
        is_success \
            = _trick_gxds_dump_data(
                trick_gxds_use_new_points_system,
                trick_gxds_title_case_trick_names
            )

        if is_success:
            print(_SUCCESS_MESSAGE_DUMP_TRICK_GXDS_DATA, file=_STD_OUT_STREAM)
        else:
            print(_FAILURE_MESSAGE_DUMP_TRICK_GXDS_DATA, file=_STD_ERR_STREAM)

    if args.is_dump_trick_surf_data_flag:
        is_success \
            = _trick_surf_dump_data(
                trick_surf_use_new_points_system,
                trick_surf_title_case_trick_names
            )

        if is_success:
            print(_SUCCESS_MESSAGE_DUMP_TRICK_SURF_DATA, file=_STD_OUT_STREAM)
        else:
            print(_FAILURE_MESSAGE_DUMP_TRICK_SURF_DATA, file=_STD_ERR_STREAM)


if __name__ == '__main__':
    try:
        _main()
    except KeyboardInterrupt:
        pass
