import json
import os

OUTPUT_PATH = r"d:\LAST EXAM(MDM)\antigravity version\Embedded-Systems-Study-Guide\data\mod3_answers.json"

# ==============================================================================
# SVG DIAGRAMS
# ==============================================================================

svg_analog_input_block = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 170" width="100%" height="auto" style="max-width:760px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px;">
  <defs>
    <marker id="arrow-ai" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#2563eb" />
    </marker>
  </defs>
  <text x="380" y="24" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#1e293b">Block Diagram: Interfacing Analog Input Devices to Microcontroller</text>
  
  <!-- Block 1: Physical Parameter -->
  <rect x="20" y="55" width="105" height="60" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="72" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#1e3a8a">Physical</text>
  <text x="72" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#1e3a8a">Quantity</text>
  <text x="72" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(Temp, Light, Force)</text>

  <line x1="125" y1="85" x2="160" y2="85" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-ai)"/>

  <!-- Block 2: Analog Sensor / Transducer -->
  <rect x="165" y="55" width="115" height="60" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="222" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#92400e">Analog Sensor</text>
  <text x="222" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#92400e">/ Transducer</text>
  <text x="222" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(LDR, LM35, Potentiometer)</text>

  <line x1="280" y1="85" x2="315" y2="85" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-ai)"/>
  <text x="298" y="78" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#475569">V_analog</text>

  <!-- Block 3: Signal Conditioning -->
  <rect x="320" y="55" width="125" height="60" rx="6" fill="#fce7f3" stroke="#ec4899" stroke-width="2"/>
  <text x="382" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#831843">Signal</text>
  <text x="382" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#831843">Conditioning</text>
  <text x="382" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(Amplifier + Filter)</text>

  <line x1="445" y1="85" x2="480" y2="85" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-ai)"/>
  <text x="463" y="78" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#475569">0–5V DC</text>

  <!-- Block 4: ADC -->
  <rect x="485" y="55" width="105" height="60" rx="6" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
  <text x="537" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#14532d">ADC</text>
  <text x="537" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="600" fill="#14532d">(Internal/External)</text>
  <text x="537" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(e.g. 10-bit: 0–1023)</text>

  <line x1="590" y1="85" x2="625" y2="85" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow-ai)"/>
  <text x="608" y="78" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#475569">Binary</text>

  <!-- Block 5: MCU -->
  <rect x="630" y="55" width="110" height="60" rx="6" fill="#ede9fe" stroke="#8b5cf6" stroke-width="2"/>
  <text x="685" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#4c1d95">Microcontroller</text>
  <text x="685" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="600" fill="#4c1d95">(CPU / Processing)</text>
  <text x="685" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(Arduino, ESP32, ARM)</text>
</svg>
</div>'''

svg_digital_input_block = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 170" width="100%" height="auto" style="max-width:720px; background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px;">
  <defs>
    <marker id="arrow-di" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#0d9488" />
    </marker>
  </defs>
  <text x="360" y="24" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#1e293b">Block Diagram: Interfacing Digital Input Devices to Microcontroller</text>
  
  <!-- Block 1: Digital Sensor -->
  <rect x="30" y="55" width="140" height="60" rx="6" fill="#ccfbf1" stroke="#0d9488" stroke-width="2"/>
  <text x="100" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#134e4a">Digital Input Device</text>
  <text x="100" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#134e4a">Pushbutton / PIR / IR</text>
  <text x="100" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(Discrete HIGH/LOW)</text>

  <line x1="170" y1="85" x2="225" y2="85" stroke="#0d9488" stroke-width="2" marker-end="url(#arrow-di)"/>
  <text x="198" y="78" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#475569">Raw 0/1</text>

  <!-- Block 2: Signal Conditioning / Protection -->
  <rect x="230" y="55" width="170" height="60" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="315" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#92400e">Interfacing Interface</text>
  <text x="315" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#92400e">Pull-up / Pull-down / Debounce</text>
  <text x="315" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(Level Shifter / Optocoupler)</text>

  <line x1="400" y1="85" x2="455" y2="85" stroke="#0d9488" stroke-width="2" marker-end="url(#arrow-di)"/>
  <text x="428" y="78" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#475569">Logic Level</text>

  <!-- Block 3: MCU GPIO -->
  <rect x="460" y="55" width="220" height="60" rx="6" fill="#ede9fe" stroke="#8b5cf6" stroke-width="2"/>
  <text x="570" y="80" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#4c1d95">Microcontroller GPIO Pin</text>
  <text x="570" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#4c1d95">Input Buffer / Interrupt Service (ISR)</text>
  <text x="570" y="128" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">(Direct digital read via Port Register)</text>
</svg>
</div>'''

