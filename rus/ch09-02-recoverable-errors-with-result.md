# Поправимые ошибки и `Result`

Большинство ошибок не требуют смерти программы.
Если файл не открылся, может, его просто создать?

Для этого есть enum `Result`:
```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

### Использование `Result`

```rust
use std::fs::File;

let greeting_file_result = File::open("hello.txt");

let greeting_file = match greeting_file_result {
    Ok(file) => file,
    Err(error) => panic!("Problem opening the file: {:?}", error),
};
```

### Обработка разных ошибок

Мы можем матчить не только сам `Result`, но и тип ошибки внутри `Err`.

```rust
use std::io::ErrorKind;

match greeting_file_result {
    Ok(file) => file,
    Err(error) => match error.kind() {
        ErrorKind::NotFound => match File::create("hello.txt") {
            Ok(fc) => fc,
            Err(e) => panic!("Problem creating the file: {:?}", e),
        },
        other_error => panic!("Problem opening the file: {:?}", other_error),
    },
};
```
Много вложенности? Да. В главе 13 мы узнаем про замыкания (closures) и методы типа `unwrap_or_else`, которые сделают этот код чище.

### Шорткаты: `unwrap` и `expect`

- `unwrap()`: Если `Ok`, верни значение. Если `Err`, вызови `panic!`.
- `expect("msg")`: То же самое, но с вашим сообщением об ошибке. **Используйте `expect`, чтобы объяснить, почему вы считаете, что ошибки не будет.**

### Пробрасывание ошибок (Error Propagation)

Если ваша функция не может справиться с ошибкой, верните её вызывающему коду.

```rust
fn read_username_from_file() -> Result<String, io::Error> {
    let f = File::open("hello.txt");
    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e), // Возврат ошибки
    };
    // ...
}
```

### Оператор `?`

В Rust это настолько частый паттерн, что для него сделали оператор `?`.

```rust
fn read_username_from_file() -> Result<String, io::Error> {
    let mut s = String::new();
    File::open("hello.txt")?.read_to_string(&mut s)?;
    Ok(s)
}
```

`?` делает следующее:

- Если `Ok`, возвращает значение и продолжает.
- Если `Err`, **возвращает `Err` из функции** (early return).

Это работает, только если функция возвращает `Result` (или `Option`), совместимый с ошибкой.
В `main` тоже можно использовать `?`, если `main` возвращает `Result<(), Box<dyn Error>>`.

---

**Анекдот:**

> — Ты любишь рисковать?  
> — Я всегда использую `unwrap()`.  
> — Ого, да ты псих.  
> — На проде.  
> — (падает в обморок)
