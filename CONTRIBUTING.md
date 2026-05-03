# Contributing to Flying Wing UAV

Cảm ơn bạn đã quan tâm đến dự án Flying Wing UAV!

## Yêu cầu

- Python 3.9+
- (Optional) Raspberry Pi 3B+ cho companion computer
- (Optional) ArduPilot SITL cho simulation

## Thiết lập môi trường

```bash
# Clone repository
git clone https://github.com/truongcongdinh97/UAV_FLyingwing.git
cd UAV_FLyingwing

# Cài đặt dependencies
pip install -r requirements.txt

# Cài đặt dependencies cho subsystem
pip install -r companion_computer/requirements.txt
pip install -r ground_station/requirements.txt
pip install -r design_calculations/requirements.txt
```

## Kiến trúc dự án

```
UAV_FLyingwing/
├── companion_computer/    # AI edge processing (RPi 3B+)
│   ├── src/ai/           # Computer vision (MobileNet SSD)
│   ├── src/navigation/   # EKF dead reckoning
│   ├── src/quantum/      # Quantum-inspired Kalman filter
│   ├── src/safety/       # GPS monitor, failsafe
│   └── src/communication/# MAVLink protocol
├── ground_station/       # GCS với web dashboard
├── design_calculations/  # Aerodynamics, CG calculator
├── firmware/             # ArduPilot parameters
├── simulation/           # SITL simulation scripts
└── docs/                 # Documentation
```

## Quy trình phát triển

### 1. Tạo Branch

```bash
git checkout -b feature/ten-feature
```

### 2. Thực hiện thay đổi

- Tuân theo code style hiện có
- Viết tests cho module mới
- Cập nhật documentation

### 3. Kiểm tra

```bash
# Chạy companion computer tests
cd companion_computer && python run_all_tests.py

# Chạy ground station tests
cd ground_station && python -m pytest tests/ -v

# Chạy simulation
cd simulation && python run_sitl_test.py
```

### 4. Commit & Push

```bash
git add .
git commit -m "feat: mô tả ngắn gọn"
git push origin feature/ten-feature
```

## Subsystems

| Subsystem | Mô tả | Tài liệu |
|-----------|-------|----------|
| Companion Computer | AI edge processing trên RPi | `companion_computer/README.md` |
| Ground Station | Web dashboard + MAVLink | `ground_station/README.md` |
| Design Calculations | Aerodynamics + CG | `design_calculations/README.md` |
| Firmware | ArduPilot parameters | `firmware/README.md` |
| Simulation | SITL testing | `simulation/README_SITL.md` |

## Safety Guidelines

⚠️ **Quan trọng khi làm việc với UAV:**

- Luôn kiểm tra `docs/testing/PRE_FLIGHT_CHECKLIST.md` trước khi bay
- Test kỹ trong simulation trước khi deploy lên hardware
- Kiểm tra failsafe logic trong `companion_computer/src/safety/`
- Tuân thủ quy định bay UAV tại địa phương

## Commit Convention

| Prefix | Mô tả |
|--------|--------|
| `feat:` | Tính năng mới |
| `fix:` | Sửa bug |
| `docs:` | Documentation |
| `refactor:` | Refactor code |
| `test:` | Thêm/sửa tests |
| `safety:` | Thay đổi liên quan đến safety |
| `chore:` | Build, dependencies |
