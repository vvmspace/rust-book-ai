# Пишем ошибки в stderr

Сейчас, если мы сделаем `cargo run > output.txt` и программа упадет, сообщение об ошибке тоже попадет в файл. Это плохо. Ошибки должны быть на экране!

### Stdout vs Stderr

*   `stdout` (стандартный вывод) — для полезных данных.
*   `stderr` (стандартный поток ошибок) — для логов и ошибок.

### `eprintln!`

В Rust есть макрос `eprintln!`, который пишет в `stderr`.
Меняем наши `println!` в блоках обработки ошибок в `main.rs`:

```rust
fn main() {
    // ...
    let config = Config::build(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}"); // Было println!
        process::exit(1);
    });

    if let Err(e) = minigrep::run(config) {
        eprintln!("Application error: {e}"); // Было println!
        process::exit(1);
    }
}
```

Всё! Теперь `cargo run > output.txt` запишет данные в файл, а ошибки покажет вам в консоль. Вы великолепны.

В следующей главе: Функциональные фичи Rust (итераторы и замыкания). Будет жарко.

---

**JavaScript Analogy:**

> `println!` — это `console.log`.
> `eprintln!` — это `console.error`.
> В Node.js они тоже пишут в разные потоки (`stdout` и `stderr` соответственно).





---

**English Joke:**

> There are two ways to write error-free programs; only the third one works.
