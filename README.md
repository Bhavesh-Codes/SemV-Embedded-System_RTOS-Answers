# Embedded Systems & RTOS — University Exam Study Guide

A polished, self-contained, offline-ready web study guide designed specifically for **8-mark university examination questions** in **Embedded Systems & Real-Time Operating Systems (RTOS)**.

All answers have been compiled and verified directly from the teacher's lecture notes and presentation PDFs across all 6 modules, preserving the exact question bank wording, syllabic hierarchy, PYQ frequency tags, and Musa references.

---

## 🚀 How to Open the Website

1. Navigate to the `Embedded-Systems-Study-Guide` folder.
2. Double-click **`index.html`** to open it directly in any web browser (Chrome, Edge, Firefox, Safari, Brave, etc.).
3. **No web server, Node.js, database, or internet connection is required.** The application is 100% self-contained and pre-bundled to work seamlessly over the `file://` protocol.

---

## 🎨 Design & Aesthetic Features

- **Minimal Academic Dashboard:** Soft pastel color palette (lavender, sky blue, mint, peach, rose, and amber).
- **Collapsible Question Cards:** Each question is housed in an accordion card displaying:
  - Exact question wording
  - PYQ frequency badge (e.g., `🔥 (x7)`, `🔥 (x3)`)
  - Musa reference badge (e.g., `📖 musa Q.14`)
  - Syllabus-only indicators (`📋 Syllabus`)
- **8-Mark Exam-Ready Answers:**
  - Clear definitions in highlighted callout boxes (`.definition-box`)
  - Subheadings and numbered/bulleted points
  - Responsive comparison tables with clean zebra striping
  - Step-by-step mathematical formulas and worked numericals (`.formula-block`)
  - Formatted assembly and C code blocks with one-click **Copy** button
  - Technically accurate, responsive inline SVG diagrams (architecture, circuits, flowcharts, state transitions, and Gantt charts)
- **Instant Search:** Real-time search across question text, topic headers, Musa tags, and answer content with direct jump and accordion auto-open.
- **Filter Bar:** One-click quick filters for *All Questions (62)*, *High Frequency (≥ x3)*, *Musa PYQ List*, and *Syllabus Only*.
- **Expand / Collapse All:** Quick controls to expand or collapse all cards in the current module view.
- **Module Navigation:** Direct sidebar navigation, next/previous module footers, and a smooth back-to-top button.
- **Mobile Responsive:** Adaptive layout with collapsible drawer navigation for mobile and tablet screens.

---

## 📚 Curriculum & Question Coverage Summary (62 Questions)

### Module 1: Introduction to Embedded Systems & Embedded Programming (8 Questions)
- **1.1 Definition, Characteristics, ES vs GPCS, Classification, Applications**
  - Q1.1.1: Define embedded system. Explain its characteristics, classification, components, application areas and examples. Differentiate between embedded systems and general computing systems. `(x7) (musa Q.14)`
  - Q1.1.2: Specialties of embedded systems. `(x1) (musa Q.14)`
  - Q1.1.3: Explain embedded system architecture in detail. `(x1) (musa Q.10)`
- **1.2 Design Metrics**
  - Q1.2.1: Explain the design metrics (cost, power dissipation, time to market, NRE cost, performance) with examples. `(x3) (musa Q.9)`
  - Q1.2.2: Challenges in optimization of design metrics. `(syllabus only)`
- **1.3 Embedded C**
  - Q1.3.1: Need for embedded C programming; bit and byte data types; significance of static and volatile modifiers. `(musa Q.28 iv)`
  - Q1.3.2: What is an ISR? Explain interrupt handling and exception handling in embedded systems. `(musa Q.28 i)`
  - Q1.3.3: Bit operations and unsigned number representation. `(syllabus only)`

### Module 2: Embedded Processors (16 Questions)
- **2.1 Features of Embedded Cores, Memories**
  - Q2.1.1: Explain SoC (System on Chip). `(x3)`
  - Q2.1.2: Compare µC, ASIC, ASSP, SoC and FPGA. `(musa Q.27 v)`
  - Q2.1.3: Embedded cores: RISC vs CISC (PYQs also list DSP and ARM cores). `(x2) (musa Q.10)`
  - Q2.1.4: Differentiate between microprocessor and microcontroller. `(x1)`
  - Q2.1.5: Different types of memories used in embedded systems. `(musa Q.15)`
- **2.2 Case Study: ARM Cortex-M3**
  - Q2.2.1: Features of ARM and why it is suitable for embedded systems. Draw and explain the architecture of Cortex-M3 with its features. `(x7) (musa Q.1)`
  - Q2.2.2: CPSR / special registers. `(x5) (musa Q.16)`
  - Q2.2.3: Programmer's model (general-purpose and special registers). `(x1) (musa Q.16)`
  - Q2.2.4: How are exceptions and interrupts handled? Role of NVIC. `(x3) (musa Q.28 iii)`
  - Q2.2.5: Operating modes and states. `(x1) (musa Q.11)`
  - Q2.2.6: MPU and memory map. `(syllabus only)`
