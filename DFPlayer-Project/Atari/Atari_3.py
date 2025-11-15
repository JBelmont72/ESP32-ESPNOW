'''
this works very well with the 3.3 volt setup    
the LFO seems choppy but it works okay

'''
from machine import Pin, PWM, ADC
import time
import math

# PWM output pin for the amplifier
pwm_pin = 27
pwm = PWM(Pin(pwm_pin), freq=440, duty=0)

# Potentiometer ADC pins (using your current pin assignments)
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
    OFF_THRESHOLD = 150 # ADC value below this is considered "off"

    while True:
        # Read all potentiometer values
        val_mid = adc_mid.read()
        val_low = adc_low.read()
        val_volume = adc_volume.read()
        val_lfo = adc_lfo.read()

        # 1. Determine base frequency using the selector logic
        if val_mid > OFF_THRESHOLD:
            current_freq = get_frequency_from_pot(val_mid, 261.63, 200)
        elif val_low > OFF_THRESHOLD:
            current_freq = get_frequency_from_pot(val_low, 130.81, 100)
        else:
            current_freq = 0 # Silence

        # 2. Implement LFO for pitch modulation (vibrato effect)
        # Only apply LFO if the LFO pot is turned up
        if val_lfo > OFF_THRESHOLD:
            lfo_depth = map_value(val_lfo, OFF_THRESHOLD, 4095, 0, 10) 
            lfo_rate = map_value(val_lfo, OFF_THRESHOLD, 4095, 0.5, 5.0)

            lfo_signal = math.sin(lfo_counter * lfo_rate * 0.1)
            modulated_freq = current_freq + (lfo_signal * lfo_depth)
            lfo_counter = (lfo_counter + 1) % 628
        else:
            modulated_freq = current_freq
            lfo_counter = 0 # Reset counter if LFO is off

        # 3. Control volume
        # Ensure volume mapping starts from 0 when pot is low
        if val_volume > 50:
             volume_level = int(map_value(val_volume, 50, 4095, 100, 1023))
        else:
             volume_level = 0


        # Update the PWM output
        if modulated_freq > 50 and volume_level > 0:
            pwm.freq(int(modulated_freq))
            pwm.duty(volume_level) # Use volume pot value for duty cycle
        else:
            pwm.duty(0)
        print(f"Mid: {val_mid}, Low: {val_low}, Freq: {modulated_freq:.2f}Hz, Volume: {volume_level}", end='\r')
        time.sleep_ms(10)

if __name__ == "__main__":
    main()
