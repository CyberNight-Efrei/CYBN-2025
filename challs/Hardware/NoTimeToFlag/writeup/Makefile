# Compiler and tools
CC       = avr-gcc
OBJCOPY  = avr-objcopy
AVRDUDE  = avrdude

# ---- Writeup target for ATmega328p ----
writeup: wu.hex
	@echo "[*] Uploading wu.hex to ATmega328p"
	$(AVRDUDE) -c arduino -p m328p -P /dev/ttyUSB0 -b 115200 -U flash:w:$<

wu.elf: wu.c
	@echo "[*] Building wu.elf for ATmega328p"
	$(CC) -mmcu=atmega328p -Os -o $@ $<

wu.hex: wu.elf
	@echo "[*] Generating wu.hex"
	$(OBJCOPY) -O ihex $< $@

clean:
	rm -f wu.elf wu.hex
