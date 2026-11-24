# build_mod3_part2.py: Topic 3.2 Output Devices and Topic 3.3 Signal Conditioning (using non-fstring templates)

def get_topic_3_2(svg_output_devices_block, svg_dac_triangular, svg_stepper_motor):
    q5_html = """
<h3>5. Interfacing of Analog and Digital Output Devices</h3>

<div class="definition-box">
  <strong>Definition of Output Interfacing:</strong> An output device (or actuator) receives processed command signals from a microcontroller and transforms electrical energy into physical action, such as illumination (LED/display), audible sound (buzzer/speaker), rotational or linear motion (DC motor/stepper/servo), or switching high-power AC loads (relays/triacs). Because microcontrollers have strictly limited current-sinking and sourcing capabilities (typically 20 mA at 3.3V or 5V per pin), interfacing requires suitable buffer circuits, switching transistors, optocouplers, or digital-to-analog converters.
</div>

<p>Depending on the nature of the control signal and the physical mechanism driven, output interfacing falls into two categories:</p>
<ol>
  <li><strong>Digital Output Devices:</strong> Controlled strictly through discrete two-state binary logic (HIGH / LOW or ON / OFF).</li>
  <li><strong>Analog Output Devices:</strong> Controlled through continuously variable analog voltages, currents, or time-averaged power modulation (PWM).</li>
</ol>

__SVG_OUTPUT_DEVICES_BLOCK__

<hr/>

<h4>A. Digital Output Devices Interfacing</h4>
<p>Digital output devices switch between two operational states. However, each device poses specific electrical drive and isolation requirements:</p>
<ul>
  <li><strong>1. Light Emitting Diode (LED):</strong>
    <ul>
      <li><em>Working Principle:</em> Solid-state semiconductor PN junction that emits photons via electroluminescence when forward-biased.</li>
      <li><em>Current-Limiting Resistor Calculation:</em> LEDs have a fixed forward voltage drop ($V_f \approx 1.8\text{V}$ for red, $2.2\text{V}$ for green, $3.2\text{V}$ for blue/white) and standard operating current $I_f = 10\text{ to }20\text{ mA}$. Connecting directly to $5\text{V}$ causes thermal destruction.
        <div class="formula-block">
          $$R = \frac{V_{CC} - V_f}{I_f} = \frac{5.0\text{V} - 2.0\text{V}}{0.015\text{A}} = \frac{3.0\text{V}}{0.015\text{A}} = 200\,\Omega \implies \text{Standard } 220\,\Omega \text{ or } 330\,\Omega$$
        </div>
      </li>
      <li><em>Interfacing Topologies:</em>
        <ul>
          <li><strong>Active-HIGH (Current Sourcing):</strong> MCU pin connects to LED anode via resistor; cathode to GND. Logic 1 turns LED ON. Limited by MCU source current.</li>
          <li><strong>Active-LOW (Current Sinking):</strong> LED anode connects to $+5\text{V}$; cathode via resistor to MCU pin. Logic 0 turns LED ON. Most 8051 and older microcontrollers sink significantly more current than they source.</li>
        </ul>
      </li>
    </ul>
  </li>
  <li><strong>2. Buzzer (Audible Alarm):</strong>
    <ul>
      <li><em>Working Principle:</em> Piezoelectric diaphragm or electromagnetic coil that vibrates to generate sound waves when energized.</li>
      <li><em>Drive Circuit:</em> An electromagnetic buzzer requires 30–80 mA, which exceeds a standard microcontroller pin limit. An <strong>NPN switching transistor (BC547 or 2N2222)</strong> is configured in common-emitter mode. A 1 kΩ base resistor connects to the MCU pin. A reverse-biased flyback diode (1N4148) is wired across the buzzer coil to suppress inductive kickback spikes.</li>
    </ul>
  </li>
  <li><strong>3. Liquid Crystal Display (16×2 Character LCD):</strong>
    <ul>
      <li><em>Controller:</em> Industry-standard Hitachi HD44780 controller. Displays 2 lines of 16 ASCII characters using a $5 \times 8$ dot matrix.</li>
      <li><em>Interfacing Modes:</em>
        <ul>
          <li><strong>8-bit Mode:</strong> Uses 8 data lines (D0–D7) + 3 control lines (RS: Register Select, RW: Read/Write, E: Enable). Consumes 11 GPIO pins.</li>
          <li><strong>4-bit Mode:</strong> Transmits 8-bit bytes as two successive 4-bit nibbles over data lines D4–D7. Saves 4 pins (consumes only 7 GPIOs).</li>
          <li><strong>$I^2C$ Backpack (PCF8574):</strong> Converts parallel lines to serial $I^2C$ protocol, requiring only 2 pins (SDA, SCL).</li>
        </ul>
      </li>
    </ul>
  </li>
  <li><strong>4. Electromechanical Relay (AC Mains Load Control):</strong>
    <ul>
      <li><em>Working Principle:</em> Uses a low-voltage DC electromagnet coil (e.g. 5V or 12V) to mechanically pull armature contacts, switching isolated high-voltage AC mains appliances (230V AC lights, motors, heaters).</li>
      <li><em>Circuit Protection:</em> Always driven via an NPN transistor or ULN2003 driver with an antiparallel <strong>Flyback Diode (1N4007)</strong> across the coil to clamp inductive back-EMF voltage spikes ($V = -L \frac{di}{dt}$) that would otherwise destroy the switching transistor. An optocoupler (PC817) provides galvanic isolation between digital and power domains.</li>
    </ul>
  </li>
</ul>

<hr/>

<h4>B. Analog Output Devices Interfacing</h4>
<p>Because microcontrollers are digital processing cores containing only binary arithmetic logic, generating true continuously variable analog voltages or controlling continuous proportional power requires specialized interfacing techniques:</p>
<ol>
  <li><strong>Digital-to-Analog Converter (DAC):</strong>
    <ul>
      <li><em>Principle:</em> An integrated circuit using an <strong>R-2R resistor ladder network</strong> or binary-weighted current mirrors (e.g. DAC0808, MCP4725) that accepts an $N$-bit digital binary word and generates an exactly proportional output current or voltage.</li>
      <li><em>Output Formula:</em>
        $$V_{out} = V_{ref} \times \left(\frac{\text{Digital Input}}{2^N}\right)$$
      </li>
      <li><em>Application:</em> True audio waveform synthesis, function generators, analog instrumentation calibration.</li>
    </ul>
  </li>
  <li><strong>Pulse Width Modulation (PWM) with Analog Averaging:</strong>
    <ul>
      <li><em>Principle:</em> Generates a high-frequency digital square wave where the switching frequency ($f_{PWM}$) remains fixed, but the ratio of pulse ON-time to total period (the <strong>Duty Cycle, $D$</strong>) is dynamically modulated.</li>
      <li><em>Duty Cycle Definition:</em>
        <div class="formula-block">
          $$D = \frac{T_{ON}}{T_{ON} + T_{OFF}} \times 100\% = \frac{T_{ON}}{T_{period}} \times 100\%$$
          $$\text{Average Output Voltage: } V_{avg} = D \times V_{CC} = \left(\frac{T_{ON}}{T_{period}}\right) \times V_{CC}$$
        </div>
      </li>
      <li><em>Important Distinction (from Lecture Notes):</em> <strong>PWM is not a true analog voltage by itself!</strong> It is a digital binary pulse train. However, when applied to loads with mechanical or thermal inertia (such as motors or heating elements) or when passed through a low-pass RC smoothing filter ($f_c \ll f_{PWM}$), the high-frequency switching harmonics are averaged out, delivering a pure proportional DC voltage.</li>
      <li><em>Applications of PWM:</em>
        <ul>
          <li><strong>DC Motor Speed Control:</strong> Average armature voltage is varied using PWM through an H-Bridge driver IC (L293D or L298N).</li>
          <li><strong>LED Brightness Dimming:</strong> Rapid pulsing above human flicker fusion threshold (>100 Hz) adjusts perceived brightness cleanly without changing LED chromaticity.</li>
          <li><strong>RC Servo Motor Positioning:</strong> Standard 50 Hz PWM (20 ms period) where pulse width between 1.0 ms and 2.0 ms controls absolute shaft angle from $0^\circ$ to $180^\circ$.</li>
        </ul>
      </li>
    </ul>
  </li>
</ol>

<hr/>

<h4>C. Comprehensive Comparison: Analog vs. Digital Output Devices</h4>
<table class="comparison-table">
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Analog Output Devices</th>
      <th>Digital Output Devices</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Output Signal Nature</strong></td>
      <td>Continuously varying voltage/current or time-averaged power level (PWM duty cycle).</td>
      <td>Discrete two-state binary levels: HIGH (ON) or LOW (OFF).</td>
    </tr>
    <tr>
      <td><strong>Driving Mechanism</strong></td>
      <td>Requires DAC + Op-Amp transimpedance stage, or MCU Timer PWM module + driver/filter.</td>
      <td>Direct GPIO pin output, switching transistor (BJT/MOSFET), or relay module.</td>
    </tr>
    <tr>
      <td><strong>Control Resolution</strong></td>
      <td>Multi-level / continuous (e.g. 256 steps for 8-bit DAC, 4096 steps for 12-bit DAC).</td>
      <td>Binary: strictly 2 operational states ($0$ or $1$).</td>
    </tr>
    <tr>
      <td><strong>Power Dissipation</strong></td>
      <td>Linear analog drivers dissipate significant power ($P = I \times V_{drop}$); PWM switching is highly efficient (>90%).</td>
      <td>Very efficient in saturated switching modes (transistor fully ON or fully OFF).</td>
    </tr>
    <tr>
      <td><strong>Prominent Examples</strong></td>
      <td>DAC0808 output, PWM-driven DC motor speed, audio speaker amplifier, variable LED fader.</td>
      <td>LED status indicator, piezoelectric buzzer, 16×2 LCD, mechanical relay, 7-segment display.</td>
    </tr>
    <tr>
      <td><strong>Typical Applications</strong></td>
      <td>Motor velocity regulation, proportional thermal control, audio synthesis, servo positioning.</td>
      <td>System status alarms, appliance power ON/OFF, visual annunciators, emergency shutoff.</td>
    </tr>
  </tbody>
</table>
"""
    q5_html = q5_html.replace("__SVG_OUTPUT_DEVICES_BLOCK__", svg_output_devices_block)

    q6_html = """
<h3>6. Triangular Wave Generation using DAC0808 with Interfacing Circuit</h3>

<p class="not-found">Note: High-frequency university exam question (x2). While lecture slides introduce DAC as a concept, this section provides the complete step-by-step circuit schematic, op-amp transimpedance calculation, waveform timing analysis, and embedded assembly/C generation program.</p>

<div class="definition-box">
  <strong>Working Principle of DAC0808:</strong> The DAC0808 is an industry-standard 8-bit monolithic multiplying Digital-to-Analog Converter. It consists of an inverted R-2R ladder network and 8 high-speed bipolar current steering switches. It accepts an 8-bit parallel digital binary input word ($A_1$ through $A_8$) and sinks an output current $I_{out}$ (at Pin 4) that is directly proportional to the digital value:
  $$I_{out} = I_{ref} \times \left( \frac{A_1}{2} + \frac{A_2}{4} + \frac{A_3}{8} + \dots + \frac{A_8}{256} \right)$$
  where $A_1$ is the Most Significant Bit (MSB) and $A_8$ is the Least Significant Bit (LSB).
</div>

<h4>A. Hardware Interfacing Circuit Design</h4>
<p>Because the DAC0808 generates an <strong>output current ($I_{out}$)</strong> rather than an output voltage, an external Operational Amplifier (such as the LM741, OP07, or TL081) is configured as a <strong>Current-to-Voltage Converter (Transimpedance Amplifier)</strong>.</p>

__SVG_DAC_TRIANGULAR__

<h5>Detailed Circuit Connections:</h5>
<ul>
  <li><strong>Digital Inputs ($A_1$ to $A_8$):</strong> Connected to an 8-bit microcontroller port (e.g. Port 1 of 8051 or Port D of AVR/Arduino), where $A_1$ (Pin 5) is MSB and $A_8$ (Pin 12) is LSB.</li>
  <li><strong>Reference Voltage Inputs:</strong>
    <ul>
      <li>Pin 14 ($V_{ref(+)}$): Connected to a stable $+5.0\text{V}$ reference through an accurate reference resistor $R_{ref} = 5\text{ k}\Omega$. This sets the reference current:
        $$I_{ref} = \frac{V_{ref}}{R_{ref}} = \frac{5.0\text{V}}{5\text{ k}\Omega} = 1.0\text{ mA}$$
      </li>
      <li>Pin 15 ($V_{ref(-)}$): Connected directly to system Ground ($0\text{V}$).</li>
    </ul>
  </li>
  <li><strong>Power Supplies:</strong> Pin 13 ($V_{CC}$) to $+5\text{V}$ (or $+12\text{V}$); Pin 3 ($V_{EE}$) to $-12\text{V}$ or $-15\text{V}$.</li>
  <li><strong>Frequency Compensation:</strong> Pin 16 is tied to $V_{EE}$ via a $0.1\,\mu\text{F}$ capacitor to guarantee amplifier stability and eliminate ringing.</li>
  <li><strong>Current-to-Voltage Converter (Op-Amp LM741):</strong>
    <ul>
      <li>Pin 4 ($I_{out}$ of DAC) connects directly to the <strong>inverting input (Pin 2)</strong> of the Op-Amp. Because the non-inverting input (Pin 3) is tied to ground, the inverting node is held at <em>virtual ground ($0\text{V}$)</em>, ensuring zero voltage compliance error for the DAC current switches.</li>
      <li>Feedback resistor $R_f = 5\text{ k}\Omega$ is connected between the inverting input and the Op-Amp output (Pin 6).</li>
    </ul>
  </li>
</ul>

<div class="formula-block">
  <strong>Output Voltage Transfer Function:</strong><br/>
  $$V_{out} = I_{out} \times R_f = \left[ \frac{V_{ref}}{R_{ref}} \times \left(\frac{\text{Digital Value}}{256}\right) \right] \times R_f$$
  When $R_f = R_{ref} = 5\text{ k}\Omega$:
  $$V_{out} = V_{ref} \times \left(\frac{\text{Digital Value}}{256}\right)$$
  <ul>
    <li>When Digital Input = <code>0x00</code> (0 decimal): $V_{out} = 5\text{V} \times \frac{0}{256} = 0.00\text{V}$.</li>
    <li>When Digital Input = <code>0x80</code> (128 decimal): $V_{out} = 5\text{V} \times \frac{128}{256} = 2.50\text{V}$.</li>
    <li>When Digital Input = <code>0xFF</code> (255 decimal): $V_{out} = 5\text{V} \times \frac{255}{256} = 4.98\text{V}$ (Full Scale).</li>
    <li><strong>Step Size (Resolution):</strong> $\Delta V = \frac{5.0\text{V}}{256} = 19.531\text{ mV per step}$.</li>
  </ul>
</div>

<hr/>

<h4>B. Triangular Wave Generation Principle &amp; Algorithm</h4>
<p>A periodic triangular wave consists of a strictly linear positive slope (ramp-up) followed by an identical linear negative slope (ramp-down):</p>
<ol>
  <li><strong>Ramp-Up Phase:</strong>
    <ul>
      <li>Initialize the microcontroller accumulator / counter register to <code>0x00</code>.</li>
      <li>Output the value to DAC Port.</li>
      <li>Call a calibrated software delay subroutine $T_{delay}$.</li>
      <li>Increment counter by 1.</li>
      <li>Repeat until counter reaches <code>0xFF</code> (255 decimal). As the binary value increases linearly from 0 to 255, the op-amp output voltage rises linearly from $0.0\text{V}$ to $4.98\text{V}$.</li>
    </ul>
  </li>
  <li><strong>Ramp-Down Phase:</strong>
    <ul>
      <li>Decrement counter by 1.</li>
      <li>Output value to DAC Port.</li>
      <li>Call the same delay subroutine $T_{delay}$.</li>
      <li>Repeat until counter reaches <code>0x00</code>. As the value decreases linearly from 255 to 0, output falls linearly back to $0.0\text{V}$.</li>
    </ul>
  </li>
  <li><strong>Continuous Repetition:</strong> Enclose both loops inside an infinite loop (<code>while(1)</code> / <code>SJMP</code>) to generate a continuous, steady triangular waveform.</li>
</ol>

<div class="formula-block">
  <strong>Frequency and Period Calculations:</strong><br/>
  One complete triangular wave period consists of:
  $$N_{total} = 256 \text{ steps (up)} + 256 \text{ steps (down)} = 512 \text{ steps}$$
  $$\text{Period } T = 512 \times t_{step} = 512 \times (t_{delay} + t_{instruction})$$
  $$\text{Frequency } f = \frac{1}{T} = \frac{1}{512 \times t_{step}}$$
  <em>Example:</em> If $t_{step} = 10\,\mu\text{s}$, then $T = 512 \times 10\,\mu\text{s} = 5.12\text{ ms}$, giving frequency $f = \frac{1}{0.00512} \approx 195.3\text{ Hz}$.
</div>

<hr/>

<h4>C. Complete Embedded C Program (8051 / Keil C Architecture)</h4>
<pre><code>#include &lt;reg51.h&gt;

#define DAC_PORT P1  // Port 1 connected to DAC0808 inputs A1-A8

// Calibrated Microsecond Delay
void delay_us(unsigned int count) {
    while(count--);
}

void main(void) {
    unsigned int val;

    DAC_PORT = 0x00;  // Initialize DAC to 0V

    while(1) {
        // ---------------------------------------------
        // RAMP-UP: Generate rising slope (0V to ~5V)
        // ---------------------------------------------
        for(val = 0; val &lt;= 255; val++) {
            DAC_PORT = val;     // Output byte to DAC0808
            delay_us(5);        // Adjust delay to set waveform frequency
        }

        // ---------------------------------------------
        // RAMP-DOWN: Generate falling slope (~5V to 0V)
        // ---------------------------------------------
        for(val = 255; val &gt; 0; val--) {
            DAC_PORT = val;     // Output byte to DAC0808
            delay_us(5);        // Identical delay for symmetric wave
        }
        DAC_PORT = 0;           // Complete bottom peak at 0
        delay_us(5);
    }
}
</code></pre>

<hr/>

<h4>D. 8051 Assembly Language Program for Maximum Speed</h4>
<pre><code>; 8051 Assembly Program to Generate Triangular Waveform using DAC0808 on Port 1
ORG 0000H
    MOV P1, #00H         ; Initialize Port 1 to 00H

REPEAT:
    ; --- Ramp Up Phase (00H to FFH) ---
    MOV A, #00H          ; Start at 00H
UP_LOOP:
    MOV P1, A            ; Send byte to DAC
    INC A                ; Increment count
    CJNE A, #0FFH, UP_LOOP ; Loop until A reaches 0xFF
    MOV P1, #0FFH        ; Output peak 0xFF

    ; --- Ramp Down Phase (FFH to 00H) ---
DOWN_LOOP:
    DEC A                ; Decrement count
    MOV P1, A            ; Send byte to DAC
    JNZ DOWN_LOOP        ; Continue until A = 0

    SJMP REPEAT          ; Repeat continuously
END
</code></pre>
"""
    q6_html = q6_html.replace("__SVG_DAC_TRIANGULAR__", svg_dac_triangular)

    q7_html = """
<h3>7. Working, Construction, and Interfacing of Stepper Motor</h3>

<p class="not-found">Note: Primary syllabus topic and university exam question (x1). Lecture notes mention motor drivers; this comprehensive section provides the full 8-mark university examination answer detailing internal construction, operating principle, stepping modes, driver circuit design (ULN2003), and sequence programs.</p>

<div class="definition-box">
  <strong>Definition of Stepper Motor:</strong> A stepper motor is a brushless, synchronous electromechanical actuator that converts digital electrical pulse sequences into precise, discrete mechanical angular increments (steps). Each electrical input pulse commands the rotor to rotate through a fixed, calibrated angle called the <strong>Step Angle ($\beta$)</strong>. Because shaft displacement is directly proportional to the number of input pulses and rotational speed is directly proportional to pulse frequency, stepper motors achieve exceptional open-loop position and speed control without requiring closed-loop feedback encoders.
</div>

<h4>A. Construction &amp; Types of Stepper Motors</h4>
<p>A stepper motor consists of a multiphase stationary stator containing electromagnetic coils and a central permanent magnet or toothed soft-iron rotor:</p>
<ol>
  <li><strong>Permanent Magnet (PM) Stepper Motor:</strong>
    <ul>
      <li>Rotor consists of a cylindrical permanent magnet magnetized with alternating north and south poles parallel to the rotor axis.</li>
      <li>Offers moderate step angles ($7.5^\circ\text{ to }45^\circ$), good holding torque even when de-energized (detent torque), and low manufacturing cost.</li>
    </ul>
  </li>
  <li><strong>Variable Reluctance (VR) Stepper Motor:</strong>
    <ul>
      <li>Rotor is made of soft non-magnetic iron cut with teeth; it possesses no internal permanent magnet.</li>
      <li>Operates on the <em>principle of minimum magnetic reluctance</em>: when a stator phase is energized, the rotor teeth rotate to align with the energized stator poles to minimize magnetic path reluctance. Zero detent torque when powered down.</li>
    </ul>
  </li>
  <li><strong>Hybrid Synchronous Stepper Motor:</strong>
    <ul>
      <li>Combines the best attributes of PM and VR motors. Features an axially magnetized permanent magnet core enclosed by two toothed soft-iron cups offset by half a tooth pitch.</li>
      <li>Offers high positional accuracy, high holding torque, and fine step angles (typically $1.8^\circ$ or $0.9^\circ$). Standard in 3D printers, CNC mills, and robotic joints.</li>
    </ul>
  </li>
  <li><strong>Unipolar vs. Bipolar Winding Configurations:</strong>
    <ul>
      <li><strong>Unipolar Stepper (5 or 6 Wires):</strong> Each phase coil has a center-tap connection tied to positive DC supply ($+12\text{V}$). Current flows in only one direction per half-coil, enabling simple low-side driver circuits (single transistor per coil like ULN2003).</li>
      <li><strong>Bipolar Stepper (4 Wires):</strong> Coils have no center taps. Driving requires reversing the direction of current flow through each entire coil using dual full H-Bridges (e.g. L298N or A4988). Delivers roughly 30% higher torque for the same motor volume.</li>
    </ul>
  </li>
</ol>

<div class="formula-block">
  <strong>Step Angle ($\beta$) Formulas:</strong><br/>
  $$\beta = \frac{360^\circ}{N_{steps}} = \frac{360^\circ}{\text{Number of steps per revolution}}$$
  $$\beta = \frac{|N_s - N_r|}{N_s \times N_r} \times 360^\circ$$
  where $N_s$ is the number of stator magnetic poles and $N_r$ is the number of rotor teeth.<br/>
  <em>Example:</em> A standard hybrid motor with $N_{steps} = 200$ has a step angle:
  $$\beta = \frac{360^\circ}{200} = 1.8^\circ \text{ per step}$$
</div>

<hr/>

<h4>B. Stepper Motor Driver Circuit (ULN2003 Interfacing)</h4>
<p>Microcontroller I/O pins supply at most 20 mA at 5V, while even small stepper motors (such as the popular 28BYJ-48 unipolar motor) require 200 mA to 600 mA at 5V–12V. Connecting a motor directly to MCU pins will destroy the silicon port buffers due to overcurrent and inductive back-EMF spikes. A <strong>ULN2003 Darlington Transistor Array IC</strong> is utilized as a robust buffer interface.</p>

__SVG_STEPPER_MOTOR__

<h5>Key Roles of ULN2003 Driver IC:</h5>
<ul>
  <li><strong>Current Amplification:</strong> Contains 7 high-voltage, high-current NPN Darlington transistor pairs capable of sinking up to <strong>500 mA per channel</strong> with a 50V collector breakdown rating.</li>
  <li><strong>Internal Flyback Clamping Diodes:</strong> Pin 9 (COM) is connected to the motor power supply ($+12\text{V}$). Internal cathode-connected suppression diodes absorb inductive turn-off voltage spikes ($V = -L \frac{di}{dt}$), safeguarding the driver transistors.</li>
  <li><strong>Logic Level Compatibility:</strong> Features built-in 2.7 kΩ base series resistors, enabling direct interface with 5V TTL and CMOS microcontroller pins without external discrete components.</li>
</ul>

<hr/>

<h4>C. Excitation and Stepping Modes</h4>
<p>A 4-phase unipolar stepper motor (coils A, B, C, D) can be driven in three distinct sequence modes:</p>

<table class="comparison-table">
  <thead>
    <tr>
      <th>Stepping Mode</th>
      <th>Excitation Sequence</th>
      <th>Hex Code</th>
      <th>Torque &amp; Characteristics</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Wave Drive (One-Phase ON)</strong></td>
      <td>
        Step 1: Coil A<br/>
        Step 2: Coil B<br/>
        Step 3: Coil C<br/>
        Step 4: Coil D
      </td>
      <td>
        <code>0x08</code> (1000b)<br/>
        <code>0x04</code> (0100b)<br/>
        <code>0x02</code> (0010b)<br/>
        <code>0x01</code> (0001b)
      </td>
      <td>
        <strong>Lowest Power Consumption.</strong> Only one phase draws current at any instant. Lower holding torque. Prone to resonance at low speeds.
      </td>
    </tr>
    <tr>
      <td><strong>2. Full-Step Drive (Two-Phase ON)</strong></td>
      <td>
        Step 1: Coils A &amp; B<br/>
        Step 2: Coils B &amp; C<br/>
        Step 3: Coils C &amp; D<br/>
        Step 4: Coils D &amp; A
      </td>
      <td>
        <code>0x0C</code> (1100b)<br/>
        <code>0x06</code> (0110b)<br/>
        <code>0x03</code> (0011b)<br/>
        <code>0x09</code> (1001b)
      </td>
      <td>
        <strong>Maximum Torque.</strong> Two coils energized simultaneously produce $\sqrt{2} \approx 1.414$ times higher torque than wave drive. Best dynamic holding capability.
      </td>
    </tr>
    <tr>
      <td><strong>3. Half-Step Drive (1-Phase / 2-Phase Alternate)</strong></td>
      <td>
        Step 1: A<br/>
        Step 2: A+B<br/>
        Step 3: B<br/>
        Step 4: B+C<br/>
        Step 5: C<br/>
        Step 6: C+D<br/>
        Step 7: D<br/>
        Step 8: D+A
      </td>
      <td>
        <code>0x08</code><br/>
        <code>0x0C</code><br/>
        <code>0x04</code><br/>
        <code>0x06</code><br/>
        <code>0x02</code><br/>
        <code>0x03</code><br/>
        <code>0x01</code><br/>
        <code>0x09</code>
      </td>
      <td>
        <strong>Doubled Angular Resolution.</strong> Step angle is halved (e.g. $1.8^\circ \to 0.9^\circ$). Motion is exceptionally smooth, significantly reducing mechanical vibration and acoustic noise.
      </td>
    </tr>
  </tbody>
</table>

<hr/>

<h4>D. Direction and Speed Control Principles</h4>
<ul>
  <li><strong>Direction Control:</strong> Executing the step table sequentially from Step 1 to Step 4 produces <strong>Clockwise (CW)</strong> rotation. Traversing the table in reverse order (Step 4 down to Step 1) reverses the magnetic stator vector, producing <strong>Counter-Clockwise (CCW)</strong> rotation.</li>
  <li><strong>Speed (RPM) Control:</strong> Rotational velocity depends strictly on the inter-step time delay ($T_{delay}$):
    <div class="formula-block">
      $$\text{Speed (RPM)} = \frac{\text{Steps per Second}}{\text{Steps per Revolution}} \times 60 = \frac{\left(\frac{1}{T_{delay}}\right)}{N_{steps}} \times 60$$
    </div>
    Decreasing $T_{delay}$ accelerates the motor; increasing $T_{delay}$ slows it down.
  </li>
</ul>

<hr/>

<h4>E. Complete Embedded C Program (Arduino / 8051 Architecture)</h4>
<pre><code>#include &lt;reg51.h&gt;

#define MOTOR_PORT P1  // P1.0 to P1.3 connect to ULN2003 IN1-IN4

// Full-Step 4-Phase Drive Sequence (Clockwise: A, B, C, D)
const unsigned char step_sequence[4] = {0x0C, 0x06, 0x03, 0x09};

void delay_ms(unsigned int ms) {
    unsigned int i, j;
    for(i = 0; i &lt; ms; i++)
        for(j = 0; j &lt; 120; j++);
}

// Rotate Stepper Motor by a given number of steps
// dir = 1 for CW, dir = 0 for CCW
void step_motor(unsigned int total_steps, unsigned char dir, unsigned int speed_delay) {
    unsigned int i;
    int step_idx = 0;

    for(i = 0; i &lt; total_steps; i++) {
        MOTOR_PORT = step_sequence[step_idx]; // Energize coils
        delay_ms(speed_delay);                // Controls motor speed

        if(dir == 1) {
            step_idx++;
            if(step_idx &gt;= 4) step_idx = 0;  // Wrap around CW
        }} else {
            step_idx--;
            if(step_idx &lt; 0) step_idx = 3;   // Wrap around CCW
        }
    }
    MOTOR_PORT = 0x00; // De-energize coils to prevent static heating
}

void main(void) {
    while(1) {
        // Rotate 1 Full Revolution (200 steps at 1.8 deg/step) Clockwise
        step_motor(200, 1, 10);
        delay_ms(1000); // Pause 1 second

        // Rotate 1 Full Revolution Counter-Clockwise
        step_motor(200, 0, 10);
        delay_ms(1000); // Pause 1 second
    }
}
</code></pre>
"""
    q7_html = q7_html.replace("__SVG_STEPPER_MOTOR__", svg_stepper_motor)

    return {
        "id": "3.2",
        "title": "Output Devices",
        "questions": [
            {
                "id": "3.2.1",
                "question": "Interfacing of analog and digital output devices with diagrams.",
                "tags": ["musa Q.18"],
                "answer_html": q5_html
            },
            {
                "id": "3.2.2",
                "question": "Generate a triangular wave using DAC, with interfacing circuit.",
                "tags": ["x2"],
                "answer_html": q6_html
            },
            {
                "id": "3.2.3",
                "question": "Working of stepper motor.",
                "tags": ["x1"],
                "answer_html": q7_html
            }
        ]
    }


