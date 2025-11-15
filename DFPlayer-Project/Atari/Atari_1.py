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
'''
# Map function: Re-maps a number from one range to another.
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
# Map function: Re-maps a number from one range to another.
'''
def map_value(value, in_min, in_max, out_min, out_max):
    """
    Maps an input value from one range to an output range.
    """
    # Use your observed maximum (e.g., 3035) instead of 4095
    input_max_observed = 3035 
    
    return (value - in_min) * (out_max - out_min) / (input_max_observed - in_min) + out_min

# The get_frequency_from_pot function already calls map_value,
# so the updated mapping will automatically be used there.

def get_frequency_from_pot(adc_value, base_freq, range_hz):
    # Simple linear mapping for pitch
    min_freq = max(50, base_freq - range_hz / 2)
    max_freq = base_freq + range_hz / 2
    frequency = map_value(adc_value, 0, 4095, min_freq, max_freq)
    return frequency

def main():
    print("Potentiometer controlled Atari Synth running.")
    print("Rotate potentiometers to change pitch.")
    
    # Define a threshold for "off" or "minimum volume"
    # An ADC value below this threshold will be considered silent/inactive.
    OFF_THRESHOLD = 150 # Increased from 50 for clearer selection

    while True:
        # Read raw ADC values
        val_mid = adc_mid.read_u16()
        val_low = adc_low.read_u16()

        # Calculate frequencies (calculations remain the same)
        freq_mid = get_frequency_from_pot(val_mid, 261.63, 200)
        freq_low = get_frequency_from_pot(val_low, 130.81, 100)

        # --- REVISED LOGIC ---
        # If the midrange pot is turned up past the threshold, use its frequency.
        if val_mid > OFF_THRESHOLD:
            current_freq = freq_mid
            current_duty = 512
        # Otherwise, if the low range pot is turned up past the threshold, use its frequency.
        elif val_low > OFF_THRESHOLD:
            current_freq = freq_low
            current_duty = 512
        # If neither is turned up, silence the output.
        else:
            current_freq = 0 # Set frequency to 0 or a safe default
            current_duty = 0 # Set duty cycle to 0 for silence
        # --- END REVISED LOGIC ---

        # Update the PWM frequency and duty cycle
        if current_duty > 0:
            pwm.freq(int(current_freq))
            pwm.duty(current_duty) 
        else:
            pwm.duty(0) # Silence the output

        # Optional: Print values for debugging in the shell
        print(f"Mid: {val_mid}, Freq: {freq_mid:.2f}Hz | Low: {val_low}, Freq: {freq_low:.2f}Hz | Active Freq: {current_freq:.2f}Hz", end='\r')
        
        time.sleep_ms(10) # Small delay for stability



'''
def main():
    print("Synth with Volume and LFO running.")
    
    # Variables for LFO
    lfo_counter = 0
    
    while True:
        # Read all potentiometer values
        val_mid = adc_mid.read_u16()
        val_low = adc_low.read_u16()
        val_volume = adc_volume.read_u16()
        val_lfo = adc_lfo.read_u16()

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
'''
if __name__ == "__main__":
    main()