svg_keyboard_matrix = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 540" width="100%" height="auto" style="max-width:620px; background:#ffffff; border:1px solid #cbd5e1; border-radius:8px;">
  <!-- Title -->
  <text x="310" y="28" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" font-weight="700" fill="#0f172a">4×4 Matrix Keyboard Interfacing with Microcontroller</text>
  <text x="310" y="46" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Rows: Driven as OUTPUT (Active LOW) | Columns: Read as INPUT with Pull-up Resistors</text>

  <!-- Microcontroller Left Box -->
  <rect x="20" y="70" width="110" height="380" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="75" y="100" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#1d4ed8">MCU</text>
  <text x="75" y="118" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#3b82f6">(8051 / AVR /</text>
  <text x="75" y="132" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#3b82f6">Arduino)</text>

  <!-- MCU Pins Labels -->
  <!-- Outputs (Rows) -->
  <text x="120" y="175" text-anchor="end" font-family="monospace" font-size="11" font-weight="bold" fill="#1e3a8a">R0 (P1.0) ─</text>
  <text x="120" y="235" text-anchor="end" font-family="monospace" font-size="11" font-weight="bold" fill="#1e3a8a">R1 (P1.1) ─</text>
  <text x="120" y="295" text-anchor="end" font-family="monospace" font-size="11" font-weight="bold" fill="#1e3a8a">R2 (P1.2) ─</text>
  <text x="120" y="355" text-anchor="end" font-family="monospace" font-size="11" font-weight="bold" fill="#1e3a8a">R3 (P1.3) ─</text>

  <!-- Inputs (Columns) -->
  <text x="120" y="395" text-anchor="end" font-family="monospace" font-size="10" fill="#047857">C0-C3 ◄─</text>
  <text x="75" y="420" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#047857">Port Pins as</text>
  <text x="75" y="432" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#047857">Inputs</text>

  <!-- Horizontal Row Lines -->
  <line x1="125" y1="170" x2="520" y2="170" stroke="#2563eb" stroke-width="2"/>
  <line x1="125" y1="230" x2="520" y2="230" stroke="#2563eb" stroke-width="2"/>
  <line x1="125" y1="290" x2="520" y2="290" stroke="#2563eb" stroke-width="2"/>
  <line x1="125" y1="350" x2="520" y2="350" stroke="#2563eb" stroke-width="2"/>

  <!-- Vertical Column Lines -->
  <line x1="200" y1="110" x2="200" y2="390" stroke="#059669" stroke-width="2"/>
  <line x1="280" y1="110" x2="280" y2="390" stroke="#059669" stroke-width="2"/>
  <line x1="360" y1="110" x2="360" y2="390" stroke="#059669" stroke-width="2"/>
  <line x1="440" y1="110" x2="440" y2="390" stroke="#059669" stroke-width="2"/>

  <!-- Column Pull-up Resistors at Top -->
  <!-- VCC Rail -->
  <line x1="180" y1="70" x2="460" y2="70" stroke="#dc2626" stroke-width="2"/>
  <text x="475" y="74" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#dc2626">+5V (Vcc)</text>

  <!-- Resistors symbols (rectangles) -->
  <rect x="193" y="75" width="14" height="25" fill="#fef3c7" stroke="#b45309" stroke-width="1.5"/>
  <text x="188" y="92" text-anchor="end" font-family="system-ui, sans-serif" font-size="8" fill="#b45309">10k</text>
  <line x1="200" y1="70" x2="200" y2="75" stroke="#dc2626" stroke-width="1.5"/>
  <line x1="200" y1="100" x2="200" y2="110" stroke="#059669" stroke-width="1.5"/>

  <rect x="273" y="75" width="14" height="25" fill="#fef3c7" stroke="#b45309" stroke-width="1.5"/>
  <text x="268" y="92" text-anchor="end" font-family="system-ui, sans-serif" font-size="8" fill="#b45309">10k</text>
  <line x1="280" y1="70" x2="280" y2="75" stroke="#dc2626" stroke-width="1.5"/>
  <line x1="280" y1="100" x2="280" y2="110" stroke="#059669" stroke-width="1.5"/>

  <rect x="353" y="75" width="14" height="25" fill="#fef3c7" stroke="#b45309" stroke-width="1.5"/>
  <text x="348" y="92" text-anchor="end" font-family="system-ui, sans-serif" font-size="8" fill="#b45309">10k</text>
  <line x1="360" y1="70" x2="360" y2="75" stroke="#dc2626" stroke-width="1.5"/>
  <line x1="360" y1="100" x2="360" y2="110" stroke="#059669" stroke-width="1.5"/>

  <rect x="433" y="75" width="14" height="25" fill="#fef3c7" stroke="#b45309" stroke-width="1.5"/>
  <text x="428" y="92" text-anchor="end" font-family="system-ui, sans-serif" font-size="8" fill="#b45309">10k</text>
  <line x1="440" y1="70" x2="440" y2="75" stroke="#dc2626" stroke-width="1.5"/>
  <line x1="440" y1="100" x2="440" y2="110" stroke="#059669" stroke-width="1.5"/>

  <!-- Column labels -->
  <text x="200" y="125" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="#047857">C0</text>
  <text x="280" y="125" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="#047857">C1</text>
  <text x="360" y="125" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="#047857">C2</text>
  <text x="440" y="125" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="#047857">C3</text>

  <!-- Connect columns back to MCU inputs at bottom -->
  <polyline points="200,390 200,410 130,410" fill="none" stroke="#059669" stroke-width="1.5" stroke-dasharray="3"/>
  <polyline points="280,390 280,420 130,420" fill="none" stroke="#059669" stroke-width="1.5" stroke-dasharray="3"/>
  <polyline points="360,390 360,430 130,430" fill="none" stroke="#059669" stroke-width="1.5" stroke-dasharray="3"/>
  <polyline points="440,390 440,440 130,440" fill="none" stroke="#059669" stroke-width="1.5" stroke-dasharray="3"/>

  <!-- KEYS / SWITCHES (Row 0) -->
  <circle cx="200" cy="170" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="200" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">1</text>

  <circle cx="280" cy="170" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="280" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">2</text>

  <circle cx="360" cy="170" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="360" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">3</text>

  <circle cx="440" cy="170" r="16" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="440" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#991b1b">A</text>

  <!-- KEYS / SWITCHES (Row 1) -->
  <circle cx="200" cy="230" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="200" y="235" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">4</text>

  <circle cx="280" cy="230" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="280" y="235" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">5</text>

  <circle cx="360" cy="230" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="360" y="235" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">6</text>

  <circle cx="440" cy="230" r="16" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="440" y="235" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#991b1b">B</text>

  <!-- KEYS / SWITCHES (Row 2) -->
  <circle cx="200" cy="290" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="200" y="295" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">7</text>

  <circle cx="280" cy="290" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="280" y="295" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">8</text>

  <circle cx="360" cy="290" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="360" y="295" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">9</text>

  <circle cx="440" cy="290" r="16" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="440" y="295" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#991b1b">C</text>

  <!-- KEYS / SWITCHES (Row 3) -->
  <circle cx="200" cy="350" r="16" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="200" y="356" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#854d0e">* (E)</text>

  <circle cx="280" cy="350" r="16" fill="#f1f5f9" stroke="#475569" stroke-width="1.5"/>
  <text x="280" y="355" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#0f172a">0</text>

  <circle cx="360" cy="350" r="16" fill="#fef9c3" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="360" y="356" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#854d0e"># (F)</text>

  <circle cx="440" cy="350" r="16" fill="#fee2e2" stroke="#dc2626" stroke-width="1.5"/>
  <text x="440" y="355" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#991b1b">D</text>

  <!-- Bottom Explanatory Banner -->
  <rect x="20" y="465" width="580" height="60" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="30" y="484" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#1e293b">Scanning Principle:</text>
  <text x="30" y="500" font-family="system-ui, sans-serif" font-size="10" fill="#334155">• Ground one row at a time (e.g. R0=0, R1=R2=R3=1). Read column bus C0–C3.</text>
  <text x="30" y="515" font-family="system-ui, sans-serif" font-size="10" fill="#334155">• If a key is pressed, that column line is pulled LOW (0). MCU maps (Row, Col) to Hex code.</text>
