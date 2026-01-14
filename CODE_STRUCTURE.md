# 🏗️ Code Structure

This document explains the architecture of HampterLiker.

## 📐 Architecture Overview

HampterLiker follows **functional programming principles** with clean separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│                    User Interfaces                   │
│  ┌──────────────┐              ┌─────────────────┐ │
│  │   gui.py     │              │    app.py       │ │
│  │  (Desktop)   │              │  (Web Flask)    │ │
│  └──────┬───────┘              └────────┬────────┘ │
└─────────┼────────────────────────────────┼─────────┘
          │                                │
          └────────────┬───────────────────┘
                       │
          ┌────────────▼─────────────┐
          │   youtube_service.py     │
          │  (Pure Business Logic)   │
          └────────────┬─────────────┘
                       │
          ┌────────────▼─────────────┐
          │      config.py           │
          │   (Configuration)        │
          └──────────────────────────┘
```

## 📦 Module Breakdown

### `config.py` - Configuration Layer
**Purpose:** Immutable configuration management

**Key Features:**
- `@dataclass(frozen=True)` for immutability
- Factory methods for defaults
- Type-safe configuration

```python
@dataclass(frozen=True)
class YouTubeConfig:
    scopes: List[str]
    api_service_name: str
    api_version: str
```

### `youtube_service.py` - Business Logic Layer
**Purpose:** Pure functional YouTube API operations

**Key Concepts:**
- **Pure Functions:** No side effects where possible
- **Immutable Data:** All data structures are frozen dataclasses
- **Type Hints:** Full type annotations
- **Composition:** Small functions that compose together

**Data Structures:**
```python
@dataclass(frozen=True)
class Channel:
    id: str
    handle: str

@dataclass(frozen=True)
class Video:
    id: str

@dataclass(frozen=True)
class LikeResult:
    video_id: str
    success: bool
    error: Optional[str] = None
```

**Function Categories:**
1. **File Operations:** `find_client_secret_files()`, `get_first_client_secret()`
2. **Authentication:** `create_authenticated_service()`, `get_authenticated_service()`
3. **Channel Lookup:** `lookup_channel_by_handle()`, `find_channel()`
4. **Video Operations:** `fetch_channel_videos()`, `like_videos()`
5. **High-Level Workflows:** `like_all_channel_videos()`

### `gui.py` - Desktop Interface
**Purpose:** Standalone tkinter GUI

**Architecture:**
- **Class-based:** `HampterLikerGUI` class
- **Thread-safe:** Queue-based messaging between threads
- **Event-driven:** Tkinter event loop + background workers

**Key Components:**
```python
class HampterLikerGUI:
    - _create_widgets()      # Build UI
    - _run_workflow()        # Background worker
    - _process_messages()    # Handle updates
```

### `app.py` - Web Interface
**Purpose:** Flask web application

**Architecture:**
- **Immutable State:** `ProgressState` dataclass with `with_*` methods
- **Thread-safe:** `ProgressManager` with locks
- **RESTful API:** JSON endpoints for status updates

**Key Components:**
```python
class ProcessStatus(Enum):
    IDLE, AUTHENTICATING, FETCHING, LIKING, COMPLETED, ERROR

@dataclass
class ProgressState:
    - with_status()    # Immutable state update
    - with_progress()  # Immutable progress update
```

## 🎯 Functional Programming Patterns Used

### 1. Immutable Data Structures
```python
@dataclass(frozen=True)
class Channel:
    id: str
    handle: str
```

### 2. Pure Functions
```python
def clean_handle(handle: str) -> str:
    """Pure function - same input always gives same output."""
    return handle.lstrip('@')
```

### 3. Higher-Order Functions
```python
def like_videos_with_callback(
    youtube: Any,
    videos: List[Video],
    on_progress: Callable[[int, int, Video], None]
) -> List[LikeResult]:
    """Function that takes another function as parameter."""
```

### 4. Function Composition
```python
def like_all_channel_videos(youtube, handle, on_progress):
    """Composed workflow of smaller functions."""
    channel = find_channel(youtube, handle)
    videos = fetch_channel_videos(youtube, channel.id)
    results = like_videos_with_callback(youtube, videos, on_progress)
    return (channel, videos, results)
```

### 5. List Comprehensions & Map/Filter
```python
def extract_video_ids(response: Dict[str, Any]) -> List[str]:
    return [item["id"]["videoId"] for item in response.get("items", [])]
```

### 6. Strategy Pattern
```python
lookup_strategies = [
    lookup_channel_by_handle,
    lookup_channel_by_username
]
for strategy in lookup_strategies:
    result = strategy(youtube, cleaned)
    if result:
        return Channel(id=result["id"], handle=handle)
```

## 🧪 Testing Strategy

### Unit Tests (Recommended)
```python
def test_clean_handle():
    assert clean_handle("@hampter") == "hampter"
    assert clean_handle("hampter") == "hampter"

def test_extract_video_ids():
    response = {"items": [{"id": {"videoId": "abc123"}}]}
    assert extract_video_ids(response) == ["abc123"]
```

### Integration Tests
```python
def test_find_channel():
    # Mock YouTube service
    # Test channel lookup with different handles
    pass
```

## 🔒 Thread Safety

### GUI (tkinter)
- Uses `Queue` for thread-safe communication
- Background worker thread for YouTube API calls
- Main thread handles UI updates

### Web (Flask)
- `ProgressManager` with `threading.Lock`
- Immutable state snapshots
- Thread-safe state updates

## 📊 Data Flow

### Desktop GUI Flow:
```
User Input → GUI Thread → Queue → Worker Thread
                ↑                      ↓
            UI Updates ← Queue ← Progress Updates
```

### Web UI Flow:
```
User Request → Flask Route → Background Thread
                 ↑                    ↓
            Progress API ← ProgressManager ← Updates
```

## 🎨 Design Principles

1. **Immutability First:** Use frozen dataclasses
2. **Pure Functions:** Minimize side effects
3. **Type Safety:** Type hints everywhere
4. **Composition:** Build complex from simple
5. **Single Responsibility:** Each function does one thing
6. **Documentation:** Docstrings on all public functions

## 🚀 Performance Considerations

- **Pagination:** Uses `reduce` for functional pagination
- **Threading:** Background workers prevent UI blocking
- **Rate Limiting:** Respects YouTube API limits
- **Caching:** OAuth tokens cached automatically

## 🔄 Future Improvements

- [ ] Add result caching with `functools.lru_cache`
- [ ] Implement retry logic with exponential backoff
- [ ] Add async/await for concurrent API calls
- [ ] Create pure functional state machine for progress
- [ ] Add property-based testing with Hypothesis

---

**Built with 💕 using functional programming principles**
