# class placeholder for non-raspi development devices
import RPi.GPIO as gpio
# from include.fake_gpio import gpio
import time

from include.input_controls import InputControls
from include.system_class import MainSystem

from include.dispenser import PaperDispenser

# Configure this file based on testing the stepper motors with the mechanisms
# especially the number of steps for each movement from each motor
from include.config import a4_step_motors, long_step_motors


# Define GPIO pin connected to the coin acceptor's pulse output
coin_acceptor_pulse_pin = 17 

# Set up GPIO
gpio.setmode(gpio.BCM)
gpio.setup(coin_acceptor_pulse_pin, gpio.IN, pull_up_down=gpio.PUD_UP)

pulse_count = 0
coin_value = 0

def count_pulse(channel):
    """Callback function for each pulse received."""
    global pulse_count
    pulse_count += 1

# Attach the callback function to the rising edge of the pulse
#gpio.add_event_detect(coin_acceptor_pulse_pin, gpio.RISING, callback=count_pulse, bouncetime=200) 

def main():
    # Initialize components
    a4_dispenser = PaperDispenser(a4_step_motors['stepper_one'], a4_step_motors['stepper_two'])
    long_dispenser = PaperDispenser(long_step_motors['stepper_one'], long_step_motors['stepper_two'])

    # Initialize main System
    system = MainSystem()

    # Override buttons
    # InputControls(system)

    # Runs repeatedly
    def check_coin_slot_interrupt():
        global pulse_count
        if system.active_view == 'main_frame':
            if pulse_count > 0:
                # Determine coin value based on pulse count
                if pulse_count == 1:
                    coin_value = 1  # 1 Peso
                elif pulse_count == 5:
                    coin_value = 5  # 5 Pesos
                elif pulse_count == 10:
                    coin_value = 10  # 10 Pesos
                else:
                    coin_value = 0  # Unknown coin
                print(f"Coin Inserted: {coin_value} Pesos")

                # Add logic here to handle the coin insertion 
                # (e.g., update a counter, dispense a product, etc.)

                system.amount_given_var.set(system.amount_given_var.get() + coin_value)
                pulse_count = 0  # Reset pulse count for the next coin
        system.after(10, check_coin_slot_interrupt)

    system.customInit()
    check_coin_slot_interrupt()
    system.mainloop()

if __name__ == "__main__":
    main()