</svg>
</div>'''

svg_adc0808 = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 520" width="100%" height="auto" style="max-width:680px; background:#ffffff; border:1px solid #cbd5e1; border-radius:8px;">
  <!-- Title -->
  <text x="340" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" font-weight="700" fill="#0f172a">ADC 0808 — Functional Pin Diagram (28-Pin Dual In-Line Package)</text>
  <text x="340" y="44" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">8-Bit Successive Approximation ADC with 8-Channel Multiplexer</text>

  <!-- IC Chip Body -->
  <rect x="240" y="60" width="200" height="420" rx="8" fill="#1e293b" stroke="#0f172a" stroke-width="2"/>
  
  <!-- Notch at top -->
  <path d="M 320 60 A 20 20 0 0 0 360 60 Z" fill="#ffffff" stroke="#0f172a" stroke-width="1"/>
  <circle cx="260" cy="80" r="4" fill="#94a3b8"/> <!-- Pin 1 indicator -->

  <text x="340" y="110" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#38bdf8">ADC 0808</text>
  <text x="340" y="126" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#94a3b8">8-Bit SAR ADC</text>

  <!-- Internal Architecture blocks text inside IC -->
  <rect x="255" y="145" width="170" height="70" rx="4" fill="#334155"/>
  <text x="340" y="170" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" fill="#f8fafc">8-Channel MUX</text>
  <text x="340" y="185" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#94a3b8">Address Latch & Decoder</text>
  <text x="340" y="200" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#94a3b8">(ADD A, B, C / ALE)</text>

  <rect x="255" y="225" width="170" height="65" rx="4" fill="#334155"/>
  <text x="340" y="248" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" fill="#f8fafc">SAR Core + DAC</text>
  <text x="340" y="263" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#94a3b8">Comparator & Control Logic</text>
  <text x="340" y="278" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#94a3b8">(START, EOC, CLK)</text>

  <rect x="255" y="300" width="170" height="60" rx="4" fill="#334155"/>
  <text x="340" y="323" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" fill="#f8fafc">Tri-State Output Latch</text>
  <text x="340" y="338" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#94a3b8">8-Bit Data Bus (D0–D7)</text>
  <text x="340" y="352" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#94a3b8">Output Enable (OE)</text>

  <!-- PINS LEFT (1 to 14) -->
  <!-- Pin 1: IN3 -->
  <line x1="170" y1="80" x2="240" y2="80" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="84" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">1</text>
  <text x="160" y="84" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN3</text>

  <!-- Pin 2: IN4 -->
  <line x1="170" y1="108" x2="240" y2="108" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="112" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">2</text>
  <text x="160" y="112" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN4</text>

  <!-- Pin 3: IN5 -->
  <line x1="170" y1="136" x2="240" y2="136" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="140" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">3</text>
  <text x="160" y="140" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN5</text>

  <!-- Pin 4: IN6 -->
  <line x1="170" y1="164" x2="240" y2="164" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="168" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">4</text>
  <text x="160" y="168" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN6</text>

  <!-- Pin 5: IN7 -->
  <line x1="170" y1="192" x2="240" y2="192" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="196" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">5</text>
  <text x="160" y="196" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN7</text>

  <!-- Pin 6: START -->
  <line x1="170" y1="220" x2="240" y2="220" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="224" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">6</text>
  <text x="160" y="224" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#dc2626">START</text>

  <!-- Pin 7: EOC -->
  <line x1="170" y1="248" x2="240" y2="248" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="252" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">7</text>
  <text x="160" y="252" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#dc2626">EOC (End of Conv)</text>

  <!-- Pin 8: 2^-4 (D3) -->
  <line x1="170" y1="276" x2="240" y2="276" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="280" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">8</text>
  <text x="160" y="280" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#16a34a">D3 (2⁻⁴)</text>

  <!-- Pin 9: OE -->
  <line x1="170" y1="304" x2="240" y2="304" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="308" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">9</text>
  <text x="160" y="308" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#dc2626">OE (Output Enable)</text>

  <!-- Pin 10: CLK -->
  <line x1="170" y1="332" x2="240" y2="332" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="336" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">10</text>
  <text x="160" y="336" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#d97706">CLOCK (640kHz)</text>

  <!-- Pin 11: VCC -->
  <line x1="170" y1="360" x2="240" y2="360" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="364" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">11</text>
  <text x="160" y="364" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#ea580c">Vcc (+5V)</text>

  <!-- Pin 12: VREF(+) -->
  <line x1="170" y1="388" x2="240" y2="388" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="392" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">12</text>
  <text x="160" y="392" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#ea580c">Vref (+) (+5V)</text>

  <!-- Pin 13: GND -->
  <line x1="170" y1="416" x2="240" y2="416" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="420" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">13</text>
  <text x="160" y="420" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#334155">GND (0V)</text>

  <!-- Pin 14: 2^-6 (D1) -->
  <line x1="170" y1="444" x2="240" y2="444" stroke="#64748b" stroke-width="2"/>
  <text x="230" y="448" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">14</text>
  <text x="160" y="448" text-anchor="end" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#16a34a">D1 (2⁻⁶)</text>

  <!-- PINS RIGHT (28 to 15) -->
  <!-- Pin 28: IN2 -->
  <line x1="440" y1="80" x2="510" y2="80" stroke="#64748b" stroke-width="2"/>
  <text x="250" y="84" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc" style="display:none;"></text>
  <text x="450" y="84" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">28</text>
  <text x="520" y="84" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN2</text>

  <!-- Pin 27: IN1 -->
  <line x1="440" y1="108" x2="510" y2="108" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="112" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">27</text>
  <text x="520" y="112" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN1</text>

  <!-- Pin 26: IN0 -->
  <line x1="440" y1="136" x2="510" y2="136" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="140" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">26</text>
  <text x="520" y="140" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0284c7">IN0</text>

  <!-- Pin 25: ADD A -->
  <line x1="440" y1="164" x2="510" y2="164" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="168" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">25</text>
  <text x="520" y="168" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#7c3aed">ADD A (LSB)</text>

  <!-- Pin 24: ADD B -->
  <line x1="440" y1="192" x2="510" y2="192" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="196" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">24</text>
  <text x="520" y="196" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#7c3aed">ADD B</text>

  <!-- Pin 23: ADD C -->
  <line x1="440" y1="220" x2="510" y2="220" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="224" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">23</text>
  <text x="520" y="224" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#7c3aed">ADD C (MSB)</text>

  <!-- Pin 22: ALE -->
  <line x1="440" y1="248" x2="510" y2="248" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="252" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">22</text>
  <text x="520" y="252" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#dc2626">ALE (Addr Latch En)</text>

  <!-- Pin 21: 2^-1 (D7 MSB) -->
  <line x1="440" y1="276" x2="510" y2="276" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="280" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">21</text>
  <text x="520" y="280" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#16a34a">D7 (2⁻¹ / MSB)</text>

  <!-- Pin 20: 2^-2 (D6) -->
  <line x1="440" y1="304" x2="510" y2="304" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="308" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">20</text>
  <text x="520" y="308" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#16a34a">D6 (2⁻²)</text>

  <!-- Pin 19: 2^-3 (D5) -->
  <line x1="440" y1="332" x2="510" y2="332" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="336" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">19</text>
  <text x="520" y="336" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#16a34a">D5 (2⁻³)</text>

  <!-- Pin 18: 2^-4 (D4) -->
  <line x1="440" y1="360" x2="510" y2="360" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="364" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">18</text>
  <text x="520" y="364" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#16a34a">D4 (2⁻⁴)</text>

  <!-- Pin 17: 2^-5 (D2) -->
  <line x1="440" y1="388" x2="510" y2="388" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="392" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">17</text>
  <text x="520" y="392" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#16a34a">D2 (2⁻⁵)</text>

  <!-- Pin 16: VREF(-) -->
  <line x1="440" y1="416" x2="510" y2="416" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="420" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">16</text>
  <text x="520" y="420" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#ea580c">Vref (-) (0V)</text>

  <!-- Pin 15: 2^-8 (D0 LSB) -->
  <line x1="440" y1="444" x2="510" y2="444" stroke="#64748b" stroke-width="2"/>
  <text x="450" y="448" font-family="monospace" font-size="10" font-weight="bold" fill="#f8fafc">15</text>
  <text x="520" y="448" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#16a34a">D0 (2⁻⁸ / LSB)</text>

  <!-- Color Key at Bottom -->
  <rect x="30" y="488" width="620" height="24" rx="4" fill="#f8fafc" stroke="#e2e8f0"/>
  <circle cx="50" cy="500" r="5" fill="#0284c7"/><text x="60" y="504" font-family="system-ui, sans-serif" font-size="10">Analog Inputs (IN0-IN7)</text>
  <circle cx="190" cy="500" r="5" fill="#dc2626"/><text x="200" y="504" font-family="system-ui, sans-serif" font-size="10">Control Signals</text>
  <circle cx="295" cy="500" r="5" fill="#7c3aed"/><text x="305" y="504" font-family="system-ui, sans-serif" font-size="10">Address Inputs</text>
  <circle cx="400" cy="500" r="5" fill="#16a34a"/><text x="410" y="504" font-family="system-ui, sans-serif" font-size="10">Digital Outputs (D0-D7)</text>
  <circle cx="535" cy="500" r="5" fill="#ea580c"/><text x="545" y="504" font-family="system-ui, sans-serif" font-size="10">Power &amp; Vref</text>
</svg>
</div>'''

