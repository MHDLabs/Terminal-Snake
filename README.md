# 🐍 Terminal Snake

A small and lightweight **Snake game for the terminal**, written in pure Python using `curses`.

No GUI. No external packages. Just a terminal, Python, and a little snake. 😄

---

## ✨ Features

* 🎮 Arrow keys and **WASD** controls
* 🍎 Food spawning with `*`
* 🐍 Snake rendered directly inside the terminal
* 🧮 Score tracking
* 💀 Wall and self-collision detection
* 🔄 Restart the game after `GAME OVER`
* 📐 Handles terminal resizing
* ⚡ Simple and lightweight
* 📦 No external Python dependencies

---

## 🇬🇧 English

### Requirements

* Python **3.x**
* A terminal with `curses` support

This project uses only Python's standard library, so no `pip install` is required.

It is intended primarily for **Linux and other Unix-like systems**.

---

### ▶️ Run

Clone the repository:

```bash
git clone https://github.com/MHDLabs/Terminal-Snake.git
cd terminal-snake
```

Run the game:

```bash
python3 main.py
```

That's it. 🐍

You can also run it directly because `main.py` already includes a Python shebang:

```bash
chmod +x main.py
./main.py
```

---

### 🎮 Controls

| Key     | Action                  |
| ------- | ----------------------- |
| `↑` `W` | Move up                 |
| `↓` `S` | Move down               |
| `←` `A` | Move left               |
| `→` `D` | Move right              |
| `R`     | Restart after game over |
| `Q`     | Quit                    |

`Ctrl+C` can also be used to exit.

---

### 🕹️ How the game works

You start with a small snake.

Move around the terminal and collect the food represented by:

```text
*
```

Your snake is represented by:

```text
O
```

Every time you eat food:

* Your score increases by `1`
* The snake grows
* A new food position is generated

The game ends when:

* You hit the edge of the terminal
* You collide with your own body
* The snake fills the entire available play area

After `GAME OVER`, press `R` to start again.

There is no wall wrapping, so hitting a terminal edge ends the game.

---

### 📐 Terminal resizing

The game detects terminal resize events.

When the terminal size changes, the game rebuilds the board using the new dimensions while keeping the current score.

For the best experience, use a reasonably sized terminal window.

If the terminal becomes too small, the game waits until there is enough space to continue.

---

### ⚙️ Project structure

```text
terminal-snake/
├── LICENSE
├── README.md
└── main.py
```

---

### 🧪 Check the source before running

You can verify that the Python file has no syntax errors:

```bash
python3 -m py_compile main.py
```

If the command finishes without output, the syntax check passed.

---

### 📦 Dependencies

There are **no third-party dependencies**.

The game uses:

* `random`
* `sys`
* `time`
* `curses`

All of these are part of Python's standard library on supported Unix-like systems.

---

### 📝 License

This project is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

---

## 🇮🇷 فارسی

# 🐍 Terminal Snake

یک بازی ساده و سبک **Snake برای ترمینال** که با Python و `curses` نوشته شده.

نه رابط گرافیکی داره، نه پکیج اضافه‌ای لازم داره؛ فقط یک ترمینال، Python و یک مار که دنبال غذا می‌گرده. 😄

---

## ✨ امکانات

* 🎮 کنترل با کلیدهای جهت و **WASD**
* 🍎 نمایش غذا با `*`
* 🐍 اجرای کامل بازی داخل ترمینال
* 🧮 نمایش امتیاز
* 💀 تشخیص برخورد با دیواره و بدن مار
* 🔄 امکان Restart بعد از باخت
* 📐 پشتیبانی از تغییر اندازه ترمینال
* ⚡ سبک و سریع
* 📦 بدون نیاز به پکیج‌های جانبی Python

---

## پیش‌نیازها

* Python **3.x**
* یک ترمینال دارای پشتیبانی از `curses`

هیچ پکیج اضافه‌ای با `pip` لازم نیست.

این پروژه عمدتاً برای **Linux و سیستم‌های Unix-like** طراحی شده است.

---

## ▶️ اجرا

ریپو را Clone کنید:

```bash
git clone https://github.com/YOUR-USERNAME/terminal-snake.git
cd terminal-snake
```

سپس اجرا کنید:

```bash
python3 main.py
```

همین. 🐍

از آنجا که فایل `main.py` دارای shebang است، می‌توانید آن را مستقیماً هم اجرا کنید:

```bash
chmod +x main.py
./main.py
```

---

## 🎮 کنترل‌ها

| کلید    | عملکرد                  |
| ------- | ----------------------- |
| `↑` `W` | حرکت به بالا            |
| `↓` `S` | حرکت به پایین           |
| `←` `A` | حرکت به چپ              |
| `→` `D` | حرکت به راست            |
| `R`     | شروع دوباره بعد از باخت |
| `Q`     | خروج                    |

برای خروج، `Ctrl+C` هم قابل استفاده است.

---

## 🕹️ نحوه بازی

بازی با یک مار کوچک شروع می‌شود.

هدف این است که در محیط ترمینال حرکت کنید و غذا را که با این علامت نمایش داده می‌شود بخورید:

```text
*
```

خود مار نیز با این کاراکتر نمایش داده می‌شود:

```text
O
```

با هر بار خوردن غذا:

* امتیاز شما `1` واحد افزایش پیدا می‌کند.
* اندازه مار بیشتر می‌شود.
* غذا در یک موقعیت جدید ظاهر می‌شود.

بازی در شرایط زیر تمام می‌شود:

* برخورد با لبه ترمینال
* برخورد مار با بدن خودش
* پر شدن تمام فضای قابل‌بازی توسط مار

بعد از `GAME OVER` می‌توانید با زدن `R` دوباره بازی را شروع کنید.

در این نسخه Wrap وجود ندارد؛ یعنی برخورد با لبه صفحه باعث باخت می‌شود.

---

## 📐 تغییر اندازه ترمینال

بازی تغییر اندازه ترمینال را تشخیص می‌دهد.

اگر اندازه پنجره ترمینال تغییر کند، محیط بازی با اندازه جدید دوباره ساخته می‌شود و امتیاز فعلی حفظ می‌شود.

برای تجربه بهتر، بهتر است بازی را در یک پنجره ترمینال با اندازه مناسب اجرا کنید.

اگر پنجره بیش از حد کوچک شود، بازی تا زمانی که فضای کافی ایجاد شود منتظر می‌ماند.

---

## ⚙️ ساختار پروژه

```text
terminal-snake/
├── LICENSE
├── README.md
└── main.py
```

---

## 🧪 بررسی خطاهای Syntax

قبل از اجرا می‌توانید صحت Syntax فایل Python را بررسی کنید:

```bash
python3 -m py_compile main.py
```

اگر این دستور هیچ خروجی‌ای نشان ندهد، بررسی Syntax با موفقیت انجام شده است.

---

## 📦 وابستگی‌ها

این پروژه **هیچ وابستگی خارجی** ندارد.

ماژول‌های استفاده‌شده:

* `random`
* `sys`
* `time`
* `curses`

همه این‌ها بخشی از کتابخانه استاندارد Python در سیستم‌های Unix-like پشتیبانی‌شده هستند.

---

## 📝 مجوز

این پروژه تحت مجوز **MIT License** منتشر شده است.

متن کامل مجوز را در فایل [`LICENSE`](LICENSE) ببینید.