- **2.3 Low Power**
  - Q2.3.1: Need and techniques for low power; low power modes in Cortex-M3 and their significance. `(musa Q.8)`
- **2.4 Cortex A, R, M Comparison**
  - Q2.4.1: Compare ARM Cortex-A, Cortex-R and Cortex-M series. `(musa Q.27 iv)`
- **2.5 ATmega328P (Arduino)**
  - Q2.5.1: Hardware features of ATmega328P (Arduino Uno/Nano). `(musa Q.17)`
  - Q2.5.2: Compare features of Arduino and Raspberry Pi. `(x2)`
  - Q2.5.3: Extended libraries of Arduino. `(x2)`

### Module 3: Interfacing Analog and Digital Devices (8 Questions)
- **3.1 Input Devices**
  - Q3.1.1: Interfacing of analog and digital input devices with block diagrams. `(musa Q.5, first part)`
  - Q3.1.2: Keyboard matrix interfacing and program to generate hex values. `(x1)`
  - Q3.1.3: Functional pin diagram of ADC 0808. `(x1)`
  - Q3.1.4: Sensors in IoT for temperature, pressure and humidity. `(x1)`
- **3.2 Output Devices**
  - Q3.2.1: Interfacing of analog and digital output devices with diagrams. `(musa Q.18)`
  - Q3.2.2: Generate a triangular wave using DAC, with interfacing circuit. `(x2)`
  - Q3.2.3: Working of stepper motor. `(x1)`
- **3.3 Signal Conditioning**
  - Q3.3.1: Signal conditioning; role of amplifiers, LPF and notch filters. `(musa Q.26)`

### Module 4: Embedded Communication Interfaces (7 Questions)
- **4.1 Wired: UART, SPI, I2C, CAN**
  - Q4.1.1: Serial communication / serial port / serial modes. UART working and features. `(x6) (musa Q.19)`
  - Q4.1.2: Program to transfer a message serially at a given baud rate. `(x3)`
  - Q4.1.3: Find TH1 value for a given baud rate. `(x2)`
  - Q4.1.4: Working of the I2C protocol with diagram. `(musa Q.5, second part)`
  - Q4.1.5: CAN bus communication with diagram, and its application. `(musa Q.3)`
  - Q4.1.6: SPI protocol, and comparison of UART, SPI, I2C and CAN. `(syllabus only)`
- **4.2 Wireless / Peripheral**
  - Q4.2.1: Compare USB 2.0, Bluetooth, Zigbee and RFID with respect to features and applications. `(musa)`

### Module 5: Real Time Operating Systems (14 Questions)
- **5.1 RTOS Basics and Scheduling**
  - Q5.1.1: RTOS basics, characteristics, architecture, hard vs soft RTOS. Need for RTOS in embedded systems; RTOS vs GPOS. `(x7) (musa Q.4)`
  - Q5.1.2: Multitasking and task scheduling; preemptive vs non-preemptive scheduling. `(musa Q.6)`
  - Q5.1.3: Task scheduling algorithms. `(x3) (musa Q.6, Q.13)`
  - Q5.1.4: Task, task states and TCB. `(x1)`
  - Q5.1.5: Task states and state transition diagram. `(musa Q.12)`
  - Q5.1.6: Criteria for task schedulability and various scheduling mechanisms. `(musa Q.13)`
  - Q5.1.7: Differentiate between RMS and EDF scheduling. `(musa Q.27 ii)`
  - Q5.1.8: NUMERICAL: Gantt charts for preemptive SJF, Priority and Round Robin; average waiting and turnaround time. `(musa Numerical Q.2)`
- **5.2 Inter-Process Communication**
  - Q5.2.1: IPC methods: message queues, mailboxes and event timers. `(x2) (musa Q.7)`
  - Q5.2.2: Event register and use of event function. `(x1)`
- **5.3 Task Synchronization**
  - Q5.3.1: Semaphore and mutex and their use; binary and counting semaphore with examples. `(x5) (musa Q.20)`
  - Q5.3.2: Deadlock, race condition and livelock; prevention methods. `(musa Q.21)`
  - Q5.3.3: Priority inversion: causes, effects, example; resolved by priority inheritance and priority ceiling. `(x3) (musa Q.22)`
  - Q5.3.4: Use semaphores to solve the shared data problem. `(x1)`

### Module 6: System Integration and Design (9 Questions)
- **6.1 EDLC**
  - Q6.1.1: Explain the Embedded Product Design Life Cycle (EDLC) with diagram. `(musa Q.2)`