svg_output_devices_block = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 280" width="100%" height="auto" style="max-width:740px; background:#ffffff; border:1px solid #cbd5e1; border-radius:8px;">
  <defs>
    <marker id="arrow-out" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#475569" />
    </marker>
  </defs>
  <!-- Main Title -->
  <text x="370" y="24" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" font-weight="700" fill="#0f172a">Interfacing Digital &amp; Analog Output Devices</text>

  <!-- PATH 1: DIGITAL OUTPUT -->
  <text x="30" y="52" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#2563eb">A. Digital Output Interfacing Path</text>
  
  <rect x="30" y="65" width="130" height="55" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="95" y="88" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#1e40af">Microcontroller</text>
  <text x="95" y="104" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#1e40af">GPIO Port (Output)</text>

  <line x1="160" y1="92" x2="215" y2="92" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-out)"/>
  <text x="187" y="84" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">HIGH/LOW</text>

  <rect x="220" y="65" width="160" height="55" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="300" y="88" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#92400e">Driver / Isolation</text>
  <text x="300" y="104" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#92400e">(Transistor, Relay, Optocoupler)</text>

  <line x1="380" y1="92" x2="435" y2="92" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-out)"/>
  <text x="407" y="84" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">Power Drive</text>

  <rect x="440" y="65" width="270" height="55" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="575" y="88" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#14532d">Digital Actuators / Displays</text>
  <text x="575" y="104" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#14532d">LED, Buzzer, 16×2 LCD, Relay Coil, Solenoid</text>

  <!-- PATH 2: ANALOG OUTPUT -->
  <text x="30" y="162" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#9333ea">B. Analog Output Interfacing Path (True DAC vs PWM)</text>

  <rect x="30" y="175" width="130" height="75" rx="6" fill="#ede9fe" stroke="#8b5cf6" stroke-width="1.5"/>
  <text x="95" y="200" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#581c87">Microcontroller</text>
  <text x="95" y="218" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#581c87">• Data Bus (D0-D7)</text>
  <text x="95" y="234" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#581c87">• PWM Timer Output</text>

  <line x1="160" y1="212" x2="215" y2="212" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-out)"/>
  <text x="187" y="204" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">Digital code / PWM</text>

  <rect x="220" y="175" width="160" height="75" rx="6" fill="#fce7f3" stroke="#ec4899" stroke-width="1.5"/>
  <text x="300" y="198" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#831843">Conversion Stage</text>
  <text x="300" y="216" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#831843">1. DAC (e.g. DAC0808) + Op-Amp</text>
  <text x="300" y="232" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#831843">2. RC Low-Pass Filter (for PWM)</text>

  <line x1="380" y1="212" x2="435" y2="212" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow-out)"/>
  <text x="407" y="204" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">Smooth V_out</text>

  <rect x="440" y="175" width="270" height="75" rx="6" fill="#ffedd5" stroke="#ea580c" stroke-width="1.5"/>
  <text x="575" y="198" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#7c2d12">Analog Actuator / System</text>
  <text x="575" y="216" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#7c2d12">DC Motor Speed (PWM/H-Bridge),</text>
  <text x="575" y="232" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#7c2d12">LED Dimmer, Audio Speaker, Function Gen</text>
