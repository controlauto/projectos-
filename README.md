# Building Automation & Controls Engineering — Projects

HVAC / BMS controls work on a multi-building commercial campus: field integration, control logic,
operator HMIs and tooling. The stack is built around **Home Assistant as an open BMS front end** on top of
BACnet/IP, Modbus, ESPHome/ESP32 controllers and Mitsubishi FX3U PLCs.

> All examples are sanitized. Site names, network addresses, device IDs and credentials are omitted.

**Core skills:** BACnet/IP & MS/TP · Modbus TCP/RTU · Home Assistant (YAML, templates, Lovelace) · ESPHome / ESP32 ·
Mitsubishi FX3U / GX Works2 · PID tuning & sequences of operation · Fault detection (FDD) & alarm design ·
Python automation · SVG / HMI design · Proxmox / Linux · CMMS (Limble)

---

## 1. Open BMS on Home Assistant (BACnet/IP)
Supervisory platform for 3 buildings: air handlers, steam and hot-water heat exchangers, a chiller plant,
a deaerator tank, UPS and parking-lot lighting. About 1,900 BACnet points.
- Shared **unified equipment status** sensors (RUNNING / ONLINE / STANDBY / ALARM / COMMS LOST / NO DATA).
  "Running" is only reported on **proven feedback** (CT, fan proof), never on command alone.
- **Industrial alarm panel** with priorities, acknowledge / shelve / disable and alarm history.
- Cleanup of orphaned and stale BACnet objects. Unavailable entities were cut by about 40%.

## 2. Fault detection & alarm engineering
- **AHU FDD:** space vs. return-air mismatch, sensor fallback logic, gated on fan proof to remove false night alarms.
- **Heat-exchanger alarms:** latching pump-proof failure (command ON and not proven within 7 s, cleared on proof),
  supply high temperature, sensor failure, valve saturated with low supply, and pump runtime service limits.
- Evidence-based diagnostics from trends: suspected valve leak-by, simultaneous heating/cooling, PID hunting,
  and a broken outdoor-air hysteresis that kept a heat exchanger locked out.

## 3. ESPHome / ESP32 field controllers
- AHU controller firmware with dual space sensors. It degrades gracefully to one sensor and has a safe AUTO mode
  (OA 0 % / RA 100 %) when data is invalid. Delivered via OTA.
- Heat-exchanger controllers with OAT enable/disable hysteresis, lead/lag pump rotation and fail-over on proof loss.
- **PLC simulator on ESP32** that reproduces a Mitsubishi FX3U pump station (I/O map, alarms, HMI registers),
  so ladder logic and HMI screens can be tested before going to site.

## 4. SCADA / HMI dashboards
- Generated **interactive SVG P&IDs**: concentric-impeller pumps, modulating valves, piping with flow indication.
  Animation runs only on proven feedback.
- **Campus "Home" overview generator (Python + JS):** single-source shared logic injected into every card, byte-identity
  guards, offline V8 rendering tests across 10 fault scenarios (panel down, comms lost, FDD, unknown states).
- Rotating TV display of plant views for the maintenance shop.

## 5. Automated, guarded deployment pipeline
- The dashboard generator was migrated into Home Assistant OS, in an isolated Python env running in an add-on.
- A nightly job (03:00 local) runs build → validate → V8 tests → publish **to staging only**, with a file lock,
  per-step and global timeouts, structured logs and 30-day retention.
- A WebSocket client allowlist makes writes to production and any equipment service call impossible by design.

## 6. AI-assisted operations (MCP)
- Model Context Protocol bridge for Home Assistant and config files. Diagnostics are read-only by default.
  Writes are two-phase (plan → diff → explicit approval) with automatic backups and protected interlock patterns.
- Integration with the **Limble CMMS** for work-order review and technical write-ups.

## 7. Infrastructure
- Proxmox VE homelab: Home Assistant VM, LXC services, Frigate NVR, Tailscale remote access.

---

### Engineering principles
Read-only by default · verify feedback vs. command · never bypass safeties or interlocks ·
back up before every change · document what changed and how it was verified.
