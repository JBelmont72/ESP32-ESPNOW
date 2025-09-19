'''
templates for both RPI and Micropython

'''
"""
 First: Cross-platform template for ESP32 (MicroPython) and Raspberry Pi (gpiozero).
Detects platform, prints firmware/version, and ensures clean exit.
Second: reusable base template (with stub setup(), loop(), cleanup() functions) so you can just drop in different hardware logic
## Third: add a generic logging wrapper (so it prints [ESP32] message or [RaspberryPi] message automatically) to make debugging easier when switching between platforms

Fourth: Key idea:
main() already has an outer try/except/finally for KeyboardInterrupt and cleanup.
Inside loop() you can have your own try/except for functional errors (bad sensor read, division by zero, etc.), so your device doesn’t crash completely

"""

# import sys

# # Platform detection		#First
# def detect_platform():
#     try:
#         import machine  # Only available in MicroPython
#         import os
#         uname = os.uname()
#         return {
#             "platform": "esp32",
#             "name": uname.sysname,
#             "version": uname.release,
#             "details": uname
#         }
#     except ImportError:
#         # Assume Raspberry Pi
#         import platform
#         return {
#             "platform": "raspberrypi",
#             "name": platform.system(),
#             "version": platform.release(),
#             "details": platform.uname()
#         }


# def main():
#     info = detect_platform()
#     print("Platform:", info["platform"])
#     print("System Name:", info["name"])
#     print("Version:", info["version"])
#     print("Details:", info["details"])

#     # Example resource
#     if info["platform"] == "raspberrypi":
#         from gpiozero import LED
#         from signal import pause
#         led = LED(17)  # Example pin

#         try:
#             print("Blinking LED on Raspberry Pi. Press Ctrl+C to exit.")
#             led.blink()
#             pause()  # Wait for signal (Ctrl+C)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt detected on Raspberry Pi.")
#         finally:
#             print("Cleaning up Raspberry Pi resources...")
#             led.close()

#     elif info["platform"] == "esp32":
#         from machine import Pin
#         import time
#         led = Pin(2, Pin.OUT)  # Built-in LED on many ESP32 boards

#         try:
#             print("Blinking LED on ESP32. Press Ctrl+C to exit.")
#             while True:
#                 led.value(1)
#                 time.sleep(0.5)
#                 led.value(0)
#                 time.sleep(0.5)
#         except KeyboardInterrupt:
#             print("\nKeyboardInterrupt detected on ESP32.")
#         finally:
#             print("Cleaning up ESP32 resources...")
#             led.init(Pin.IN)  # Deinit LED pin


# if __name__ == "__main__":
#     main()

# ## Second: reusable base template (with stub setup(), loop(), cleanup() functions) so you can just drop in different hardware logic
   

# """
# Cross-platform base template for ESP32 (MicroPython) and Raspberry Pi (gpiozero).
# Provides setup(), loop(), cleanup() with platform detection and safe exit.
# """

# import sys

# # ---------------------------
# # Platform detection
# # ---------------------------
# def detect_platform():
#     try:
#         import machine  # Only available in MicroPython
#         import os
#         uname = os.uname()
#         return {
#             "platform": "esp32",
#             "name": uname.sysname,
#             "version": uname.release,
#             "details": uname
#         }
#     except ImportError:
#         # Assume Raspberry Pi
#         import platform
#         return {
#             "platform": "raspberrypi",
#             "name": platform.system(),
#             "version": platform.release(),
#             "details": platform.uname()
#         }


# # ---------------------------
# # Platform-specific setup
# # ---------------------------
# def setup(info):
#     if info["platform"] == "raspberrypi":
#         from gpiozero import LED
#         led = LED(17)  # Example pin
#         return {"led": led}

#     elif info["platform"] == "esp32":
#         from machine import Pin
#         led = Pin(2, Pin.OUT)  # Built-in LED
#         return {"led": led}

#     return {}


# # ---------------------------
# # Platform-specific loop
# # ---------------------------
# def loop(info, resources):
#     import time

#     if info["platform"] == "raspberrypi":
#         print("Blinking LED on Raspberry Pi. Press Ctrl+C to exit.")
#         from signal import pause
#         resources["led"].blink()
#         pause()  # Blocks until Ctrl+C