</svg>
</div>'''

svg_dac_triangular = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 420" width="100%" height="auto" style="max-width:760px; background:#ffffff; border:1px solid #cbd5e1; border-radius:8px;">
  <defs>
    <marker id="arr-dac" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#1e293b" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="380" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" font-weight="700" fill="#0f172a">Interfacing Circuit: Triangular Waveform Generation using DAC0808 + Op-Amp</text>
  <text x="380" y="44" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Digital-to-Analog Converter (DAC0808) connected as Current Source with Op-Amp I-to-V Converter</text>

  <!-- Block 1: Microcontroller -->
  <rect x="20" y="70" width="120" height="200" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="80" y="100" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#1d4ed8">MCU / 8051</text>
  <text x="80" y="118" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#3b82f6">(Port 1 / Port D)</text>
  <line x1="30" y1="130" x2="130" y2="130" stroke="#93c5fd" stroke-width="1"/>
  <text x="80" y="155" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="600" fill="#1e40af">Counter Loop:</text>
  <text x="80" y="175" text-anchor="middle" font-family="monospace" font-size="10" fill="#1e40af">00H → FFH</text>
  <text x="80" y="195" text-anchor="middle" font-family="monospace" font-size="10" fill="#1e40af">FFH → 00H</text>
  <text x="80" y="235" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">Generates symmetric</text>
  <text x="80" y="248" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">digital ramp values</text>

  <!-- Bus line from MCU to DAC -->
  <line x1="140" y1="170" x2="215" y2="170" stroke="#1e293b" stroke-width="3" marker-end="url(#arr-dac)"/>
  <text x="178" y="162" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" fill="#0f172a">8-Bit Bus (D0–D7)</text>

  <!-- Block 2: DAC0808 -->
  <rect x="220" y="70" width="190" height="200" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="315" y="98" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#b45309">DAC 0808</text>
  <text x="315" y="114" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#92400e">8-Bit Multiplying DAC</text>

  <!-- DAC pin labels inside -->
  <text x="228" y="140" font-family="monospace" font-size="9" fill="#451a03">A1(MSB)...A8(LSB)</text>
  <text x="228" y="165" font-family="monospace" font-size="9" fill="#451a03">Pin 14: Vref(+) = +5V (via 5kΩ)</text>
  <text x="228" y="185" font-family="monospace" font-size="9" fill="#451a03">Pin 15: Vref(-) = GND</text>
  <text x="228" y="205" font-family="monospace" font-size="9" fill="#451a03">Pin 13: Vcc = +5V / +12V</text>
  <text x="228" y="225" font-family="monospace" font-size="9" fill="#451a03">Pin 3:  Vee = -12V / -15V</text>
  <text x="228" y="245" font-family="monospace" font-size="9" fill="#451a03">Pin 16: Comp Cap (0.1µF to -Vee)</text>

  <!-- Output Current Pin 4 -->
  <text x="402" y="174" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#b45309">Pin 4 (Iout)</text>
  <line x1="410" y1="170" x2="480" y2="170" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-dac)"/>
  <text x="445" y="160" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" fill="#dc2626">I_out</text>

  <!-- Block 3: Op-Amp (I to V Converter) -->
  <!-- Triangle Op-Amp -->
  <polygon points="485,130 485,210 555,170" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="495" y="155" font-family="monospace" font-size="14" font-weight="bold" fill="#14532d">-</text>
  <text x="495" y="195" font-family="monospace" font-size="14" font-weight="bold" fill="#14532d">+</text>
  <text x="515" y="173" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" font-weight="bold" fill="#14532d">LM741</text>
  <text x="515" y="185" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" fill="#14532d">Op-Amp</text>

  <!-- Non-inverting (+) connected to GND -->
  <line x1="485" y1="190" x2="465" y2="190" stroke="#334155" stroke-width="1.5"/>
  <line x1="465" y1="190" x2="465" y2="205" stroke="#334155" stroke-width="1.5"/>
  <line x1="455" y1="205" x2="475" y2="205" stroke="#334155" stroke-width="2"/>
  <line x1="460" y1="209" x2="470" y2="209" stroke="#334155" stroke-width="1.5"/>
  <line x1="463" y1="213" x2="467" y2="213" stroke="#334155" stroke-width="1"/>

  <!-- Inverting (-) connection -->
  <line x1="480" y1="170" x2="480" y2="150" stroke="#dc2626" stroke-width="1.5"/>
  <line x1="480" y1="150" x2="485" y2="150" stroke="#dc2626" stroke-width="1.5"/>

  <!-- Feedback Resistor Rf across Op-Amp -->
  <line x1="475" y1="150" x2="475" y2="110" stroke="#16a34a" stroke-width="1.5"/>
  <line x1="475" y1="110" x2="510" y2="110" stroke="#16a34a" stroke-width="1.5"/>
  <rect x="510" y="103" width="30" height="14" fill="#ffffff" stroke="#16a34a" stroke-width="1.5"/>
  <text x="525" y="98" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#16a34a">Rf = 5kΩ</text>
  <line x1="540" y1="110" x2="575" y2="110" stroke="#16a34a" stroke-width="1.5"/>
  <line x1="575" y1="110" x2="575" y2="170" stroke="#16a34a" stroke-width="1.5"/>

  <!-- Op-Amp Output line -->
  <line x1="555" y1="170" x2="600" y2="170" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-dac)"/>
  <circle cx="605" cy="170" r="3" fill="#16a34a"/>
  <text x="615" y="174" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#16a34a">V_out</text>

  <!-- Output Waveform Display Panel on Right -->
  <rect x="600" y="70" width="140" height="200" rx="6" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="670" y="94" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="#0f172a">Output Waveform</text>
  <!-- Axes -->
  <line x1="615" y1="210" x2="725" y2="210" stroke="#64748b" stroke-width="1.5"/>
  <line x1="615" y1="210" x2="615" y2="115" stroke="#64748b" stroke-width="1.5"/>
  <text x="612" y="125" text-anchor="end" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">+5V</text>
  <text x="612" y="213" text-anchor="end" font-family="system-ui, sans-serif" font-size="9" fill="#64748b">0V</text>
  <text x="725" y="222" font-family="system-ui, sans-serif" font-size="8" fill="#64748b">t</text>
  <!-- Triangular Wave Curve -->
  <polyline points="620,205 645,130 670,205 695,130 720,205" fill="none" stroke="#dc2626" stroke-width="2.5"/>
  <text x="670" y="240" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#dc2626">Period T = 512 × t_step</text>
  <text x="670" y="255" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#dc2626">f = 1 / T</text>

  <!-- Bottom Algorithm Box -->
  <rect x="20" y="285" width="720" height="120" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="35" y="306" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#1e293b">Triangular Wave Generation Mathematical Principle:</text>
  <text x="35" y="326" font-family="system-ui, sans-serif" font-size="11" fill="#334155">• Output Voltage Formula: V_out = I_out × R_f = V_ref × (R_f / R_ref) × (Digital Value / 256)</text>
  <text x="35" y="344" font-family="system-ui, sans-serif" font-size="11" fill="#334155">• For R_f = R_ref = 5kΩ and V_ref = +5V: Step Size = 5V / 256 ≈ 19.53 mV per LSB count.</text>
  <text x="35" y="362" font-family="system-ui, sans-serif" font-size="11" fill="#334155">• Ramp-UP Phase: Microcontroller counts UP from 00H (0V) to FFH (≈5V), incrementing by 1 each step with a fixed delay.</text>
  <text x="35" y="380" font-family="system-ui, sans-serif" font-size="11" fill="#334155">• Ramp-DOWN Phase: Microcontroller counts DOWN from FFH (≈5V) to 00H (0V), decrementing by 1 each step with the same delay.</text>
  <text x="35" y="398" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#0f172a">• Continuous infinite repetition produces a perfectly linear, symmetric triangular waveform.</text>
</svg>
</div>'''

