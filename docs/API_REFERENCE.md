# Ground Control Station API Reference

## Web Server (Flask + Socket.IO)

**URL:** `http://<gcs_ip>:5000`  
**Auth:** API key header (optional) — `X-API-Key: flyingwing2025`

---

## REST API Endpoints

### Health Check

```
GET /api/status
```

**Response:**
```json
{
  "status": "online",
  "uptime": 3600,
  "connected": true
}
```

---

### Telemetry

```
GET /api/telemetry
```

**Response:**
```json
{
  "timestamp": 1234567890,
  "lat": 21.0285,
  "lng": 105.8542,
  "alt": 100.5,
  "heading": 180.0,
  "groundspeed": 15.2,
  "airspeed": 16.0,
  "battery_voltage": 22.4,
  "battery_remaining": 75,
  "gps_fix": 3,
  "satellites": 12,
  "mode": "AUTO",
  "armed": true
}
```

---

### Image Upload

```
POST /api/image
Content-Type: multipart/form-data
```

**Body:**
- `image` — JPEG/PNG image file
- `timestamp` — Unix timestamp
- `lat` — Latitude
- `lng` — Longitude
- `alt` — Altitude

**Response:**
```json
{
  "status": "ok",
  "filename": "img_20260423_103000.jpg"
}
```

---

### Detection Results

```
POST /api/detection
Content-Type: application/json
```

**Body:**
```json
{
  "timestamp": 1234567890,
  "detections": [
    {
      "class": "person",
      "confidence": 0.85,
      "bbox": [100, 150, 200, 300],
      "gps": {"lat": 21.0285, "lng": 105.8542}
    }
  ]
}
```

---

### Target Tracking

```
POST /api/target
Content-Type: application/json
```

**Body:**
```json
{
  "timestamp": 1234567890,
  "target_id": 1,
  "class": "person",
  "confidence": 0.85,
  "gps": {"lat": 21.0285, "lng": 105.8542},
  "bbox": [100, 150, 200, 300]
}
```

---

### Commands

```
POST /api/command
Content-Type: application/json
```

**Body:**
```json
{
  "command": "arm",
  "params": {}
}
```

**Available commands:**

| Command | Params | Description |
|---------|--------|-------------|
| `arm` | — | Arm motors |
| `disarm` | — | Disarm motors |
| `takeoff` | `altitude` | Takeoff to altitude (m) |
| `land` | — | Land at current position |
| `rth` | — | Return to home |
| `goto` | `lat`, `lng`, `alt` | Navigate to waypoint |
| `loiter` | `radius`, `altitude` | Circle at current position |
| `set_mode` | `mode` | Set flight mode |

**Flight modes:** `MANUAL`, `FBWA`, `AUTO`, `LOITER`, `RTL`, `GUIDED`

---

## WebSocket Events (Socket.IO)

### Server → Client

| Event | Data | Description |
|-------|------|-------------|
| `telemetry_update` | Telemetry object | Real-time telemetry |
| `new_image` | `{filename, timestamp, gps}` | New image captured |
| `new_detection` | Detection results | AI detection results |
| `target_update` | Target tracking data | Target position update |
| `status_change` | `{state, message}` | System status change |

### Client → Server

| Event | Data | Description |
|-------|------|-------------|
| `subscribe` | `{topic}` | Subscribe to updates |
| `command` | Command object | Send command |

---

## MAVLink Communication

**Serial:** `/dev/serial0` @ 921600 baud  
**Protocol:** MAVLink 2.0

### Supported Messages

| Message | Direction | Description |
|---------|-----------|-------------|
| `HEARTBEAT` | Both | Connection heartbeat |
| `ATTITUDE` | FC→CC | Roll, pitch, yaw |
| `GPS_RAW_INT` | FC→CC | Raw GPS data |
| `GLOBAL_POSITION_INT` | FC→CC | Filtered position |
| `SYS_STATUS` | FC→CC | System status |
| `BATTERY_STATUS` | FC→CC | Battery info |
| `MISSION_*` | Both | Mission management |
| `COMMAND_LONG` | CC→FC | Send commands |
| `COMMAND_ACK` | FC→CC | Command acknowledgment |

### Custom Messages (IDs 10001-10003)

| ID | Description |
|----|-------------|
| 10001 | AI detection results |
| 10002 | Target tracking data |
| 10003 | System health metrics |

---

## RC Mode Controller

**Channels:**

| Channel | Function | PWM Range |
|---------|----------|-----------|
| CH5 (AUX1) | AI Mode Select | 1300/1500/1700 |
| CH6 (AUX2) | AI Frequency | 1300/1500/1700 |
| CH7 (AUX3) | AI Confidence | 1300/1500/1700 |
| CH8 (AUX4) | AI Target Select | 1300/1500/1700 |

**AI Modes:**

| Mode | Frequency | Targets | Confidence |
|------|-----------|---------|------------|
| Search & Rescue | Every 5 frames | person/boat/vehicle | 0.7 |
| People Counting | Every 30 frames | person | 0.6 |
| Vehicle Counting | Every 30 frames | car/truck/bus | 0.6 |
| Reconnaissance | Every 15 frames | person/vehicle/building | 0.5 |
| Manual | Disabled | — | — |

---

## Python API (Companion Computer)

### Main Entry Point

```python
from src.main import CompanionComputer

computer = CompanionComputer(config_path="config/")
computer.start()  # Starts 3-thread pipeline
computer.stop()
```

### AI Detection

```python
from src.ai.adaptive_detector import AdaptiveDetector

detector = AdaptiveDetector(model_path="models/mobilenet_v2.tflite")
detector.start()
detections = detector.get_latest_detections()
```

### Navigation

```python
from src.navigation.geolocation import Geolocation

geo = Geolocation(camera_fov_h=54, camera_fov_v=41)
target_gps = geo.calculate_target_gps(
    bbox=[100, 150, 200, 300],
    uav_lat=21.0285, uav_lng=105.8542, uav_alt=100,
    uav_heading=180, uav_pitch=-20
)
```

### Safety

```python
from src.safety.geofencing import GeofenceManager

gf = GeofenceManager()
gf.load_from_json("geofence_config.json")
action = gf.check_position(lat, lng, alt)
# Returns: WARN, RTH, LOITER, LAND, GUIDED_RETURN
```