- **6.2 System Design Steps and Testing**
  - Q6.2.1: Major steps in embedded system design (requirements, component selection, hardware and software architecture). `(musa Q.25)`
  - Q6.2.2: Role of FSM and flowcharts in embedded software design, with example. `(musa Q.23)`
  - Q6.2.3: Testing and debugging methodologies; hardware testing tools, emulator, simulator, debugger; hardware and software design issues. `(musa Q.24)`
  - Q6.2.4: Differentiate between white box and black box testing. `(musa Q.27 i)`
  - Q6.2.5: Various software testing methods for embedded systems. `(musa Q.28 ii)`
- **6.3 Example Applications**
  - Q6.3.1: Smart Card Reader system. `(x4)`
  - Q6.3.2: Design an embedded system (automatic toll collection / vending machine / smart agriculture monitoring) covering specification, component choice, hardware block diagram and software architecture. `(musa Numerical Q.1)`
  - Q6.3.3: Environment monitoring system. `(syllabus only)`

---

## 📁 Project Directory Structure

```text
Embedded-Systems-Study-Guide/
├── index.html                    # Main self-contained application entry point
├── README.md                     # Comprehensive documentation & syllabus guide
├── assets/
│   ├── css/
│   │   └── style.css             # Modern pastel design, responsive typography & layout
│   └── js/
│       ├── app.js                # Search, filtering, navigation & accordion controls
│       └── data.js               # Pre-bundled JSON data for zero-CORS file:// execution
└── data/
    ├── mod1_answers.json         # Module 1 answers (70.9 KB)
    ├── mod2_answers.json         # Module 2 answers (165.4 KB)
    ├── mod3_answers.json         # Module 3 answers (145.2 KB)
    ├── mod4_answers.json         # Module 4 answers (82.7 KB)
    ├── mod5_answers.json         # Module 5 answers (123.2 KB)
    └── mod6_answers.json         # Module 6 answers (64.4 KB)
```

---

## 📐 Included Technical Diagrams (Inline SVG)

1. **Embedded System Architecture:** Core processor, memory (Flash/RAM), sensors, actuators, and communication buses.
2. **ARM Cortex-M3 Architecture:** 3-stage pipeline core, NVIC, Bus Matrix, Bit-band regions, AHB-Lite, and debug subsystems.
3. **Cortex-M3 Register Set & Special Registers:** R0-R12, SP (MSP/PSP), LR, PC, xPSR, PRIMASK, FAULTMASK, BASEPRI, CONTROL.
4. **4x4 Keyboard Matrix Interfacing:** Row drive and column read pull-up circuit diagram with debounce flow.
5. **ADC 0808 Pinout Diagram:** Full 28-pin functional layout (IN0-IN7, ALE, START, EOC, OE, CLK, Vref).
6. **DAC Triangular Wave Generator:** Interfacing circuit to 8-bit DAC with operational amplifier buffer and output ramp waveform.
7. **Stepper Motor Interfacing:** 4-phase unipolar stepper motor interfaced via ULN2003 Darlington driver IC.
8. **Signal Conditioning Circuit Chain:** Transducer &rarr; Instrumentation Op-Amp &rarr; Active LPF &rarr; 50 Hz Notch Filter &rarr; ADC.
9. **UART Protocol Frame Format:** Start bit, 8 data bits, parity bit, and stop bits timing chart.
10. **I2C Bus Interfacing & Timing:** Master-Slave architecture, SDA/SCL pull-up resistors, START/STOP conditions, ACK/NACK.
11. **SPI Master-Slave Topology:** MOSI, MISO, SCK, and SS lines for single and multi-slave configurations.
12. **CAN Bus Architecture:** Differential signaling (CAN_H, CAN_L, dominant 0 vs. recessive 1) and 120&Omega; termination resistors.
13. **RTOS State Transition Diagram:** Ready, Running, Blocked/Waiting, Suspended states with transition events.
14. **Gantt Charts for Preemptive Scheduling:** Preemptive SJF, Priority, and Round Robin scheduling timelines with waiting/turnaround calculations.
15. **Priority Inversion & Priority Inheritance Timeline:** Unbounded inversion scenario and dynamic priority elevation resolution.
16. **EDLC Waterfall Model:** Need Identification &rarr; Conceptualization &rarr; Analysis &rarr; Design &rarr; Development & Testing &rarr; Deployment &rarr; Support.
17. **Smart Card Reader Architecture:** Contact interface, ISO 7816 pins, microcontroller processing, and host PC communication.
18. **Automatic Chocolate Vending Machine Block Diagram:** Coin validator, keypad, MCU, motor drivers, dispensing coils, and LCD.
19. **IoT Environmental Monitoring System:** Multi-sensor array (temperature, humidity, air quality), MCU, Wi-Fi/LoRa, cloud dashboard.

---
*Created for University Examination Excellence.*