svg_stepper_motor = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 460" width="100%" height="auto" style="max-width:740px; background:#ffffff; border:1px solid #cbd5e1; border-radius:8px;">
  <defs>
    <marker id="arr-step" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#334155" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="370" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" font-weight="700" fill="#0f172a">Stepper Motor Interfacing with ULN2003 Driver Circuit</text>
  <text x="370" y="44" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Current amplification and back-EMF protection using Darlington Transistor Array</text>

  <!-- MCU Block -->
  <rect x="20" y="70" width="120" height="230" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="80" y="100" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#1d4ed8">MCU</text>
  <text x="80" y="118" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#3b82f6">(Arduino / 8051)</text>

  <!-- MCU Pin lines -->
  <text x="125" y="155" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#1e3a8a">P1.0 (IN1)</text>
  <text x="125" y="195" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#1e3a8a">P1.1 (IN2)</text>
  <text x="125" y="235" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#1e3a8a">P1.2 (IN3)</text>
  <text x="125" y="275" text-anchor="end" font-family="monospace" font-size="10" font-weight="bold" fill="#1e3a8a">P1.3 (IN4)</text>

  <!-- Connecting lines MCU -> ULN -->
  <line x1="140" y1="150" x2="200" y2="150" stroke="#334155" stroke-width="1.5" marker-end="url(#arr-step)"/>
  <line x1="140" y1="190" x2="200" y2="190" stroke="#334155" stroke-width="1.5" marker-end="url(#arr-step)"/>
  <line x1="140" y1="230" x2="200" y2="230" stroke="#334155" stroke-width="1.5" marker-end="url(#arr-step)"/>
  <line x1="140" y1="270" x2="200" y2="270" stroke="#334155" stroke-width="1.5" marker-end="url(#arr-step)"/>

  <!-- ULN2003 Driver IC Block -->
  <rect x="205" y="70" width="180" height="230" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="295" y="98" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" font-weight="700" fill="#b45309">ULN 2003</text>
  <text x="295" y="114" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#92400e">Darlington Transistor Array</text>
  <text x="295" y="130" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#92400e">(500mA per channel, 50V)</text>

  <!-- ULN Input/Output Pin labels -->
  <text x="215" y="154" font-family="monospace" font-size="9" fill="#78350f">1B (IN1) → 1C (OUT1)</text>
  <text x="215" y="194" font-family="monospace" font-size="9" fill="#78350f">2B (IN2) → 2C (OUT2)</text>
  <text x="215" y="234" font-family="monospace" font-size="9" fill="#78350f">3B (IN3) → 3C (OUT3)</text>
  <text x="215" y="274" font-family="monospace" font-size="9" fill="#78350f">4B (IN4) → 4C (OUT4)</text>

  <!-- Flyback clamp diode & COM pin note -->
  <rect x="215" y="285" width="160" height="12" rx="2" fill="#fed7aa"/>
  <text x="295" y="294" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" font-weight="bold" fill="#7c2d12">Pin 9 (COM): Free-wheeling Diodes</text>

  <!-- Connecting lines ULN -> Motor Coils -->
  <line x1="385" y1="150" x2="450" y2="150" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-step)"/>
  <text x="415" y="142" text-anchor="middle" font-family="monospace" font-size="9" fill="#dc2626">Coil A</text>

  <line x1="385" y1="190" x2="450" y2="190" stroke="#d97706" stroke-width="2" marker-end="url(#arr-step)"/>
  <text x="415" y="182" text-anchor="middle" font-family="monospace" font-size="9" fill="#d97706">Coil B</text>

  <line x1="385" y1="230" x2="450" y2="230" stroke="#16a34a" stroke-width="2" marker-end="url(#arr-step)"/>
  <text x="415" y="222" text-anchor="middle" font-family="monospace" font-size="9" fill="#16a34a">Coil C</text>

  <line x1="385" y1="270" x2="450" y2="270" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-step)"/>
  <text x="415" y="262" text-anchor="middle" font-family="monospace" font-size="9" fill="#2563eb">Coil D</text>

  <!-- Stepper Motor Block -->
  <rect x="455" y="70" width="265" height="230" rx="6" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
  <text x="585" y="96" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#0f172a">4-Phase Unipolar Stepper Motor</text>
  <text x="585" y="112" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#475569">(e.g. 28BYJ-48, 5-Wire)</text>

  <!-- Stator Motor graphic circle -->
  <circle cx="585" cy="195" r="60" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
  <!-- Rotor -->
  <circle cx="585" cy="195" r="24" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
  <circle cx="585" cy="195" r="8" fill="#1e293b"/>
  <text x="585" y="198" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#ffffff">ROTOR</text>
  <!-- Rotor teeth -->
  <line x1="585" y1="171" x2="585" y2="165" stroke="#1e293b" stroke-width="3"/>
  <line x1="585" y1="219" x2="585" y2="225" stroke="#1e293b" stroke-width="3"/>
  <line x1="561" y1="195" x2="555" y2="195" stroke="#1e293b" stroke-width="3"/>
  <line x1="609" y1="195" x2="615" y2="195" stroke="#1e293b" stroke-width="3"/>

  <!-- Stator Coils -->
  <rect x="575" y="137" width="20" height="12" fill="#fca5a5" stroke="#dc2626"/>
  <text x="585" y="133" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" font-weight="bold" fill="#dc2626">A</text>

  <rect x="633" y="185" width="12" height="20" fill="#fed7aa" stroke="#d97706"/>
  <text x="652" y="198" font-family="system-ui, sans-serif" font-size="8" font-weight="bold" fill="#d97706">B</text>

  <rect x="575" y="241" width="20" height="12" fill="#bbf7d0" stroke="#16a34a"/>
  <text x="585" y="263" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" font-weight="bold" fill="#16a34a">C</text>

  <rect x="525" y="185" width="12" height="20" fill="#bfdbfe" stroke="#2563eb"/>
  <text x="520" y="198" text-anchor="end" font-family="system-ui, sans-serif" font-size="8" font-weight="bold" fill="#2563eb">D</text>

  <!-- Power Line +12V Vcc -->
  <line x1="385" y1="288" x2="585" y2="288" stroke="#dc2626" stroke-width="2"/>
  <text x="480" y="284" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#dc2626">+12V Supply Rail (COM)</text>

  <!-- Bottom Table: Stepping Sequence -->
  <rect x="20" y="320" width="700" height="125" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="35" y="340" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#0f172a">Excitation Stepping Sequences (4-Step vs 8-Step):</text>
  
  <text x="35" y="362" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#1d4ed8">• 4-Step Full Drive (2-Phase ON - Maximum Torque):</text>
  <text x="50" y="380" font-family="monospace" font-size="10" fill="#334155">Step 1: 1100b (0x0C) → Step 2: 0110b (0x06) → Step 3: 0011b (0x03) → Step 4: 1001b (0x09) [Repeat]</text>

  <text x="35" y="402" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#059669">• 4-Step Wave Drive (1-Phase ON - Lowest Power):</text>
  <text x="50" y="418" font-family="monospace" font-size="10" fill="#334155">Step 1: 1000b (0x08) → Step 2: 0100b (0x04) → Step 3: 0010b (0x02) → Step 4: 0001b (0x01) [Repeat]</text>

  <text x="35" y="438" font-family="system-ui, sans-serif" font-size="10" fill="#64748b">* Reverse step sequence for Counter-Clockwise (CCW) rotation. Change delay between steps to control RPM.</text>
