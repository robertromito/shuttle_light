from enum import IntEnum

import sys, termios, traceback, tty

import rich

from shuttle_light.ring_light import RingLight

class Keys(IntEnum):
    Q = 113
    SPACE = 32
    UP = 65
    DOWN = 66
    RIGHT = 67
    LEFT = 68
    ENTER = 13


def main():
    """
    Run the light control tool
    """
    return_code = 0

    fd = sys.stdin.fileno()
    old_term_settings = termios.tcgetattr(fd)

    help = (
        "[ on/off: space | "
        "brighter: up | "
        "dimmer: down | "
        "cooler: left | "
        "warmer: right | "
        "quit: q ]"

    )

    banner = (
        f"[bold reverse cyan] Shuttle {((len(help)//2) - len(' Shuttle ')) * ' '}[/]",
        f"[bold reverse yellow] Light {((len(help)//2) - len(' Light ')) * ' '}[/]"
    )

    # rich.print(*banner, sep = (len(help)//2) * " ")
    rich.print(*banner, sep = '')
    rich.print(help)

    try:
        tty.setraw(fd)
        light = RingLight()
        light_settings = light.current_settings()
        while True:
            print('\r',end='')
            rich.print(f">> {light_settings}", end='')
            event = ord(sys.stdin.read(1))
            match event:
                case Keys.Q:
                    break
                case Keys.SPACE:
                    light_settings.on = int(not light_settings.on)
                    light_settings = light.send_settings(light_settings)
                case Keys.UP:
                    light_settings.brightness += 1
                case Keys.DOWN:
                    light_settings.brightness -= 1
                case Keys.LEFT:
                    light_settings.temperature -= 1
                case Keys.RIGHT:
                    light_settings.temperature += 1
                case Keys.ENTER:
                    light_settings = light.send_settings(light_settings)

    except KeyboardInterrupt:
        return_code = 1

    except Exception as ex:
        print("\n\r")
        traceback.print_exc()
        return_code = 2

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_term_settings)
        sys.exit(return_code)

if __name__ == "main":
    main()