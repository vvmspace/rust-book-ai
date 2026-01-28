# Рефакторинг: Улучшаем модульность и обработку ошибок

Наш код работает, но `main` превратился в кашу.
Проблемы:

1.  `main` делает всё: парсит аргументы, читает файлы.
2.  Переменные разбросаны.
3.  Ошибки (`expect`) малоинформативны.

### Разделение ответственности

Мы вынесем логику в `src/lib.rs`, а в `src/main.rs` оставим только запуск.
Это стандартный паттерн в Rust для бинарных приложений.

### Config Struct

Вместо кучи переменных создадим структуру:

```rust
struct Config {
    query: String,
    file_path: String,
}

impl Config {
    fn build(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }
        // ...
        Ok(Config { ... })
    }
}
```

### Обработка ошибок в main

Теперь `main` выглядит чисто:

```rust
fn main() {
    let args: Vec<String> = env::args().collect();

    let config = Config::build(&args).unwrap_or_else(|err| {
        eprintln!("Problem parsing arguments: {err}");
        process::exit(1);
    });

    if let Err(e) = minigrep::run(config) {
        eprintln!("Application error: {e}");
        process::exit(1);
    }
}
```

`unwrap_or_else` позволяет нам обработать ошибку без паники (без страшного стектрейса для пользователя).

---

**JavaScript Analogy:**

> Это как если бы мы взяли огромный `index.js`, в котором всё в кучу, и вынесли бизнес-логику в `lib.js` (module.exports), а в `index.js` оставили только вызов этой логики и обработку `process.exit(1)` в случае ошибок.





---

**English Joke:**

> Refactoring is like cleaning the house.
> You hide the trash under the sofa so it looks better.
