
// Created by Karthik P S (for Nymble)
// Contact: Karthikreddyr02@gmail.com

// code to recieve data from pc and mimic back to pc with speeds

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <stdio.h>
#include <stdbool.h>


#ifndef F_CPU
#define F_CPU 16000000UL // Define CPU frequency
#endif


#include <util/delay.h>
#define BAUD 2400
#define UBRR_VALUE ((F_CPU / (16UL * BAUD)) - 1)
#define TIMEOUT_MS 1000 // Timeout period in milliseconds
#define DELAY_2_SEC 500 // Delay in milliseconds

volatile uint16_t eeprom_address = 0; // Track EEPROM address
volatile uint16_t byte_count = 0;
volatile uint32_t elapsed_time_ms = 0;
volatile uint32_t last_receive_time_ms = 0;
volatile bool receiving = false;
volatile bool data_received = false; // Flag to indicate data has been received at least once

void uart_init() {
    UBRR0H = (UBRR_VALUE >> 8);
    UBRR0L = UBRR_VALUE;
    UCSR0B = (1 << RXEN0) | (1 << TXEN0) | (1 << RXCIE0);
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void uart_send(char data) {
    while (!(UCSR0A & (1 << UDRE0)));
    UDR0 = data;
}

void uart_send_string(const char *str) {
    while (*str) {
        uart_send(*str++);
    }
}

ISR(USART_RX_vect) {
    char data = UDR0;

    // Store received data in EEPROM
    if (eeprom_address < 1000) {
        eeprom_update_byte((uint8_t*)eeprom_address++, data);
    }

    byte_count++;
    receiving = true;
    data_received = true; // Set flag to indicate data has been received
    last_receive_time_ms = elapsed_time_ms; // Update last receive time
}

ISR(TIMER1_COMPA_vect) {
    elapsed_time_ms += 1000; // 1-second interval

    if (receiving) {
        uint32_t bits_per_sec = (byte_count * 8);
        byte_count = 0;
        elapsed_time_ms = 0;

        // Transmit speed for debugging
        char buffer[32];
        sprintf(buffer, "Speed: %lu bps\n", bits_per_sec);
        uart_send_string(buffer);
        receiving = false;
    }
}

void timer_init() {
    TCCR1B = (1 << WGM12) | (1 << CS12) | (1 << CS10); // CTC mode, prescaler 1024
    OCR1A = F_CPU / 1024 - 1; // 1-second interval
    TIMSK1 = (1 << OCIE1A);
}

void clear_eeprom() {
    for (uint16_t i = 0; i < 1000; i++) {
        eeprom_update_byte((uint8_t*)i, 0xFF); // Clear EEPROM data
    }
}

int main() {
    uart_init();
    timer_init();
    sei(); // Enable global interrupts

    clear_eeprom(); // Ensure EEPROM is cleared initially
    uart_send_string("Ready to receive\n");

    while (1) {
        // Check if no data has been received for the timeout period
        if (data_received && (elapsed_time_ms - last_receive_time_ms) > TIMEOUT_MS && !receiving) {

            _delay_ms(DELAY_2_SEC);
            
            // Add null terminator at the end of received data
            eeprom_update_byte((uint8_t*)eeprom_address, '\0');

            // Send data from EEPROM
            for (uint16_t i = 0; i < 1000; i++) {
                char data = eeprom_read_byte((uint8_t*)i);
                if (data == '\0' || data == 0xFF) break; // Stop at null terminator or uninitialized data
                uart_send(data);
            }

            // Clear EEPROM after sending back data
            clear_eeprom();

            // Reset state
            eeprom_address = 0; // Reset EEPROM address
            data_received = false; // Ensure EEPROM read-and-send does not happen again until new data is received
            last_receive_time_ms = elapsed_time_ms;
        }
    }

    return 0;
}