#     elif info["platform"] == "esp32":
#         print("Blinking LED on ESP32. Press Ctrl+C to exit.")
#         led = resources["led"]
#         while True:
#             led.value(1)
#             time.sleep(0.5)
#             led.value(0)
#             time.sleep(0.5)


# # ---------------------------
# # Platform-specific cleanup
# # ---------------------------
# def cleanup(info, resources):
#     if info["platform"] == "raspberrypi":
#         print("Cleaning up Raspberry Pi resources...")
#         resources["led"].close()

#     elif info["platform"] == "esp32":
#         from machine import Pin
#         print("Cleaning up ESP32 resources...")
#         resources["led"].init(Pin.IN)  # Release LED pin


# # ---------------------------
# # Main entry point
# # ---------------------------
# def main():
#     info = detect_platform()
#     print("Platform:", info["platform"])
#     print("System Name:", info["name"])
#     print("Version:", info["version"])
#     print("Details:", info["details"])

#     resources = setup(info)

#     try:
#         loop(info, resources)
#     except KeyboardInterrupt:
#         print("\nKeyboardInterrupt detected, exiting gracefully...")
#     finally:
#         cleanup(info, resources)


# if __name__ == "__main__":
#     main()
# #### Third:   add a generic logging wrapper (so it prints [ESP32] message or [RaspberryPi] message automatically) to make debugging easier when switching between platforms
# def loop(info, resources):		##just the loop() with example of how to add the working portion
#     import time

#     if info["platform"] == "raspberrypi":
#         from gpiozero import Button
#         button = Button(27)

#         print("Blink LED on Raspberry Pi. Ctrl+C to exit.")
#         led = resources["led"]

#         try:
#             while True:
#                 if button.is_pressed:
#                     led.on()
#                     time.sleep(0.1)
#                     led.off()
#                     time.sleep(0.1)
#                 else:
#                     led.on()
#                     time.sleep(0.5)
#                     led.off()
#                     time.sleep(0.5)
#         except Exception as e:
#             print("Error in loop:", e)

#     elif info["platform"] == "esp32":
#         from machine import Pin
#         button = Pin(0, Pin.IN)  # Example button on GPIO0
#         led = resources["led"]

#         print("Blink LED on ESP32. Ctrl+C to exit.")

#         try:
#             while True:
#                 if button.value() == 0:  # pressed
#                     led.value(1)
#                     time.sleep(0.1)
#                     led.value(0)
#                     time.sleep(0.1)
#                 else:
#                     led.value(1)
#                     time.sleep(0.5)
#                     led.value(0)
#                     time.sleep(0.5)
#         except Exception as e:
#             print("Error in loop:", e)
# ## Fourth nested try/except pattern for loop() that does three things:
# #Keeps running if a recoverable runtime error happens (e.g. sensor read error).
# #Breaks immediately on KeyboardInterrupt (Ctrl+C).
# #Still allows cleanup() in finally



# def loop(info, resources):
#     import time

#     print(f"Starting loop on {info['platform']} (Ctrl+C to exit).")

#     led = resources["led"]

#     while True:
#         try:
#             # ---- Main work goes here ----
#             led.value(1)
#             time.sleep(0.2)
#             led.value(0)
#             time.sleep(0.2)

#             # Example of simulated runtime error
#             # remove this in real code
#             # raise ValueError("Simulated sensor error")

#         except KeyboardInterrupt:
#             # Let outer try/finally handle cleanup
#             print("\nKeyboardInterrupt received. Breaking loop...")
#             break

#         except Exception as e:
#             # Handle other runtime errors without crashing
#             print("Runtime error in loop:", e)
#             # Optional: wait a bit before retry
#             time.sleep(1)
# '''
# Why this works
# Outer try/except/finally in main()
# → guarantees cleanup (release GPIO, deinit pins).
# Inner try/except inside while True:
# → lets you catch normal runtime errors (e.g. sensor returning None) and keep running.
# KeyboardInterrupt gets re-raised (via break)
# → allows graceful shutdown, not swallowed by the generic except Exception.
# Execution flow
# Start loop.
# If something minor fails → caught by except Exception, printed, loop continues.
# If user presses Ctrl+C → caught by except KeyboardInterrupt, break loop, exit to outer finally, run cleanup().
# '''
# """
# Cross-platform MicroPython (ESP32) + Raspberry Pi (gpiozero) template.
# - Detects platform and prints version info.
# - Provides setup(), loop(), and cleanup() functions.
# - Handles Ctrl+C cleanly with try/except/finally.
# - Supports nested try/except inside loop() for runtime errors.

