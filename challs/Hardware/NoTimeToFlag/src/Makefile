# Compiler and tools
CC       = avr-gcc
OBJCOPY  = avr-objcopy
AVRDUDE  = avrdude

# MCU and programmer settings
MCU      = attiny85
PROGRAMMER = avrisp
PORT     = /dev/ttyACM0
BAUD     = 19200

# Project files
TARGET   = main
SRC      = main.c serial.c

# Flags
CFLAGS   = -mmcu=$(MCU) -Os

all: $(TARGET).hex

$(TARGET).elf: $(SRC)
	@echo "[*] Building ELF"
	$(CC) $(CFLAGS) -o $@ $^

$(TARGET).hex: $(TARGET).elf
	@echo "[*] Generating HEX"
	$(OBJCOPY) -O ihex $< $@

upload: $(TARGET).hex
	@echo "[*] Uploading to device"
	$(AVRDUDE) -p t85 -P $(PORT) -c $(PROGRAMMER) -b $(BAUD) -U flash:w:$<

clean:
	rm -f $(TARGET).elf $(TARGET).hex