</svg>
</div>'''

svg_signal_conditioning = '''<div class="svg-container" style="text-align:center; margin:20px 0;">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 380" width="100%" height="auto" style="max-width:760px; background:#ffffff; border:1px solid #cbd5e1; border-radius:8px;">
  <defs>
    <marker id="arr-sc" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#1e293b" />
    </marker>
  </defs>

  <!-- Title -->
  <text x="380" y="26" text-anchor="middle" font-family="system-ui, sans-serif" font-size="15" font-weight="700" fill="#0f172a">Complete 5-Stage Signal Conditioning Chain for Sensor Interfacing</text>
  <text x="380" y="44" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Sensor (e.g. ECG / Soil Moisture) → Operational Amplifier → Low-Pass Filter → Notch Filter → Clean ADC Input</text>

  <!-- STAGE 1: Sensor -->
  <rect x="15" y="65" width="125" height="120" rx="6" fill="#fee2e2" stroke="#ef4444" stroke-width="2"/>
  <text x="77" y="90" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#991b1b">Stage 1: Sensor</text>
  <text x="77" y="108" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#b91c1c">ECG / Soil Sensor</text>
  <!-- Mini waveform: very small & noisy -->
  <path d="M 25 150 Q 35 145 45 150 T 60 148 T 75 135 T 85 160 T 95 150 T 115 150" fill="none" stroke="#ef4444" stroke-width="1.5"/>
  <text x="77" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#991b1b">Weak &amp; Corrupted</text>
  <text x="77" y="186" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" fill="#7f1d1d">(2mV–100mV + Hum)</text>

  <line x1="140" y1="125" x2="160" y2="125" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-sc)"/>

  <!-- STAGE 2: Amplifier -->
  <rect x="165" y="65" width="130" height="120" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="230" y="90" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#92400e">Stage 2: Op-Amp</text>
  <text x="230" y="108" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#b45309">Non-Inverting Amp</text>
  <!-- Mini waveform: large & noisy -->
  <path d="M 175 150 Q 185 135 195 150 T 215 110 T 235 175 T 255 145 T 285 150" fill="none" stroke="#d97706" stroke-width="1.5"/>
  <text x="230" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#92400e">Amplified + Noise</text>
  <text x="230" y="186" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" fill="#78350f">Gain Av = 1 + Rf/R1</text>

  <line x1="295" y1="125" x2="315" y2="125" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-sc)"/>

  <!-- STAGE 3: Low Pass Filter -->
  <rect x="320" y="65" width="130" height="120" rx="6" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="385" y="90" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#14532d">Stage 3: LPF</text>
  <text x="385" y="108" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#15803d">Passive / Active RC</text>
  <!-- Mini waveform: smooth QRS + 50Hz ripple -->
  <path d="M 330 150 Q 345 155 355 150 T 375 115 T 395 165 T 415 150 T 440 150" fill="none" stroke="#16a34a" stroke-width="2"/>
  <text x="385" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#14532d">HF Noise Removed</text>
  <text x="385" y="186" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" fill="#14532d">fc = 1 / (2πRC)</text>

  <line x1="450" y1="125" x2="470" y2="125" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-sc)"/>

  <!-- STAGE 4: Notch Filter -->
  <rect x="475" y="65" width="130" height="120" rx="6" fill="#ede9fe" stroke="#8b5cf6" stroke-width="2"/>
  <text x="540" y="90" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#581c87">Stage 4: Notch</text>
  <text x="540" y="108" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#6d28d9">Twin-T Band-Stop</text>
  <!-- Mini waveform: perfectly clean ECG wave -->
  <path d="M 485 150 Q 500 150 510 148 L 520 152 L 530 115 L 540 170 L 550 150 Q 565 140 575 150 L 595 150" fill="none" stroke="#7c3aed" stroke-width="2"/>
  <text x="540" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#581c87">50Hz Hum Removed</text>
  <text x="540" y="186" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" fill="#4c1d95">f0 = 1 / (2πRC) = 50Hz</text>

  <line x1="605" y1="125" x2="625" y2="125" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-sc)"/>

  <!-- STAGE 5: ADC / MCU -->
  <rect x="630" y="65" width="115" height="120" rx="6" fill="#eff6ff" stroke="#3b82f6" stroke-width="2"/>
  <text x="687" y="90" text-anchor="middle" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#1e40af">Stage 5: ADC</text>
  <text x="687" y="108" text-anchor="middle" font-family="system-ui, sans-serif" font-size="10" fill="#2563eb">Microcontroller</text>
  <!-- Quantized digital levels -->
  <path d="M 640 155 H 650 V 140 H 660 V 115 H 670 V 165 H 685 V 150 H 705 V 145 H 735" fill="none" stroke="#2563eb" stroke-width="2"/>
  <text x="687" y="175" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" font-weight="bold" fill="#1e40af">Clean Digital Data</text>
  <text x="687" y="186" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" fill="#1e3a8a">(0–1023 / 0–4095)</text>

  <!-- Detailed Functional Stage Description Table -->
  <rect x="15" y="200" width="730" height="165" rx="6" fill="#f8fafc" stroke="#cbd5e1"/>
  <text x="30" y="222" font-family="system-ui, sans-serif" font-size="12" font-weight="700" fill="#0f172a">Summary of Roles in the Signal Conditioning Chain:</text>

  <text x="30" y="244" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#b45309">1. Amplifier (Op-Amp):</text>
  <text x="175" y="244" font-family="system-ui, sans-serif" font-size="11" fill="#334155">Provides voltage gain to scale millivolt-level transducer outputs to the 0–5V (or 0–3.3V) input span of the ADC.</text>
  <text x="175" y="258" font-family="system-ui, sans-serif" font-size="10" fill="#64748b">Provides high input impedance (preventing sensor loading) and low output impedance to drive subsequent stages.</text>

  <text x="30" y="278" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#15803d">2. Low-Pass Filter (LPF):</text>
  <text x="175" y="278" font-family="system-ui, sans-serif" font-size="11" fill="#334155">Eliminates high-frequency noise, radio-frequency interference, and switching transients above the desired signal bandwidth.</text>
  <text x="175" y="292" font-family="system-ui, sans-serif" font-size="10" fill="#64748b">Functions as an anti-aliasing filter to ensure compliance with the Nyquist sampling criterion (fs ≥ 2·fmax).</text>

  <text x="30" y="312" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#6d28d9">3. Notch Filter (Band-Stop):</text>
  <text x="175" y="312" font-family="system-ui, sans-serif" font-size="11" fill="#334155">Sharply rejects the pervasive 50 Hz (or 60 Hz) power-line electrical hum radiating from mains wiring without distorting the signal.</text>
  <text x="175" y="326" font-family="system-ui, sans-serif" font-size="10" fill="#64748b">High Q-factor Twin-T topology creates a deep attenuation notch (-40 dB to -60 dB) exactly at f0 = 50 Hz.</text>

  <text x="30" y="348" font-family="system-ui, sans-serif" font-size="10" font-weight="600" fill="#0f172a">Design Rule Formulas:</text>
  <text x="175" y="348" font-family="monospace" font-size="10" fill="#0f172a">Gain = 1 + (Rf / R1)   |   fc(LPF) = 1 / (2π · R_lpf · C)   |   f0(Notch) = 1 / (2π · R_notch · C) = 50 Hz</text>
</svg>
</div>'''

print("SVGs loaded successfully!")
