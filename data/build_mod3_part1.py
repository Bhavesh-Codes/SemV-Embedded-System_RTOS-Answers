# build_mod3_part1.py: Topic 3.1 Input Devices (using non-fstring templates)

def get_topic_3_1(svg_analog_input_block, svg_digital_input_block, svg_keyboard_matrix, svg_adc0808):
    q1_html = """
<h3>1. Interfacing of Analog and Digital Input Devices</h3>

<div class="definition-box">
  <strong>Definition of Interfacing:</strong> Interfacing is the hardware and software process of connecting an external device (sensor, switch, or transducer) to a microcontroller (such as Arduino, ESP32, 8051, or ARM Cortex) so that the processor can receive physical information, interpret logic or voltage states, process the data, and perform deterministic control actions.
</div>

<p>An embedded system continuously interacts with the physical external environment through input devices. Input devices collect physical phenomena (light, heat, pressure, physical contact) and translate them into electrical signals. Depending on the electrical nature of the generated signal, input devices are classified into two broad categories:</p>
<ol>
  <li><strong>Analog Input Devices:</strong> Produce continuously varying physical voltages or currents over time.</li>
  <li><strong>Digital Input Devices:</strong> Produce discrete two-state binary electrical signals (Logic 0 or Logic 1).</li>
</ol>

<hr/>

<h4>A. Interfacing Analog Input Devices</h4>
<p>Analog input devices convert continuous physical quantities into an electrical voltage that varies proportionately. Because digital microcontrollers cannot directly interpret continuous analog voltages, an <strong>Analog-to-Digital Converter (ADC)</strong> is required to sample, quantize, and digitize the signal into binary values.</p>

__SVG_ANALOG_INPUT_BLOCK__

<h5>Key Examples of Analog Input Devices (from Class Notes):</h5>
<ul>
  <li><strong>LDR (Light Dependent Resistor / Photoresistor):</strong>
    <ul>
      <li><em>Working:</em> Cadmium Sulfide (CdS) photoconductive cell whose electrical resistance decreases non-linearly with increasing incident light intensity. In darkness, resistance is in the megaohm range (>1 MΩ); under bright light, it drops to a few hundred ohms.</li>
      <li><em>Interfacing Circuit:</em> Arranged in a voltage divider network with a fixed pull-down resistor $R_{fixed}$ (typically 10 kΩ). The output voltage $V_{out} = V_{CC} \times \frac{R_{fixed}}{R_{LDR} + R_{fixed}}$ is fed directly to an ADC channel.</li>
      <li><em>Primary Application:</em> Automatic streetlight controllers, dusk-to-dawn security illuminators, solar panel sun-tracking systems.</li>
    </ul>
  </li>
  <li><strong>Analog Temperature Sensor (e.g. LM35 / Thermistor):</strong>
    <ul>
      <li><em>Working:</em> Precision integrated-circuit temperature sensor whose output voltage is linearly proportional to the Celsius temperature ($10\text{ mV/}^\circ\text{C}$ scale factor). At $25^\circ\text{C}$, $V_{out} = 250\text{ mV}$; at $100^\circ\text{C}$, $V_{out} = 1000\text{ mV} = 1.0\text{V}$.</li>
      <li><em>Interfacing:</em> Output pin connects directly to an ADC input pin with a decoupling capacitor (0.1 µF) to bypass high-frequency line noise.</li>
      <li><em>Application:</em> HVAC temperature regulation, battery pack thermal runaway safety cutoff, industrial process cooling.</li>
    </ul>
  </li>
  <li><strong>Potentiometer (Rotary / Slider):</strong>
    <ul>
      <li><em>Working:</em> Three-terminal variable resistor forming an adjustable voltage divider. As the wiper rotates between terminal 1 ($V_{CC}$) and terminal 3 (GND), terminal 2 outputs a continuous linear DC voltage between $0\text{V}$ and $V_{CC}$.</li>
      <li><em>Application:</em> User-controlled setpoints, audio volume dials, motor speed control references, robotic joint angular position sensing.</li>
    </ul>
  </li>
</ul>

<div class="formula-block">
  <strong>Role and Mathematical Quantization of ADC:</strong><br/>
  An ADC converts an instantaneous analog voltage $V_{in}$ into an $N$-bit integer binary code:
  $$\text{Digital Code} = \left\lfloor \frac{V_{in} - V_{ref(-)}}{V_{ref(+)} - V_{ref(-)}} \times (2^N - 1) \right\rfloor$$
  For an Arduino Uno with an integrated 10-bit Successive Approximation ADC ($N = 10$, $2^{10} = 1024$ levels from 0 to 1023) operating with $V_{ref} = 5.0\text{V}$:
  $$\text{Resolution (Step Size)} = \frac{5.0\text{V}}{1024} = 4.8828\text{ mV per LSB count}$$
  If an LDR divider produces $2.5\text{V}$, the microcontroller reads: $\text{ADC Code} = \frac{2.5\text{V}}{0.004883\text{V}} = 512$.
</div>

<hr/>

<h4>B. Interfacing Digital Input Devices</h4>
<p>Digital input devices provide discrete binary signals—either a logic HIGH (nominally $V_{CC}$, e.g. 5V or 3.3V) or logic LOW (nominally GND, 0V). They connect directly to standard General Purpose Input/Output (GPIO) pins configured as inputs.</p>

__SVG_DIGITAL_INPUT_BLOCK__

<h5>Key Examples of Digital Input Devices (from Class Notes):</h5>
<ul>
  <li><strong>Push Button / Tact Switch:</strong>
    <ul>
      <li><em>Working:</em> A momentary mechanical contact switch. When pressed, internal metal contacts close; when released, spring action opens them.</li>
      <li><em>Interfacing:</em> Requires a pull-up resistor (typically 10 kΩ to $V_{CC}$) so that the unpressed line remains solidly at logic HIGH (1). When pressed, the line is tied to GND (logic 0). Software or hardware RC debouncing is necessary to suppress mechanical bounce spikes (10–20 ms duration).</li>
      <li><em>Application:</em> Reset switches, emergency stop buttons, user input keys, trigger switches.</li>
    </ul>
  </li>
  <li><strong>PIR (Passive Infrared) Motion Sensor:</strong>
    <ul>
      <li><em>Working:</em> Pyroelectric sensor with a segmented Fresnel lens that detects changes in infrared radiation emitted by warm bodies (human or animal, wavelength ~9.4 µm) moving across detection zones.</li>
      <li><em>Output:</em> On-board BISS0001 processing IC outputs a clean digital pulse: HIGH (3.3V) when motion is detected, and LOW (0V) when idle.</li>
      <li><em>Application:</em> Burglar alarm systems, automatic motion-activated stairwell lights, occupancy-based HVAC power savers.</li>
    </ul>
  </li>
  <li><strong>IR Obstacle Sensor:</strong>
    <ul>
      <li><em>Working:</em> Consists of an infrared emitter diode and an IR photodiode/phototransistor receiver. When an obstacle is within reflective range, the reflected IR beam is sensed, and an on-board LM393 voltage comparator trips, producing a clean digital LOW (active-low) or HIGH output.</li>
      <li><em>Application:</em> Obstacle-avoiding robotic vehicles, conveyor product counters, contactless touchless sanitary dispensers.</li>
    </ul>
  </li>
</ul>

<hr/>

<h4>C. Comprehensive Comparison: Analog vs. Digital Input Devices</h4>
<table class="comparison-table">
  <thead>
    <tr>
      <th>Comparison Parameter</th>
      <th>Analog Input Devices</th>
      <th>Digital Input Devices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Signal Representation</strong></td>
      <td>Continuously varying voltage or current over time ($0\text{V}$ to $V_{CC}$).</td>
      <td>Discrete two-state binary levels (Logic 0 / Logic 1).</td>
    </tr>
    <tr>
      <td><strong>Processing Hardware</strong></td>
      <td>Requires an Analog-to-Digital Converter (ADC), reference voltage, and sample-and-hold circuit.</td>
      <td>Connects directly to MCU digital GPIO pins via internal Schmidt triggers / input buffers.</td>
    </tr>
    <tr>
      <td><strong>Noise Immunity</strong></td>
      <td>Low. Susceptible to electromagnetic interference, power rail ripple, and thermal noise. Requires filtering.</td>
      <td>High. Inherent noise margin prevents minor noise fluctuations from toggling logic state.</td>
    </tr>
    <tr>
      <td><strong>Interfacing Circuitry</strong></td>
      <td>Voltage dividers, operational amplifiers, anti-aliasing low-pass filters, instrumentation amps.</td>
      <td>Pull-up / pull-down resistors, mechanical debounce circuits (RC or software timer), level shifters.</td>
    </tr>
    <tr>
      <td><strong>MCU Resource Usage</strong></td>
      <td>Consumes dedicated ADC channels, requires conversion delay time ($T_{conv}$).</td>
      <td>Consumes standard digital GPIO pins; can trigger hardware external interrupts (INT0, INT1).</td>
    </tr>
    <tr>
      <td><strong>Prominent Examples</strong></td>
      <td>LDR, LM35 temperature sensor, potentiometer, strain gauge, soil moisture sensor.</td>
      <td>Push button switch, PIR motion sensor, IR obstacle sensor, limit switch, optical encoder.</td>
    </tr>
    <tr>
      <td><strong>Typical Applications</strong></td>
      <td>Continuous environmental monitoring, analog telemetry, light measurement, audio capture.</td>
      <td>Event detection, user push-buttons, safety interlocks, object counting, presence alarms.</td>
    </tr>
  </tbody>
</table>

<hr/>

<h4>D. Systematic 6-Step Interfacing Procedure (from Course Guidelines):</h4>
<ol>
  <li><strong>Device Classification:</strong> Determine whether the device is an input or output transducer, and identify whether its output signal is continuous analog or discrete digital.</li>
  <li><strong>Electrical Specification Check:</strong> Review the device datasheet for operating voltage ($V_{CC}$: 3.3V vs 5V), current draw ($I_{max}$), output impedance, and logic threshold standards.</li>
  <li><strong>Pin Allocation &amp; Circuit Wiring:</strong> Connect analog sensors to MCU ADC channels (e.g., A0–A5 on Arduino) and digital sensors to standard GPIOs. Ensure appropriate pull-up/pull-down resistors or voltage dividers are inserted.</li>
  <li><strong>Common Ground Reference:</strong> Always interconnect the ground (GND) terminals of the sensor, driver circuit, and microcontroller to establish a unified reference potential.</li>
  <li><strong>Firmware Development:</strong> Initialize GPIO direction registers (<code>pinMode()</code> as <code>INPUT</code> or <code>INPUT_PULLUP</code>) or configure ADC registers (prescaler, reference voltage, channel selection). Write acquisition routines with debouncing or analog averaging.</li>
  <li><strong>Verification &amp; Calibration:</strong> Upload firmware, observe readings over serial monitor / oscilloscope, and apply mathematical scaling formulas (e.g. converting raw ADC code into $^\circ\text{C}$ or Lux).</li>
</ol>
"""
    q1_html = q1_html.replace("__SVG_ANALOG_INPUT_BLOCK__", svg_analog_input_block)
    q1_html = q1_html.replace("__SVG_DIGITAL_INPUT_BLOCK__", svg_digital_input_block)

    q2_html = """
<h3>2. 4×4 Keyboard Matrix Interfacing and Hex Code Generation</h3>

<p class="not-found">Note: Found as primary syllabus requirement and university exam question (x1). The provided lecture slides focus on basic push-button interfacing; this comprehensive section provides the full 8-mark standard university curriculum answer, circuit diagram, scanning algorithm, and hex code conversion program.</p>

<div class="definition-box">
  <strong>Concept of Matrix Keyboards:</strong> A keyboard matrix arranges pushbutton switches in a two-dimensional grid of rows and columns. While connecting 16 independent switches individually requires 16 separate microcontroller I/O pins, a <strong>4×4 matrix keyboard requires only 8 pins (4 row outputs + 4 column inputs)</strong>, saving 50% of the microcontroller's valuable GPIO resources.
</div>

<h4>A. Hardware Interfacing &amp; Circuit Architecture</h4>
<p>In a 4×4 matrix keypad:</p>
<ul>
  <li><strong>Row Lines ($R_0, R_1, R_2, R_3$):</strong> Connected to 4 microcontroller output pins (e.g., Port 1 pins P1.0 to P1.3).</li>
  <li><strong>Column Lines ($C_0, C_1, C_2, C_3$):</strong> Connected to 4 microcontroller input pins (e.g., Port 1 pins P1.4 to P1.7).</li>
  <li><strong>Pull-Up Resistors:</strong> Each column line is pulled up to $+5\text{V}$ through a 10 kΩ resistor (or internal MCU weak pull-ups). Thus, when no key is pressed, all column lines read logic <strong>HIGH (1111b)</strong>.</li>
  <li><strong>Key Switches:</strong> Each momentary tactile switch sits at the intersection of a row and a column. Pressing a key mechanically bridges that specific row and column line.</li>
</ul>

__SVG_KEYBOARD_MATRIX__

<hr/>

<h4>B. Key Detection &amp; Scanning Algorithm (Step-by-Step)</h4>
<p>The microcontroller executes a continuous matrix scanning sequence:</p>
<ol>
  <li><strong>Step 1: Check if ANY Key is Pressed:</strong>
    <ul>
      <li>Drive all Row lines LOW ($R_0 = R_1 = R_2 = R_3 = 0$).</li>
      <li>Read the Column lines ($C_0 - C_3$).</li>
      <li>If all columns read HIGH ($1111\text{b}$ or <code>0x0F</code>), no key is pressed. The processor continues other tasks or loops.</li>
      <li>If any column reads LOW (not $1111\text{b}$), at least one key is currently pressed! Proceed to Step 2.</li>
    </ul>
  </li>
  <li><strong>Step 2: Debounce the Key:</strong>
    <ul>
      <li>Mechanical contacts bounce for 10 ms to 20 ms, generating false rapid transitions.</li>
      <li>The MCU pauses for a software delay of 20 ms and re-reads the columns. If still LOW, the key closure is genuine.</li>
    </ul>
  </li>
  <li><strong>Step 3: Identify Key by Row-by-Row Scanning:</strong>
    <ul>
      <li>Drive <strong>Row 0 LOW</strong>, and all other rows HIGH ($R = 1110\text{b}$). Read Columns. If any column is LOW, the key is in Row 0! Note the column number.</li>
      <li>If no column is LOW, drive <strong>Row 1 LOW</strong> ($R = 1101\text{b}$). Read Columns. If any column is LOW, the key is in Row 1.</li>
      <li>If still not found, drive <strong>Row 2 LOW</strong> ($R = 1011\text{b}$). Read Columns.</li>
      <li>If still not found, drive <strong>Row 3 LOW</strong> ($R = 0111\text{b}$). Read Columns.</li>
    </ul>
  </li>
  <li><strong>Step 4: Decode to Hexadecimal Value:</strong>
    <ul>
      <li>Using the identified Row index ($0..3$) and Column index ($0..3$), lookup the corresponding ASCII/Hexadecimal character from a pre-defined 4×4 lookup matrix.</li>
    </ul>
  </li>
  <li><strong>Step 5: Wait for Key Release:</strong>
    <ul>
      <li>Drive all rows LOW again and loop until all columns return to HIGH ($1111\text{b}$). This prevents repeated firing of the same key press.</li>
    </ul>
  </li>
</ol>

<hr/>

<h4>C. Hexadecimal Keypad Encoding Table</h4>
<table class="comparison-table">
  <thead>
    <tr>
      <th>Row Driven LOW</th>
      <th>Column 0 (LOW)</th>
      <th>Column 1 (LOW)</th>
      <th>Column 2 (LOW)</th>
      <th>Column 3 (LOW)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Row 0 (P1.0 = 0)</strong></td>
      <td>Key '1' (Hex <code>0x01</code>)</td>
      <td>Key '2' (Hex <code>0x02</code>)</td>
      <td>Key '3' (Hex <code>0x03</code>)</td>
      <td>Key 'A' (Hex <code>0x0A</code>)</td>
    </tr>
    <tr>
      <td><strong>Row 1 (P1.1 = 0)</strong></td>
      <td>Key '4' (Hex <code>0x04</code>)</td>
      <td>Key '5' (Hex <code>0x05</code>)</td>
      <td>Key '6' (Hex <code>0x06</code>)</td>
      <td>Key 'B' (Hex <code>0x0B</code>)</td>
    </tr>
    <tr>
      <td><strong>Row 2 (P1.2 = 0)</strong></td>
      <td>Key '7' (Hex <code>0x07</code>)</td>
      <td>Key '8' (Hex <code>0x08</code>)</td>
      <td>Key '9' (Hex <code>0x09</code>)</td>
      <td>Key 'C' (Hex <code>0x0C</code>)</td>
    </tr>
    <tr>
      <td><strong>Row 3 (P1.3 = 0)</strong></td>
      <td>Key '*' (Hex <code>0x0E</code>)</td>
      <td>Key '0' (Hex <code>0x00</code>)</td>
      <td>Key '#' (Hex <code>0x0F</code>)</td>
      <td>Key 'D' (Hex <code>0x0D</code>)</td>
    </tr>
  </tbody>
</table>

<hr/>

<h4>D. Complete Embedded C Program (8051 / Arduino Architecture)</h4>
<pre><code>#include &lt;reg51.h&gt;  // Standard 8051 register definitions

#define KEYPAD_PORT P1  // P1.0-P1.3 = Rows (Out), P1.4-P1.7 = Cols (In)

// 4x4 Keypad Hex Lookup Table
const unsigned char hex_lookup[4][4] = {
    {0x01, 0x02, 0x03, 0x0A},  // Row 0: 1, 2, 3, A
    {0x04, 0x05, 0x06, 0x0B},  // Row 1: 4, 5, 6, B
    {0x07, 0x08, 0x09, 0x0C},  // Row 2: 7, 8, 9, C
    {0x0E, 0x00, 0x0F, 0x0D}   // Row 3: *, 0, #, D
};

// Software Debounce Delay (~20ms at 11.0592 MHz)
void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for(i = 0; i &lt; ms; i++)
        for(j = 0; j &lt; 120; j++);
}

// Keypad Scanner Function: Returns Hex value of pressed key
unsigned char get_key(void) {
    unsigned char row, col, col_val;
    unsigned char row_masks[4] = {0x0E, 0x0D, 0x0B, 0x07}; // Ground one row at a time

    while(1) {
        // Step 1: Detect if ANY key is pressed (ground all rows)
        KEYPAD_PORT = 0xF0;  // P1.0-P1.3 = 0 (Rows LOW), P1.4-P1.7 = 1 (Cols pulled-up)
        col_val = (KEYPAD_PORT &amp; 0xF0);
        if(col_val == 0xF0)
            continue; // No key pressed, keep polling

        // Step 2: Debounce key press
        delay_ms(20);
        col_val = (KEYPAD_PORT &amp; 0xF0);
        if(col_val == 0xF0)
            continue; // False trigger / bounce

        // Step 3: Scan row by row to identify specific key
        for(row = 0; row &lt; 4; row++) {
            // Ground specific row, set columns as inputs (HIGH)
            KEYPAD_PORT = (0xF0 | row_masks[row]);
            col_val = (KEYPAD_PORT &amp; 0xF0);

            if(col_val != 0xF0) {
                // Found active column!
                if(col_val == 0xE0)      col = 0; // Col 0 is LOW (1110 0000b)
                else if(col_val == 0xD0) col = 1; // Col 1 is LOW (1101 0000b)
                else if(col_val == 0xB0) col = 2; // Col 2 is LOW (1011 0000b)
                else if(col_val == 0x70) col = 3; // Col 3 is LOW (0111 0000b)
                else continue;

                // Step 4: Wait for Key Release (Debounce release)
                KEYPAD_PORT = 0xF0;
                while((KEYPAD_PORT &amp; 0xF0) != 0xF0);
                delay_ms(20);

                // Step 5: Return decoded Hex byte
                return hex_lookup[row][col];
            }
        }
    }
}

void main(void) {
    unsigned char key_val;
    while(1) {
        key_val = get_key(); // Blocks until key is pressed &amp; decoded
        P2 = key_val;        // Output hex value to Port 2 LEDs / Display
    }
}
</code></pre>
"""
    q2_html = q2_html.replace("__SVG_KEYBOARD_MATRIX__", svg_keyboard_matrix)

    q3_html = """
<h3>3. Functional Pin Diagram and Architecture of ADC 0808</h3>

<p class="not-found">Note: Primary syllabus topic and frequent university examination question (x1). Lecture slides mention the role of ADC and Arduino 10-bit ADC; this section details the full monolithic ADC 0808 integrated circuit pin diagram, internal architecture, and interfacing sequence as required for full marks.</p>

<div class="definition-box">
  <strong>Overview of ADC 0808:</strong> The ADC0808 is an industry-standard 8-bit monolithic CMOS analog-to-digital converter fabricated with an integrated 8-channel analog multiplexer, an on-chip Successive Approximation Register (SAR) ADC core, and microprocessor-compatible tri-state output latches. It provides high speed, high accuracy, and minimal power consumption without requiring external zero or full-scale trims.
</div>

<h4>A. Key Specifications of ADC 0808:</h4>
<ul>
  <li><strong>Resolution:</strong> 8 bits ($2^8 = 256$ discrete digital quantization levels).</li>
  <li><strong>Number of Analog Channels:</strong> 8 single-ended multiplexed inputs ($\text{IN}_0$ to $\text{IN}_7$).</li>
  <li><strong>Conversion Principle:</strong> Successive Approximation Register (SAR).</li>
  <li><strong>Conversion Time:</strong> ~100 µs at a clock frequency of 640 kHz.</li>
  <li><strong>Supply Voltage:</strong> Single $+5\text{V DC}$ supply ($V_{CC} = +5\text{V}$).</li>
  <li><strong>Power Dissipation:</strong> Very low, approximately 15 mW.</li>
  <li><strong>Linearity Error:</strong> $\pm \frac{1}{2} \text{ LSB}$ (unadjusted error $\pm 1 \text{ LSB}$).</li>
</ul>

<hr/>

<h4>B. Functional Pin Diagram (28-Pin Dual In-Line Package)</h4>
__SVG_ADC0808__

<hr/>

<h4>C. Comprehensive Pin Function Description (All 28 Pins)</h4>
<table class="comparison-table">
  <thead>
    <tr>
      <th>Pin Number</th>
      <th>Pin Name</th>
      <th>Signal Type</th>
      <th>Functional Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1 to 5</strong></td>
      <td>IN3, IN4, IN5, IN6, IN7</td>
      <td>Analog Input</td>
      <td>Multiplexed analog input channels 3 through 7. Accepts input voltages in the range $V_{ref(-)} \le V_{in} \le V_{ref(+)}$.</td>
    </tr>
    <tr>
      <td><strong>6</strong></td>
      <td>START</td>
      <td>Digital Input</td>
      <td><strong>Start of Conversion Pulse.</strong> A positive-going pulse (active HIGH, min width 100 ns) resets the internal SAR. Conversion officially begins on the falling edge of this pulse.</td>
    </tr>
    <tr>
      <td><strong>7</strong></td>
      <td>EOC</td>
      <td>Digital Output</td>
      <td><strong>End of Conversion.</strong> Goes LOW when conversion begins, and transitions to logic HIGH when 8-bit conversion is complete. Connected to MCU interrupt or polling pin.</td>
    </tr>
    <tr>
      <td><strong>8</strong></td>
      <td>$2^{-4}$ (D3)</td>
      <td>Digital Output</td>
      <td>Bit 3 of the 8-bit digital output byte. Tri-state output.</td>
    </tr>
    <tr>
      <td><strong>9</strong></td>
      <td>OE</td>
      <td>Digital Input</td>
      <td><strong>Output Enable.</strong> Active HIGH signal. When asserted HIGH, it enables the internal tri-state output latches, placing the conversion byte onto data lines D0–D7.</td>
    </tr>
    <tr>
      <td><strong>10</strong></td>
      <td>CLK</td>
      <td>Digital Input</td>
      <td><strong>External Clock Input.</strong> Typically clocked between 10 kHz and 1280 kHz (nominal 640 kHz, requiring ~64 clock cycles per SAR conversion).</td>
    </tr>
    <tr>
      <td><strong>11</strong></td>
      <td>$V_{CC}$</td>
      <td>Power Supply</td>
      <td>Positive power supply input: $+5.0\text{V DC} \pm 5\%$.</td>
    </tr>
    <tr>
      <td><strong>12</strong></td>
      <td>$V_{ref(+)}$</td>
      <td>Reference Input</td>
      <td>Positive reference voltage. Sets the full-scale analog input voltage span (typically connected to $+5.0\text{V}$).</td>
    </tr>
    <tr>
      <td><strong>13</strong></td>
      <td>GND</td>
      <td>Power Supply</td>
      <td>System Ground reference ($0\text{V}$).</td>
    </tr>
    <tr>
      <td><strong>14</strong></td>
      <td>$2^{-6}$ (D1)</td>
      <td>Digital Output</td>
      <td>Bit 1 of digital output byte.</td>
    </tr>
    <tr>
      <td><strong>15</strong></td>
      <td>$2^{-8}$ (D0 / LSB)</td>
      <td>Digital Output</td>
      <td><strong>Least Significant Bit (LSB)</strong> of the 8-bit digital output.</td>
    </tr>
    <tr>
      <td><strong>16</strong></td>
      <td>$V_{ref(-)}$</td>
      <td>Reference Input</td>
      <td>Negative reference voltage. Sets the zero-scale analog input voltage (typically connected to GND, $0\text{V}$).</td>
    </tr>
    <tr>
      <td><strong>17 to 20</strong></td>
      <td>D2, D4, D5, D6</td>
      <td>Digital Output</td>
      <td>Bits 2, 4, 5, and 6 of digital output byte.</td>
    </tr>
    <tr>
      <td><strong>21</strong></td>
      <td>$2^{-1}$ (D7 / MSB)</td>
      <td>Digital Output</td>
      <td><strong>Most Significant Bit (MSB)</strong> of the 8-bit digital output.</td>
    </tr>
    <tr>
      <td><strong>22</strong></td>
      <td>ALE</td>
      <td>Digital Input</td>
      <td><strong>Address Latch Enable.</strong> A positive pulse latches the 3-bit channel address present on pins ADD A, ADD B, and ADD C into the internal address decoder register.</td>
    </tr>
    <tr>
      <td><strong>23, 24, 25</strong></td>
      <td>ADD C, ADD B, ADD A</td>
      <td>Digital Input</td>
      <td><strong>Channel Selection Address Lines.</strong> 3-bit binary address where ADD C is MSB and ADD A is LSB. Decodes to select one of 8 analog channels ($\text{IN}_0$–$\text{IN}_7$).</td>
    </tr>
    <tr>
      <td><strong>26 to 28</strong></td>
      <td>IN0, IN1, IN2</td>
      <td>Analog Input</td>
      <td>Multiplexed analog input channels 0, 1, and 2.</td>
    </tr>
  </tbody>
</table>

<hr/>

<h4>D. Channel Multiplexer Address Truth Table</h4>
<table class="comparison-table">
  <thead>
    <tr>
      <th>ADD C (Pin 23 - MSB)</th>
      <th>ADD B (Pin 24)</th>
      <th>ADD A (Pin 25 - LSB)</th>
      <th>Selected Analog Channel</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>0</td><td>0</td><td>0</td><td><strong>IN0</strong> (Pin 26)</td></tr>
    <tr><td>0</td><td>0</td><td>1</td><td><strong>IN1</strong> (Pin 27)</td></tr>
    <tr><td>0</td><td>1</td><td>0</td><td><strong>IN2</strong> (Pin 28)</td></tr>
    <tr><td>0</td><td>1</td><td>1</td><td><strong>IN3</strong> (Pin 1)</td></tr>
    <tr><td>1</td><td>0</td><td>0</td><td><strong>IN4</strong> (Pin 2)</td></tr>
    <tr><td>1</td><td>0</td><td>1</td><td><strong>IN5</strong> (Pin 3)</td></tr>
    <tr><td>1</td><td>1</td><td>0</td><td><strong>IN6</strong> (Pin 4)</td></tr>
    <tr><td>1</td><td>1</td><td>1</td><td><strong>IN7</strong> (Pin 5)</td></tr>
  </tbody>
</table>

<hr/>

<h4>E. Microcontroller Interfacing and Conversion Timing Sequence</h4>
<ol>
  <li><strong>Channel Selection:</strong> Apply the 3-bit channel address code on lines ADD A, ADD B, ADD C from the microcontroller GPIO port.</li>
  <li><strong>Address Latching:</strong> Provide a HIGH pulse on the <strong>ALE</strong> pin (min 100 ns) to lock the address into the multiplexer. In practice, ALE and START pins are frequently tied together to trigger both actions with a single MCU pulse.</li>
  <li><strong>Initiate Conversion:</strong> Drive <strong>START</strong> HIGH and then return it LOW. The falling edge resets the SAR register and initiates analog conversion. At this instant, <strong>EOC goes LOW</strong>, signaling that conversion is active.</li>
  <li><strong>Monitor EOC:</strong> Microcontroller polls the EOC line or configures an external hardware interrupt to listen for a LOW-to-HIGH transition. When EOC goes <strong>HIGH</strong>, conversion is complete.</li>
  <li><strong>Read Data:</strong> Microcontroller drives <strong>OE (Output Enable) HIGH</strong>. This commands the tri-state output buffers to drive D0–D7 onto the MCU data bus.</li>
  <li><strong>Complete Handshake:</strong> Microcontroller reads the digital byte, then returns <strong>OE LOW</strong> to release the data bus back to high-impedance.</li>
</ol>

<div class="formula-block">
  <strong>Step Size and Output Conversion Formula:</strong><br/>
  $$\text{Step Size (Resolution)} = \frac{V_{ref(+)} - V_{ref(-)}}{2^8} = \frac{5.0\text{V} - 0.0\text{V}}{256} = 19.531\text{ mV}$$
  $$\text{Digital Output (Decimal)} = \left\lfloor \frac{V_{in} - V_{ref(-)}}{19.531\text{ mV}} \right\rfloor$$
  For example, an input voltage $V_{in} = 2.0\text{V}$ yields:
  $$D = \left\lfloor \frac{2.0}{0.019531} \right\rfloor = 102_{10} = 0110\,0110_2 = 0\text{x}66$$
</div>
"""
    q3_html = q3_html.replace("__SVG_ADC0808__", svg_adc0808)

    q4_html = """
<h3>4. Sensors in IoT for Temperature, Pressure, and Humidity</h3>

<p class="not-found">Note: Syllabus topic and university exam question (x1). Lecture slides provide introductory coverage on temperature sensing; this section details the complete comparative and architectural breakdown of IoT-grade Temperature, Pressure, and Humidity sensors for 8-mark exam answers.</p>

<div class="definition-box">
  <strong>Role of Sensors in IoT Architecture:</strong> In the Internet of Things (IoT) reference framework, sensors constitute the <strong>Perception Layer (Physical Sensing Layer)</strong>. They continuously observe physical environmental parameters, convert them into conditioned electrical signals (analog or digital serial buses like I2C/SPI), and feed them to edge computing nodes (ESP32, STM32, Raspberry Pi) for local processing and telemetry upload to cloud platforms (AWS IoT, ThingsBoard, Azure) via Wi-Fi, LoRaWAN, or NB-IoT.
</div>

<hr/>

<h4>1. Temperature Sensors in IoT</h4>
<p>Temperature is the most frequently measured physical variable in IoT applications ranging from industrial condition monitoring to smart cold-chain logistics.</p>
<ul>
  <li><strong>LM35 (Analog Semiconductor Sensor):</strong>
    <ul>
      <li><em>Operating Principle:</em> Uses the temperature-dependent forward voltage characteristics of silicon PN junctions. Provides an output voltage linearly proportional to Celsius temperature: $V_{out} = 10\text{ mV/}^\circ\text{C}$.</li>
      <li><em>Range &amp; Accuracy:</em> $-55^\circ\text{C}$ to $+150^\circ\text{C}$ with $\pm 0.5^\circ\text{C}$ typical accuracy. Draws only 60 µA current.</li>
      <li><em>IoT Interfacing:</em> Connects to an ADC pin of an IoT node (e.g., ESP32 ADC pin).</li>
      <li><em>Use Case:</em> Server rack thermal alarms, basic HVAC thermostats.</li>
    </ul>
  </li>
  <li><strong>DS18B20 (1-Wire Digital Sensor):</strong>
    <ul>
      <li><em>Operating Principle:</em> Bandgap temperature sensor with on-chip 12-bit ADC and digital signal processor communicating over Maxim's proprietary <strong>1-Wire bus</strong>.</li>
      <li><em>Unique IoT Advantage:</em> Each sensor features a factory-lasered unique 64-bit ROM address code. This allows <strong>multiple DS18B20 sensors (dozens) to be daisy-chained on a single GPIO line</strong> with one external 4.7 kΩ pull-up resistor.</li>
      <li><em>Range:</em> $-55^\circ\text{C}$ to $+125^\circ\text{C}$ ($\pm 0.5^\circ\text{C}$ accuracy from $-10^\circ\text{C}$ to $+85^\circ\text{C}$). Supports "parasite power mode" (derives power directly from data line).</li>
      <li><em>Use Case:</em> Multi-zone pipeline monitoring, refrigerated vaccine cold-chain transport, soil depth temperature profiling.</li>
    </ul>
  </li>
  <li><strong>Thermocouples (Type-K with MAX6675 / MAX31855 SPI Interface):</strong>
    <ul>
      <li><em>Principle:</em> Seebeck effect (thermoelectric voltage generated across two dissimilar metals joined at a measurement junction).</li>
      <li><em>Range:</em> $0^\circ\text{C}$ to $+1024^\circ\text{C}$.</li>
      <li><em>Use Case:</em> Industrial furnaces, kilns, automotive exhaust gas temperature telemetry.</li>
    </ul>
  </li>
</ul>

<hr/>

<h4>2. Pressure Sensors in IoT</h4>
<p>Pressure sensors monitor atmospheric barometric pressure, liquid levels, pipe pressures, and vacuum states in smart cities and industrial automation.</p>
<ul>
  <li><strong>BMP280 / BME280 (Digital Piezoresistive Barometric Sensor):</strong>
    <ul>
      <li><em>Operating Principle:</em> Micro-Electro-Mechanical Systems (MEMS) diaphragm with integrated piezoresistive strain gauges. Deflection of the silicon membrane under air pressure alters the electrical resistance. An on-chip low-noise 24-bit ADC and DSP compute calibrated atmospheric pressure.</li>
      <li><em>Interface:</em> Standard <strong>$I^2C$ (address 0x76/0x77)</strong> or <strong>SPI bus</strong>. Operating current is only 2.7 µA at 1 Hz, making it exceptionally suited for battery-powered IoT devices.</li>
      <li><em>Pressure Range:</em> 300 hPa to 1100 hPa ($0.3\text{ to }1.1\text{ bar}$) with absolute accuracy of $\pm 1\text{ hPa}$.</li>
      <li><em>Altitude Calculation:</em> Because atmospheric pressure decreases exponentially with altitude according to the barometric formula, the sensor can calculate altitude with $\pm 1\text{ meter}$ precision:
        $$h = 44330 \times \left(1 - \left(\frac{P}{P_0}\right)^{1 / 5.255}\right)$$
      </li>
      <li><em>IoT Applications:</em> Drone altimeter and vertical stability hold, automated micro-weather forecasting stations, indoor floor-level navigation in smart buildings.</li>
    </ul>
  </li>
  <li><strong>MPX5010 / MPX5700 (Analog Piezoresistive Transducer):</strong>
    <ul>
      <li><em>Operating Principle:</em> Monolithic silicon pressure sensor with on-chip thin-film strain gauge shear stress network and temperature-compensated op-amp amplifier.</li>
      <li><em>Range:</em> 0 to 10 kPa ($0\text{ to }1.45\text{ psi}$) or up to 700 kPa. Outputs a calibrated $0.2\text{V}$ to $4.7\text{V}$ analog signal.</li>
      <li><em>IoT Applications:</em> Smart water utility pipe leak detection, hospital ventilator pressure loops, smart municipal tank level telemetry.</li>
    </ul>
  </li>
</ul>

<hr/>

<h4>3. Humidity Sensors in IoT</h4>
<p>Relative humidity (% RH) is critical in smart agriculture, pharmaceutical preservation, and building climate comfort.</p>
<ul>
  <li><strong>DHT11 &amp; DHT22 / AM2302 (Digital Capacitive Humidity Sensor):</strong>
    <ul>
      <li><em>Operating Principle:</em> Consists of a hygroscopic dielectric polymer layer sandwiched between two porous metallic electrodes. As water vapor molecules are absorbed or desorbed from ambient air, the dielectric constant changes proportionately, altering the capacitance ($C = \frac{\epsilon_r \epsilon_0 A}{d}$).</li>
      <li><em>Comparison:</em>
        <ul>
          <li><strong>DHT11:</strong> Lower cost; 20% to 90% RH range, $\pm 5\%$ RH accuracy; sampling rate 1 Hz.</li>
          <li><strong>DHT22:</strong> High precision; 0% to 100% RH range, $\pm 2\%$ RH accuracy; sampling rate 0.5 Hz.</li>
        </ul>
      </li>
      <li><em>Interface:</em> Single-bus bidirectional serial protocol with custom 40-bit handshake framing.</li>
      <li><em>IoT Applications:</em> Smart home air quality monitors, smart greenhouse automation, server room moisture alarms.</li>
    </ul>
  </li>
  <li><strong>BME280 (All-in-One Environmental Combo Sensor):</strong>
    <ul>
      <li><em>Unique Advantage:</em> Combines <strong>Temperature, Pressure, and Relative Humidity</strong> onto a single tiny $2.5 \times 2.5\text{ mm}$ package over $I^2C$/SPI.</li>
      <li><em>Humidity Specs:</em> 0 to 100% RH, $\pm 3\%$ accuracy, response time $\tau_{63\%} = 1\text{ s}$. Extremely low power (3.6 µA).</li>
      <li><em>IoT Applications:</em> Wearable health bands, remote agricultural weather stations, smart grain silo ventilation controls.</li>
    </ul>
  </li>
  <li><strong>Capacitive Soil Moisture Sensors (v1.2 / Corrosion Resistant):</strong>
    <ul>
      <li><em>Operating Principle:</em> Measures dielectric permittivity of surrounding soil via high-frequency fringing electric fields. Unlike resistive probes that corrode rapidly due to electrolysis, capacitive probes have no exposed metal traces.</li>
      <li><em>Output:</em> Analog DC voltage ($1.2\text{V}$ to $3.0\text{V}$) inversely proportional to moisture level.</li>
      <li><em>IoT Applications:</em> Automated solar-powered smart irrigation systems (activating solenoid valves only when soil moisture falls below calibrated threshold).</li>
    </ul>
  </li>
</ul>

<hr/>

<h4>4. Comparative Summary of IoT Environmental Sensors</h4>
<table class="comparison-table">
  <thead>
    <tr>
      <th>Sensor Name</th>
      <th>Physical Parameter</th>
      <th>Sensing Principle</th>
      <th>Output Interface</th>
      <th>Measurement Range</th>
      <th>Primary IoT Application</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>LM35</strong></td>
      <td>Temperature</td>
      <td>Silicon bandgap PN junction</td>
      <td>Analog ($10\text{ mV/}^\circ\text{C}$)</td>
      <td>$-55^\circ\text{C}$ to $+150^\circ\text{C}$</td>
      <td>Local cooling fan controllers, thermal monitoring.</td>
    </tr>
    <tr>
      <td><strong>DS18B20</strong></td>
      <td>Temperature</td>
      <td>Integrated 12-bit bandgap ADC</td>
      <td>Digital 1-Wire Serial</td>
      <td>$-55^\circ\text{C}$ to $+125^\circ\text{C}$</td>
      <td>Multi-point cold storage, vaccine tracking, piping.</td>
    </tr>
    <tr>
      <td><strong>BMP280</strong></td>
      <td>Barometric Pressure (+Temp)</td>
      <td>Piezoresistive MEMS diaphragm</td>
      <td>Digital $I^2C$ / SPI</td>
      <td>300 to 1100 hPa</td>
      <td>Drone altimeters, personal weather stations, altimetry.</td>
    </tr>
    <tr>
      <td><strong>DHT22</strong></td>
      <td>Humidity + Temperature</td>
      <td>Capacitive polymer + NTC</td>
      <td>Digital Single-wire bus</td>
      <td>0–100% RH, $-40\text{ to }+80^\circ\text{C}$</td>
      <td>Smart greenhouses, HVAC climate control systems.</td>
    </tr>
    <tr>
      <td><strong>BME280</strong></td>
      <td>Temp + Pressure + Humidity</td>
      <td>MEMS piezoresistive + polymer</td>
      <td>Digital $I^2C$ / SPI</td>
      <td>Full environmental span</td>
      <td>Compact smart agriculture telemetry nodes, wearables.</td>
    </tr>
    <tr>
      <td><strong>Capacitive Soil Probe</strong></td>
      <td>Soil Moisture</td>
      <td>Soil dielectric fringing field</td>
      <td>Analog DC voltage</td>
      <td>Dry (3.0V) to Wet (1.2V)</td>
      <td>Precision agricultural drip irrigation management.</td>
    </tr>
  </tbody>
</table>
"""

    return {
        "id": "3.1",
        "title": "Input Devices",
        "questions": [
            {
                "id": "3.1.1",
                "question": "Interfacing of analog and digital input devices with block diagrams.",
                "tags": ["musa Q.5", "first part"],
                "answer_html": q1_html
            },
            {
                "id": "3.1.2",
                "question": "Keyboard matrix interfacing and program to generate hex values.",
                "tags": ["x1"],
                "answer_html": q2_html
            },
            {
                "id": "3.1.3",
                "question": "Functional pin diagram of ADC 0808.",
                "tags": ["x1"],
                "answer_html": q3_html
            },
            {
                "id": "3.1.4",
                "question": "Sensors in IoT for temperature, pressure and humidity.",
                "tags": ["x1"],
                "answer_html": q4_html
            }
        ]
    }

print("Part 1 template ready!")