def get_topic_3_3(svg_signal_conditioning):
    q8_html = """
<h3>8. Signal Conditioning: Role of Amplifiers, LPF, and Notch Filters</h3>

<div class="definition-box">
  <strong>Definition of Signal Conditioning:</strong> Signal conditioning encompasses the sequence of analog electronic processing stages applied to raw transducer output signals to adapt, scale, and purify them so that they satisfy the strict input voltage range, bandwidth, and signal-to-noise ratio (SNR) requirements of an Analog-to-Digital Converter (ADC) or microcontroller.
</div>

<h4>A. Why Signal Conditioning is Essential in Embedded Systems</h4>
<p>Real-world environmental and physiological sensors rarely produce electrical signals that an embedded microcontroller can digitize directly:</p>
<ul>
  <li><strong>Extremely Weak Amplitudes:</strong> Biomedical electrodes (ECG, EEG, EMG) produce potentials of only <strong>10 µV to 5 mV</strong>; thermocouples output ~40 µV/°C; piezoresistive strain bridges output microvolts. An Arduino ADC with 4.88 mV resolution would digitize a 2 mV heartbeat into pure zero or random quantization noise!</li>
  <li><strong>High-Frequency Noise:</strong> Thermal Johnson-Nyquist noise, radio-frequency interference (RFI), switching power-supply harmonics, and mechanical vibration introduce erratic high-frequency jitter.</li>
  <li><strong>Mains Power Line Hum (50 Hz / 60 Hz):</strong> The pervasive alternating magnetic and electrostatic fields radiated by standard AC electrical wiring (50 Hz in India/Europe, 60 Hz in the Americas) couple into sensor cables, introducing a heavy sinusoidal hum that dwarfs small physiological signals.</li>
  <li><strong>Impedance Mismatch:</strong> Many sensors (e.g. piezoelectric crystals or pH glass probes) possess megaohm internal source impedances and cannot supply the current required to charge an ADC's internal sampling capacitor without severe loading attenuation.</li>
</ul>

__SVG_SIGNAL_CONDITIONING__

<hr/>

<h4>B. The 5-Stage Signal Conditioning Chain in Detail</h4>

<h5>1. Stage 1: Weak Sensor Signal</h5>
<ul>
  <li><em>Characteristics:</em> Very small amplitude (e.g., ECG cardiac depolarization waveform ~2 mV to 5 mV; soil moisture probe ~100 mV).</li>
  <li><em>Corruption:</em> Buried under a combination of high-frequency white noise and 50 Hz power-line interference.</li>
</ul>

<h5>2. Stage 2: Operational Amplifier (Instrumentation / Non-Inverting Op-Amp)</h5>
<ul>
  <li><em>Primary Role:</em> Provides linear voltage amplification to boost the millivolt-level signal up to the standard ADC input span ($0\text{V to }5\text{V}$ or $0\text{V to }3.3\text{V}$).</li>
  <li><em>Buffer Action:</em> Delivers ultra-high input impedance ($>10^{12}\,\Omega$ with FET-input op-amps like TL081 or AD620), preventing loading on the sensor, and very low output impedance to drive subsequent filters.</li>
  <li><em>Configuration &amp; Formula:</em> Non-Inverting Amplifier configuration:
    <div class="formula-block">
      $$A_v = 1 + \frac{R_f}{R_1}$$
      $$V_{out} = A_v \times V_{in} = \left(1 + \frac{R_f}{R_1}\right) \times V_{in}$$
    </div>
  </li>
  <li><em>Practical Engineering Design:</em> For massive gains (e.g. $A_v = 1000$ to boost 2 mV to 2V), a single stage requires $R_f / R_1 = 999$. Using a single 30 MΩ resistor introduces severe stray capacitance and drift. In practical engineering, the gain is partitioned across two cascading stages (e.g. $A_{v1} = 31.6$ and $A_{v2} = 31.6$, yielding $31.6 \times 31.6 \approx 1000$).</li>
</ul>

<h5>3. Stage 3: Low-Pass Filter (LPF)</h5>
<ul>
  <li><em>Primary Role:</em> Passes desired low-frequency physiological or environmental phenomena (ECG diagnostic bandwidth is 0.05 Hz to 100 Hz; soil moisture changes at &lt;1 Hz) while sharply attenuating high-frequency noise, transient spikes, and radio interference.</li>
  <li><em>Anti-Aliasing Function:</em> Guarantees compliance with the <strong>Nyquist-Shannon Sampling Criterion</strong> ($f_s \ge 2 f_{max}$), preventing high-frequency noise from folding back (aliasing) into the digitized spectrum.</li>
  <li><em>Circuit Topology:</em> Passive RC network (series resistor $R$ followed by shunt capacitor $C$ to ground) or Active Sallen-Key 2nd-order Butterworth filter.</li>
  <li><em>Cutoff Frequency Formula:</em>
    <div class="formula-block">
      $$f_c = \frac{1}{2 \pi R C}$$
    </div>
    At $f = f_c$, the signal power drops by $-3\text{ dB}$ ($0.707$ of passband amplitude). Beyond $f_c$, attenuation rolls off at $-20\text{ dB/decade}$ (for 1st-order) or $-40\text{ dB/decade}$ (for 2nd-order).
  </li>
</ul>

<h5>4. Stage 4: Notch Filter (Band-Stop Filter)</h5>
<ul>
  <li><em>Primary Role:</em> Selectively eliminates the single interfering frequency of <strong>50 Hz mains hum</strong> (or 60 Hz) without distorting the desired biological or sensor waveform lying immediately adjacent in the spectrum.</li>
  <li><em>Circuit Topology:</em> The <strong>Active Twin-T Notch Filter</strong> consists of two parallel T-networks:
    <ul>
      <li>Low-pass T: Two resistors $R$ and one shunt capacitor $2C$.</li>
      <li>High-pass T: Two capacitors $C$ and one shunt resistor $R/2$ connected to a voltage follower.</li>
    </ul>
  </li>
  <li><em>Center Notch Frequency Formula:</em>
    <div class="formula-block">
      $$f_0 = \frac{1}{2 \pi R C} = 50\text{ Hz}$$
    </div>
  </li>
  <li><em>Rejection Capability:</em> Delivers deep attenuation exceeding $-40\text{ dB to }-60\text{ dB}$ precisely at 50 Hz, effectively eradicating power hum.</li>
</ul>

<h5>5. Stage 5: Clean Signal Delivery to ADC / Microcontroller</h5>
<ul>
  <li><em>Characteristics:</em> The conditioned signal is now an amplified, noise-purified, hum-free waveform spanning the optimum dynamic range of the microcontroller ADC ($0\text{ to }5\text{V}$ or $0\text{ to }3.3\text{V}$), ensuring maximum quantization fidelity and resolution.</li>
</ul>

<hr/>

<h4>C. Fully Worked Numerical Problems (Directly from Module 3 VSY Class PDF)</h4>

<div class="formula-block" style="background:#f0fdf4; border:1px solid #86efac;">
  <h4 style="margin-top:0; color:#166534;">Numerical Problem 1: Soil Moisture Sensor System</h4>
  <p><strong>Problem Statement (from Class Notes):</strong><br/>
  <em>A soil moisture sensor used in an automatic water irrigation system gives a very weak 100 mV signal with high-frequency noise above 100 Hz and 50 Hz mains hum. Apply the knowledge of signal conditioning chain to get a clean 1V signal for Arduino. Given $R_1 = 10\text{ k}\Omega, C = 0.1\,\mu\text{F}$.</em></p>

  <p><strong>Step-by-Step Mathematical Solution:</strong></p>
  <ol>
    <li><strong>Step 1: Design of Non-Inverting Amplifier Stage</strong>
      <ul>
        <li>Input Voltage $V_{in} = 100\text{ mV} = 0.1\text{V}$</li>
        <li>Desired Output Voltage $V_{out} = 1.0\text{V}$</li>
        <li>Required Voltage Gain:
          $$A_v = \frac{V_{out}}{V_{in}} = \frac{1.0\text{V}}{0.1\text{V}} = 10$$
        </li>
        <li>Formula for Non-Inverting Op-Amp:
          $$A_v = 1 + \frac{R_f}{R_1}$$
        </li>
        <li>Substitute $A_v = 10$ and given $R_1 = 10\text{ k}\Omega$:
          $$10 = 1 + \frac{R_f}{10\text{ k}\Omega} \implies \frac{R_f}{10\text{ k}\Omega} = 9$$
          $$R_f = 9 \times 10\text{ k}\Omega = \mathbf{90\text{ k}\Omega}$$
        </li>
        <li><em>Component Selection:</em> Use standard precision metal-film resistor $R_f = 90\text{ k}\Omega$ (or standard $91\text{ k}\Omega$).</li>
      </ul>
    </li>

    <li><strong>Step 2: Design of Low-Pass Filter (LPF) Stage</strong>
      <ul>
        <li>Noise cutoff requirement: Eliminate high-frequency noise above 100 Hz $\implies f_c = 100\text{ Hz}$.</li>
        <li>Given capacitor value: $C = 0.1\,\mu\text{F} = 0.1 \times 10^{-6}\,\text{F}$.</li>
        <li>LPF Cutoff Formula:
          $$f_c = \frac{1}{2 \pi R_{lpf} C}$$
        </li>
        <li>Rearranging to solve for resistance $R_{lpf}$:
          $$R_{lpf} = \frac{1}{2 \pi f_c C} = \frac{1}{2 \times 3.14159 \times 100 \times (0.1 \times 10^{-6})}$$
          $$R_{lpf} = \frac{1}{6.28318 \times 10^{-5}} = 15915.5\,\Omega \approx \mathbf{15.91\text{ k}\Omega}$$
        </li>
        <li><em>Component Selection:</em> Standard $16\text{ k}\Omega$ (or $15\text{ k}\Omega + 910\,\Omega$ in series).</li>
      </ul>
    </li>

    <li><strong>Step 3: Design of 50 Hz Notch Filter Stage</strong>
      <ul>
        <li>Requirement: Eliminate 50 Hz power-line mains hum $\implies f_0 = 50\text{ Hz}$.</li>
        <li>Given capacitor value: $C = 0.1\,\mu\text{F}$.</li>
        <li>Notch Center Frequency Formula:
          $$f_0 = \frac{1}{2 \pi R_{notch} C}$$
        </li>
        <li>Solving for $R_{notch}$:
          $$R_{notch} = \frac{1}{2 \pi f_0 C} = \frac{1}{2 \times 3.14159 \times 50 \times (0.1 \times 10^{-6})}$$
          $$R_{notch} = \frac{1}{3.14159 \times 10^{-5}} = 31830.9\,\Omega \approx \mathbf{31.83\text{ k}\Omega}$$
        </li>
        <li><em>Twin-T Component Values:</em>
          <ul>
            <li>Two series resistors $R = 31.83\text{ k}\Omega$ (standard $31.6\text{ k}\Omega$).</li>
            <li>One shunt resistor $R/2 = \frac{31.83\text{ k}\Omega}{2} = 15.91\text{ k}\Omega$.</li>
            <li>Two capacitors $C = 0.1\,\mu\text{F}$.</li>
            <li>One shunt capacitor $2C = 2 \times 0.1\,\mu\text{F} = 0.2\,\mu\text{F}$ (standard $0.22\,\mu\text{F}$).</li>
          </ul>
        </li>
      </ul>
    </li>

    <li><strong>Final System Synthesis:</strong>
      <p>Soil Moisture Sensor (100 mV) $\to$ Op-Amp Non-Inverting Amp ($R_1 = 10\text{ k}\Omega, R_f = 90\text{ k}\Omega, A_v = 10$) $\to$ LPF ($R = 15.91\text{ k}\Omega, C = 0.1\,\mu\text{F}, f_c = 100\text{ Hz}$) $\to$ Twin-T Notch Filter ($R = 31.83\text{ k}\Omega, C = 0.1\,\mu\text{F}, f_0 = 50\text{ Hz}$) $\to$ Arduino ADC Channel A0 (Clean 1.0V DC signal).</p>
    </li>
  </ol>
</div>

<br/>

<div class="formula-block" style="background:#eff6ff; border:1px solid #93c5fd;">
  <h4 style="margin-top:0; color:#1e40af;">Numerical Problem 2: Continuous Cardiac Monitoring ECG Sensor in ICU</h4>
  <p><strong>Problem Statement (from Class Notes):</strong><br/>
  <em>An ECG sensor used for Continuous Cardiac Monitoring in an ICU gives a very weak 2 mV signal with high-frequency noise above 120 Hz and 50 Hz mains hum. Apply the knowledge of signal conditioning chain to get a clean 2V signal for Arduino. Given $R_1 = 30\text{ k}\Omega, C = 0.1\,\mu\text{F}$.</em></p>

  <p><strong>Step-by-Step Mathematical Solution:</strong></p>
  <ol>
    <li><strong>Step 1: Design of Amplifier Stage</strong>
      <ul>
        <li>Input Voltage $V_{in} = 2\text{ mV} = 0.002\text{V}$</li>
        <li>Desired Output Voltage $V_{out} = 2.0\text{V}$</li>
        <li>Required Overall Voltage Gain:
          $$A_v = \frac{V_{out}}{V_{in}} = \frac{2.0\text{V}}{0.002\text{V}} = 1000$$
        </li>
        <li>Formula for Non-Inverting Op-Amp:
          $$A_v = 1 + \frac{R_f}{R_1}$$
        </li>
        <li>Substitute $A_v = 1000$ and given $R_1 = 30\text{ k}\Omega$:
          $$1000 = 1 + \frac{R_f}{30\text{ k}\Omega} \implies \frac{R_f}{30\text{ k}\Omega} = 999$$
          $$R_f = 999 \times 30\text{ k}\Omega = \mathbf{29.97\text{ M}\Omega}$$
        </li>
        <li><em>Practical Engineering Implementation Note:</em> In biomedical instrumentation, realizing a gain of 1000 with a single stage using a $30\text{ M}\Omega$ feedback resistor suffers from excessive thermal noise, gain-bandwidth product limitations, and stray parasitic capacitance. Therefore, the gain of 1000 is practically split across two stages:
          <ul>
            <li><strong>Stage A (Instrumentation Pre-amplifier):</strong> Gain $A_{v1} = \sqrt{1000} \approx 31.62$</li>
            <li><strong>Stage B (Non-inverting Second Stage):</strong> Gain $A_{v2} = \sqrt{1000} \approx 31.62$</li>
            <li>Total Cascaded Gain $= 31.62 \times 31.62 = 1000$.</li>
          </ul>
        </li>
      </ul>
    </li>

    <li><strong>Step 2: Design of Low-Pass Filter (LPF) Stage</strong>
      <ul>
        <li>Noise cutoff requirement: Eliminate high-frequency noise above 120 Hz $\implies f_c = 120\text{ Hz}$.</li>
        <li>Given capacitor value: $C = 0.1\,\mu\text{F} = 0.1 \times 10^{-6}\,\text{F}$.</li>
        <li>Solving for $R_{lpf}$:
          $$R_{lpf} = \frac{1}{2 \pi f_c C} = \frac{1}{2 \times 3.14159 \times 120 \times (0.1 \times 10^{-6})}$$
          $$R_{lpf} = \frac{1}{7.5398 \times 10^{-5}} = 13262.9\,\Omega \approx \mathbf{13.26\text{ k}\Omega}$$
        </li>
        <li><em>Component Selection:</em> Standard $13.3\text{ k}\Omega$ metal-film resistor.</li>
      </ul>
    </li>

    <li><strong>Step 3: Design of 50 Hz Notch Filter Stage</strong>
      <ul>
        <li>Interfering mains hum frequency $f_0 = 50\text{ Hz}$. Given $C = 0.1\,\mu\text{F}$.</li>
        <li>Solving for $R_{notch}$:
          $$R_{notch} = \frac{1}{2 \pi f_0 C} = \frac{1}{2 \times 3.14159 \times 50 \times (0.1 \times 10^{-6})} = \mathbf{31.83\text{ k}\Omega}$$
        </li>
        <li><em>Twin-T Component Values:</em>
          <ul>
            <li>Resistors: Two of $R = 31.83\text{ k}\Omega$, one of $R/2 = 15.91\text{ k}\Omega$.</li>
            <li>Capacitors: Two of $C = 0.1\,\mu\text{F}$, one of $2C = 0.2\,\mu\text{F}$.</li>
          </ul>
        </li>
      </ul>
    </li>

    <li><strong>Final System Synthesis:</strong>
      <p>ICU Patient ECG Electrodes (2 mV) $\to$ Instrumentation Op-Amp Chain ($A_v = 1000$) $\to$ RC Low-Pass Filter ($f_c = 120\text{ Hz}, R = 13.26\text{ k}\Omega, C = 0.1\,\mu\text{F}$) $\to$ Active Twin-T 50 Hz Notch Filter ($f_0 = 50\text{ Hz}, R = 31.83\text{ k}\Omega, C = 0.1\,\mu\text{F}$) $\to$ Arduino ADC Pin A0 (Pristine 2.0V P-Q-R-S-T cardiac waveform ready for cardiac arrhythmia detection algorithms).</p>
    </li>
  </ol>
</div>
"""
    q8_html = q8_html.replace("__SVG_SIGNAL_CONDITIONING__", svg_signal_conditioning)

    return {
        "id": "3.3",
        "title": "Signal Conditioning",
        "questions": [
            {
                "id": "3.3.1",
                "question": "Signal conditioning; role of amplifiers, LPF and notch filters.",
                "tags": ["musa Q.26"],
                "answer_html": q8_html
            }
        ]
    }

print("Part 2 template ready!")
