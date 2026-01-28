# Принимаем аргументы командной строки

Создадим проект:
```bash
cargo new minigrep
cd minigrep
```

Мы хотим запускать его так:
```bash
cargo run -- searchstring example-filename.txt
```

### Чтение аргументов

Для этого нам нужен `std::env::args`.

```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    dbg!(args);
}
```

**Важно:**

*   `args[0]` — это имя самой программы (как в C или Node.js).
*   `args[1]` — первый реальный аргумент.

### Сохраняем в переменные

```rust
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    let query = &args[1];
    let file_path = &args[2];

    println!("Ищем: {}", query);
    println!("В файле: {}", file_path);
}
```
Пока что, если аргументов нет, программа запаникует при доступе к индексу. Это нормально, мы это починим позже.

---

**JavaScript Analogy:**

> `std::env::args()` в Rust — это аналог `process.argv` в Node.js.
> Только в Rust это итератор, который мы превращаем в массив (`Vec`) через `.collect()`.





---

**English Joke:**

> A SQL query walks into a bar, walks up to two tables and asks,
> "Can I join you?"
