'''


'''
from machine import Pin, PWM, ADC
import time
import math

# PWM output pin for the amplifier
pwm_pin = 27
pwm = PWM(Pin(pwm_pin), freq=440, duty=0)

# Potentiometer ADC pins
pot_mid_pin = 33
pot_low_pin = 36
pot_volume_pin = 39
pot_lfo_pin = 32

# Initialize ADCs
adc_mid = ADC(Pin(pot_mid_pin))
adc_low = ADC(Pin(pot_low_pin))
adc_volume = ADC(Pin(pot_volume_pin))
adc_lfo = ADC(Pin(pot_lfo_pin))

# Set attenuation for 0-3.3V range
adc_mid.atten(ADC.ATTN_11DB)
adc_low.atten(ADC.ATTN_11DB)
adc_volume.atten(ADC.ATTN_11DB)
adc_lfo.atten(ADC.ATTN_11DB)

# Map function: Re-maps a number from one range to another.
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_frequency_from_pot(adc_value, base_freq, range_hz):
    # Simple linear mapping for pitch
    min_freq = max(50, base_freq - range_hz / 2)
    max_freq = base_freq + range_hz / 2
    frequency = map_value(adc_value, 0, 4095, min_freq, max_freq)
    return frequency

def main():
    print("Synth with Volume and LFO running.")
    
    # Variables for LFO
    lfo_counter = 0
    
    while True:
        # Read all potentiometer values
        val_mid = adc_mid.read()
        val_low = adc_low.read()
        val_volume = adc_volume.read()
        val_lfo = adc_lfo.read()

        # 1. Determine base frequency
        current_freq = get_frequency_from_pot(val_mid if val_mid > 50 else val_low, 261.63, 200)

        # 2. Implement LFO for pitch modulation (vibrato effect)
        # Map LFO pot to LFO depth (e.g., 0Hz to 10Hz swing)
        lfo_depth = map_value(val_lfo, 0, 4095, 0, 10) 
        # Map LFO pot to LFO rate (e.g., 0.5Hz to 5Hz)
        lfo_rate = map_value(val_lfo, 0, 4095, 0.5, 5.0)

        # Generate a sine wave for the LFO signal
        # Use a counter to advance the sine wave phase
        lfo_signal = math.sin(lfo_counter * lfo_rate * 0.1) # 0.1 for scaling 
        modulated_freq = current_freq + (lfo_signal * lfo_depth)
        
        # Increment LFO counter
        lfo_counter = (lfo_counter + 1) % 628 # Reset counter to avoid overflow (~2*pi*100)

        # 3. Control volume with the volume potentiometer
        # Map ADC value (0-4095) to PWM duty cycle (0-1023 or 0-65535 depending on bit depth)
        # Using 10-bit range for simplicity: 0-1023
        volume_level = int(map_value(val_volume, 0, 4095, 0, 1023))

        # Update the PWM output
        if modulated_freq > 50 and volume_level > 20: # Only play if frequency and volume are reasonable
            pwm.freq(int(modulated_freq))
            pwm.duty(volume_level) # Use volume pot value for duty cycle
        else:
            pwm.duty(0)

        time.sleep_ms(10) # Adjust this delay for smoother LFO modulation

if __name__ == "__main__":
    main()
