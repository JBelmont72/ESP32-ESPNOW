


Excellent — now we can move to the **second half of Day 4: File Handling (read + write)**
This will give you the final tools needed before we step into Days 5–7 and eventually BLE commands.

---

# ✅ **DAY 4 — PART 2: File Handling**

MicroPython and normal Python both support file operations:

* **write** → create or overwrite a file
* **append** → add to the end
* **read** → read all contents
* **readline** → read line by line

Here is your mini-toolkit.

---

# ⭐ 1. **Write to a file**

```python
with open("log.txt", "w") as f:
    f.write("Hello file!\n")
    f.write("Line #2\n")
```

This **creates** or **overwrites** `log.txt`.

---

# ⭐ 2. **Append to a file**

```python
with open("log.txt", "a") as f:
    f.write("Appended line\n")
```

This **adds** without deleting old content.

---

# ⭐ 3. **Read a whole file**

```python
with open("log.txt", "r") as f:
    data = f.read()
    print(data)
```

---

# ⭐ 4. **Read line by line**

```python
with open("log.txt") as f:
    for line in f:
        print("LINE:", line.strip())
```

---

# ⭐ 5. **Using a helper function (important)**

Just like your `tools.shout()`, you can make **file helper modules**.

Create a file: `file_tools.py`

```python
def save(filename, text):
    with open(filename, "a") as f:
        f.write(text + "\n")

def load(filename):
    with open(filename) as f:
        return f.read()
```

Now you can use it:

```python
import file_tools

file_tools.save("notes.txt", "My first saved note!")
print(file_tools.load("notes.txt"))
```

---

# ⭐ 6. **Your small exercise (very quick)**

Create a module:

**grades_file.py**

```
def add_grade(value):
    with open("grades.txt", "a") as f:
        f.write(str(value) + "\n")

def read_grades():
    with open("grades.txt") as f:
        return [float(x) for x in f]
```

Then write another file:

```
import grades_file

grades_file.add_grade(85)
grades_file.add_grade(92)

print(grades_file.read_grades())
```

---

# ⭐ When you're done, just send:

**done**

Then we proceed to **Day 5 (advanced data structures)** — the part that prepares you for the BLE command system.
