# Modern Manga Translator - UI Rework

## การออกแบบ UI ใหม่

### 🎨 คุณสมบัติใหม่

1. **Modern Dark Theme**
   - สีสันทันสมัย (Indigo + Slate)
   - คอนทราสต์สูง อ่านง่าย
   - รองรับ High DPI

2. **Component-Based Architecture**
   - แยก Components ออกมาชัดเจน
   - ใช้ซ้ำได้ (Reusable)
   - Maintain ง่าย

3. **Improved Navigation**
   - Sidebar ใหม่ ใช้งานง่าย
   - Quick Actions
   - Keyboard Shortcuts

4. **Better UX**
   - Animation เล็กน้อย
   - Visual Feedback
   - Responsive Layout

### 📁 โครงสร้างไฟล์ใหม่

```
ui/
├── themes/                    # ระบบ Theme
│   ├── __init__.py
│   └── modern_theme.py       # Color Palette & Styles
├── components/                # UI Components
│   ├── __init__.py
│   ├── modern_button.py      # Buttons with animations
│   ├── modern_card.py        # Card containers
│   ├── modern_sidebar.py     # New Sidebar
│   └── modern_slider.py      # Custom sliders
├── layouts/                   # Layout templates
├── main_window_new.py        # MainWindow ใหม่
└── ...

launch_modern.py              # Launcher ใหม่
launch_modern.bat            # Windows Batch file
```

### 🚀 การใช้งาน

#### รัน UI ใหม่:
```batch
launch_modern.bat
```

#### รันด้วย Project:
```batch
launch_modern.bat --proj-dir "C:\Path\To\Project"
```

#### Debug Mode:
```batch
launch_modern.bat --debug
```

### ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open Project |
| `Ctrl+S` | Save Project |
| `Ctrl+T` | Toggle Text Panel |
| `Ctrl+B` | Toggle Sidebar |
| `D` | Run Detection |
| `O` | Run OCR |
| `I` | Run Inpainting |

### 🎨 Theme Customization

สามารถปรับแต่งสีได้ที่ `ui/themes/modern_theme.py`:

```python
colors = ThemeColors(
    primary="#6366f1",        # สีหลัก
    bg_primary="#0f172a",     # พื้นหลังหลัก
    text_primary="#f8fafc",   # สีข้อความ
    accent_success="#22c55e", # สีสำเร็จ
    accent_error="#ef4444",   # สีผิดพลาด
)
```

### 🧩 Components

#### ModernButton
```python
from ui.components import ModernButton

btn = ModernButton("Click Me", primary=True)
```

#### ModernCard
```python
from ui.components import ModernCard

card = ModernCard("Title")
card.add_widget(content)
```

#### ModernSlider
```python
from ui.components import ModernSlider

slider = ModernSlider("Opacity", 0, 100, 50)
slider.value_changed.connect(on_value_change)
```

### 🔄 Migration Guide

หากต้องการกลับไปใช้ UI เดิม:
```batch
launch_win.bat
```

UI ใหม่ถูกออกแบบให้ทำงานแยกจาก UI เดิม ไม่กระทบกัน

### 🐛 Troubleshooting

#### ปัญหา: Module not found
```bash
# ตรวจสอบว่าอยู่ในโฟลเดอร์ถูกต้อง
cd C:\Users\dansa\Desktop\AI\ModernMangaTranslator
python launch_modern.py
```

#### ปัญหา: Qt Platform Plugin
ติดตั้ง PyQt6 หรือ PySide6:
```bash
pip install PyQt6
```

### 📝 Notes

- UI ใหม่ยังอยู่ในช่วงพัฒนา (Beta)
- ฟีเจอร์บางอย่างอาจยังไม่สมบูรณ์
- สามารถใช้ UI เดิมได้ตามปกติ
