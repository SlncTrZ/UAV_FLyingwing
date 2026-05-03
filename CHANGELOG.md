# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- Modified Blended Wing Body (BWB) flying wing design
- Companion computer system (Raspberry Pi 3B+)
- AI edge processing với MobileNet SSD (~100ms/frame)
- Quantum-Inspired Kalman Filter (VQC 4-qubit, shadow mode)
- Hybrid GPS Denial System (15-state EKF + IMU + Airspeed)
- Ground Control Station với web dashboard
- MAVLink 2.0 communication protocol
- Geofencing system
- Pre-flight checklist
- SITL simulation scripts
- PID tuning scripts (stability, smoothness, balanced)
- Hardware wiring guide
- Radio master channel mixes
- Design calculations (aerodynamics, CG, BOM)
- 3D visualization plan
- Web server for telemetry
- Raspberry Pi deployment guide
- Companion computer deployment guide
- EKF implementation plan & deployment roadmap
- Comprehensive test suite (13 test files)

### Architecture
- 5 subsystems: companion_computer, ground_station, design_calculations, firmware, simulation
- Edge-first AI processing (no cloud dependency)
- Dual PID gaze tracking
- State-machine autonomous decision making