# Customize `setup()`, `loop()`, and `cleanup()` for your hardware needs.
# """

# import sys      ## universal template
# #/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Universal_template.py
# # also copy in RPI_1 workspace
# # ---------------------------
# # Platform detection		Consolidated
# # ---------------------------
# def detect_platform():
#     try:
#         import machine  # MicroPython only
#         import os
#         uname = os.uname()
#         return {
#             "platform": "esp32",
#             "name": uname.sysname,
#             "version": uname.release,
#             "details": uname
#         }
#     except ImportError:
#         # Assume Raspberry Pi
#         import platform
#         return {
#             "platform": "raspberrypi",
#             "name": platform.system(),
#             "version": platform.release(),
#             "details": platform.uname()
#         }


# # ---------------------------
# # Platform-specific setup
# # ---------------------------
# def setup(info):
#     """
#     Initialize hardware resources here.
#     Add imports specific to each platform inside the conditions.
#     """
#     if info["platform"] == "raspberrypi":
#         from gpiozero import LED  # Import modules as needed
#         led = LED(17)             # Example: LED on GPIO17
#         return {"led": led}

#     elif info["platform"] == "esp32":
#         from machine import Pin   # Import modules as needed
#         led = Pin(2, Pin.OUT)     # Example: built-in LED
#         return {"led": led}

#     return {}  # Empty resources if nothing initialized


# # ---------------------------
# # Platform-specific loop
# # ---------------------------
# def loop(info, resources):
#     """
#     Main program logic.
#     Runs inside a while True loop with nested try/except:
#       - KeyboardInterrupt cleanly breaks loop.
#       - Other runtime errors are caught and logged, loop continues.
#     """
#     import time
#     led = resources.get("led")

#     print(f"Starting loop on {info['platform']} (Ctrl+C to exit).")

#     while True:
#         try:
#             # ---- MAIN WORK SECTION ----
#             # Replace this LED blink example with your logic.
#             led.on() if info["platform"] == "raspberrypi" else led.value(1)
#             time.sleep(0.5)
#             led.off() if info["platform"] == "raspberrypi" else led.value(0)
#             time.sleep(0.5)

#         except KeyboardInterrupt:
#             # Allows graceful exit
#             print("\nKeyboardInterrupt received. Exiting loop...")
#             break

#         except Exception as e:
#             # Catch other errors without crashing
#             print("Runtime error in loop:", e)
#             time.sleep(1)  # Optional backoff before retry


# # ---------------------------
# # Platform-specific cleanup
# # ---------------------------
# def cleanup(info, resources):
#     """
#     Release resources, close devices, deinit pins, etc.
#     """
#     if info["platform"] == "raspberrypi":
#         print("Cleaning up Raspberry Pi resources...")
#         resources.get("led") and resources["led"].close()

#     elif info["platform"] == "esp32":
#         from machine import Pin
#         print("Cleaning up ESP32 resources...")
#         if "led" in resources:
#             resources["led"].init(Pin.IN)  # Reset pin to input


# # ---------------------------
# # Main entry point
# # ---------------------------
# def main():
#     info = detect_platform()
#     print("Platform:", info["platform"])
#     print("System Name:", info["name"])
#     print("Version:", info["version"])
#     print("Details:", info["details"])

#     resources = setup(info)

#     try:
#         loop(info, resources)
#     finally:
#         cleanup(info, resources)


# if __name__ == "__main__":
#     main()


# #####~~~~~~



# """
# Cross-platform MicroPython (ESP32) + Raspberry Pi (gpiozero) template.
# Includes LED (output), Button (input), and Servo (output).
# Handles setup, loop, and cleanup safely with try/except/finally.
# """

import sys      # universal setup for RPI and micropython

#/Users/judsonbelmont/Documents/SharedFolders/ESP32/ESP32-ESPNOW/Universal_template.py
# also copy in RPI_1 workspace
# ---------------------------
# Platform detection
# ---------------------------
def detect_platform():
    try:
        import machine  # MicroPython only
        import os
        uname = os.uname()
        return {
            "platform": "esp32",
            "name": uname.sysname,
            "version": uname.release,
            "details": uname
        }
    except ImportError:
        # Assume Raspberry Pi
        import platform
        return {
            "platform": "raspberrypi",
            "name": platform.system(),
            "version": platform.release(),
            "details": platform.uname()
        }


