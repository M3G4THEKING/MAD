from mapadroid.db.resource_definitions.Resource import Resource


class Device(Resource):
    # TODO: handle name_field and search_field at all?
    # TODO: Handle validation....
    # TODO: Handle dependencies?
    name_field = 'origin'
    search_field = 'name'
    translations = {
        'origin': 'name',
        'pool': 'pool_id',
        'walker': 'walker_id',
    }
    configuration = {
        "fields": {
            "origin": {
                "settings": {
                    "type": "text",
                    "require": True,
                    "description": "Name of device (from RGC settings)",
                    "expected": str
                }
            },
            "walker": {
                "settings": {
                    "type": "walkerselect",
                    "require": True,
                    "description": "Walker of this area",
                    "expected": int,
                    "uri": True,
                    "data_source": "walker",
                    "uri_source": "api_walker"
                }
            },
            "pool": {
                "settings": {
                    "type": "poolselect",
                    "require": False,
                    "empty": None,
                    "description": "Configpool for this area",
                    "expected": int,
                    "uri": True,
                    "data_source": "devicepool",
                    "uri_source": "api_devicepool"
                }
            },
            "adbname": {
                "name": "adbname",
                "settings": {
                    "type": "adbselect",
                    "require": False,
                    "empty": None,
                    "description": "ADB devicename",
                    "expected": str
                }
            },
            "interface_type": {
                "settings": {
                    "type": "option",
                    "values": ["lan", "wlan"],
                    "require": False,
                    "description": "Interface type to use",
                    "expected": str
                }
            },
            "mac_address": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "MAC address of the device",
                    "expected": str
                }
            },
            "post_walk_delay": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Delay in seconds after reaching destination with the speed given (Default: 0)",
                    "expected": float
                }
            },
            "post_teleport_delay": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Delay in seconds after teleport (Default: 0)",
                    "expected": float
                }
            },
            "walk_after_teleport_distance": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Walk in meters to walk after teleport. Might help loading data (Default: 0)",
                    "expected": float
                }
            },
            "cool_down_sleep": {
                "settings": {
                    "type": "option",
                    "require": False,
                    "values": [None, False, True],
                    "description": "Add extra cooldown after teleport (Default: False)",
                    "expected": bool
                }
            },
            "post_turn_screen_on_delay": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Delay in seconds after a screenshot has been taken and about to be saved (Default: "
                                   "2.0 / 7.0 - Task Dependent)",
                    "expected": float
                }
            },
            "post_pogo_start_delay": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Delay in seconds to wait after starting pogo (Default: 60.0)",
                    "expected": float
                }
            },
            "restart_pogo": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Restart Pogo every N location-changes (Default: 0.  0 for never)",
                    "expected": int
                }
            },
            "inventory_clear_rounds": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Number of rounds to clear the inventory. (Default: 10)",
                    "expected": int
                }
            },
            "mitm_wait_timeout": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Timeout in seconds while waiting for data after setting/reaching a location. "
                                   "(Default: 45)",
                    "expected": float
                }
            },
            "vps_delay": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Set click delay for pokestop walker (VPS -> local device) (Default: 0)",
                    "expected": float
                }
            },
            "reboot": {
                "settings": {
                    "type": "option",
                    "require": False,
                    "values": [None, True, False],
                    "description": "Reboot device if reboot_thresh is reached (Default: True)",
                    "expected": bool
                }
            },
            "reboot_thresh": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Restart device after restart Pogo N times. This value is doubled when init is "
                                   "active (Default: 3)",
                    "expected": int
                }
            },
            "restart_thresh": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Restart Pogo after reaching MITM Timeout N times. This value is doubled when init "
                                   "is active (Default: 5)",
                    "expected": int
                }
            },
            "post_screenshot_delay": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "The delay in seconds to wait after taking a screenshot to copy it and start the "
                                   "next (Default: 1)",
                    "expected": float
                }
            },
            "screenshot_x_offset": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Adjust the x-axis click offset on devices with softbars and/or black upper bars. "
                                   "(+ right - left / Default: 0)",
                    "expected": int
                }
            },
            "screenshot_y_offset": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Adjust the y-axis click offset on devices. "
                                   "If softbar_enabled is True, the values will be added up. "
                                   "(+ down - up / Default: 0)",
                    "expected": int
                }
            },
            "softbar_enabled": {
                "settings": {
                    "type": "option",
                    "require": False,
                    "values": [None, True, False],
                    "description": "If a softbar button is visible on screenshots, set to true. "
                                   "The offset will be read automatically (Default: False)",
                    "expected": bool,
                }
            },
            "extended_permission_toggling": {
                "settings": {
                    "type": "option",
                    "require": True,
                    "values": [True, False],
                    "description": "Whether e.g. magisk should be toggled on/off regularly (Default: False)",
                    "expected": bool,
                }
            },
            "screenshot_type": {
                "settings": {
                    "type": "option",
                    "require": False,
                    "values": [None, "jpeg", "png"],
                    "description": "Type of screenshot (Default: jpeg)",
                    "expected": str
                }
            },
            "screenshot_quality": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Quality of screenshot (Default: 80)",
                    "expected": int
                }
            },
            "startcoords_of_walker": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Start Coords of Walker (Default: None) (Format: 123.45,67.89)",
                    "expected": str
                }
            },
            "screendetection": {
                "settings": {
                    "type": "option",
                    "values": [None, True, False],
                    "require": False,
                    "description": "Use this argument if there are login/logout problems with this device or you want "
                                   "to levelup accounts  (Default: True)",
                    "expected": bool
                }
            },
            "ggl_login_mail": {
                "settings": {
                    "type": "select",
                    "require": False,
                    "description": "Declare a login address or domain from device (Empty = first @gmail.com entry).  "
                                   "Use ',' to set more the one account (address|address)",
                    "expected": str
                }
            },
            "clear_game_data": {
                "settings": {
                    "type": "option",
                    "values": [None, False, True],
                    "require": False,
                    "description": "Clear game data if logins fail multiple times (Default: False)",
                    "expected": bool
                }
            },
            "account_rotation": {
                "settings": {
                    "type": "option",
                    "values": [None, False, True],
                    "require": False,
                    "description": "Rotate accounts (f.e. to prevent long cool downs) - Only for PTC (Default: False)",
                    "expected": bool
                }
            },
            "rotation_waittime": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Rotate accounts if wait time is longer than x seconds after teleport.  Requires "
                                   "account_rotation to be enabled (Default: 300)",
                    "expected": float
                }
            },
            "rotate_on_lvl_30": {
                "settings": {
                    "type": "option",
                    "values": [None, False, True],
                    "require": False,
                    "description": "Rotate accounts if player level >= 30 (for leveling mode)  (Default: False)",
                    "expected": bool
                }
            },
            "injection_thresh_reboot": {
                "settings": {
                    "type": "text",
                    "require": False,
                    "description": "Reboot (if enabled) device after not injecting for X times in a row (Default: 20)",
                    "expected": int
                }
            },
            "enhanced_mode_quest_safe_items": {
                "settings": {
                    "type": "select",
                    "require": False,
                    "description": "Items not to be deleted in quest mode (Default: 1401, 1402, "
                                   "1403, 1106, 901, 902, 903, 501, 502, 503, 504, 301)",
                    "expected": str,
                    "default": "1401, 1402, 1403, 1106, 901, 902, 903, 501, 502, 503, 504, 301"
                }
            }
        }
    }