# ---------------------------
# Platform-specific setup
# ---------------------------
def setup(info):
    """
    Initialize hardware resources (LED, Button, Servo).
    """
    if info["platform"] == "raspberrypi":
        from gpiozero import LED, Button, Servo

        led = LED(17)             # GPIO17 LED
        button = Button(27)       # GPIO27 Button
        servo = Servo(18)         # GPIO18 Servo (hardware PWM pin)

        return {"led": led, "button": button, "servo": servo}

    elif info["platform"] == "esp32":
        from machine import Pin, PWM

        led = Pin(2, Pin.OUT)     # Built-in LED
        button = Pin(0, Pin.IN, Pin.PULL_UP)  # GPIO0 Button w/ pull-up

        # Servo on GPIO15 (pick a PWM-capable pin)
        pwm = PWM(Pin(15), freq=50)  # Standard servo freq: 50 Hz

        # Helper to set servo angle (0–180 degrees)
        def set_angle(angle):
            # duty_u16: 0–65535 range
            min_duty = 1638   # ~0.5 ms pulse
            max_duty = 8192   # ~2.5 ms pulse
            duty = int(min_duty + (max_duty - min_duty) * angle / 180)
            pwm.duty_u16(duty)

        return {"led": led, "button": button, "servo": pwm, "set_angle": set_angle}

    return {}


# ---------------------------
# Main loop
# ---------------------------
def loop(info, resources):
    """
    Example: 
    - Blink LED at different speeds depending on button state.
    - Sweep servo angle when button pressed.
    """
    import time
    led = resources.get("led")
    button = resources.get("button")

    print(f"Starting loop on {info['platform']} (Ctrl+C to exit).")

    while True:
        try:
            if info["platform"] == "raspberrypi":
                servo = resources.get("servo")

                if button.is_pressed:
                    print("Button pressed → fast blink, servo sweep.")
                    led.blink(0.1, 0.1, background=False)

                    # Servo sweep
                    for angle in [-1, 0, 1]:  # gpiozero uses -1 to +1
                        servo.value = angle
                        time.sleep(0.5)
                else:
                    print("Button not pressed → slow blink.")
                    led.blink(0.5, 0.5, background=False)

            elif info["platform"] == "esp32":
                servo_pwm = resources.get("servo")
                set_angle = resources.get("set_angle")

                if button.value() == 0:  # pressed (active low)
                    print("Button pressed → fast blink, servo sweep.")
                    for angle in range(0, 181, 45):  # 0→180 degrees
                        resources["led"].value(1)
                        set_angle(angle)
                        time.sleep(0.2)
                        resources["led"].value(0)
                        time.sleep(0.2)
                else:
                    print("Button not pressed → slow blink.")
                    resources["led"].value(1)
                    time.sleep(0.5)
                    resources["led"].value(0)
                    time.sleep(0.5)

        except KeyboardInterrupt:
            print("\nKeyboardInterrupt received. Exiting loop...")
            break

        except Exception as e:
            print("Runtime error in loop:", e)
            time.sleep(1)


# ---------------------------
# Cleanup
# ---------------------------
def cleanup(info, resources):
    """
    Release resources, close devices, deinit pins.
    """
    if info["platform"] == "raspberrypi":
        print("Cleaning up Raspberry Pi resources...")
        if "led" in resources:
            resources["led"].close()
        if "button" in resources:
            resources["button"].close()
        if "servo" in resources:
            resources["servo"].close()

    elif info["platform"] == "esp32":
        from machine import Pin
        print("Cleaning up ESP32 resources...")

        if "led" in resources:
            resources["led"].init(Pin.IN)
        if "button" in resources:
            resources["button"].init(Pin.IN)
        if "servo" in resources:
            resources["servo"].deinit()  # release PWM


# ---------------------------
# Main entry point
# ---------------------------
def main():
    info = detect_platform()
    print("Platform:", info["platform"])
    print("System Name:", info["name"])
    print("Version:", info["version"])
    print("Details:", info["details"])

    resources = setup(info)

    try:
        loop(info, resources)
    finally:
        cleanup(info, resources)


if __name__ == "__main__":
    main()


