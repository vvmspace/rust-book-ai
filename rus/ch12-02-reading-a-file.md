# Чтение файла

Теперь нам нужно прочитать файл.
Сначала создайте файл `poem.txt` в корне проекта (рядом с `src`, а не внутри):

```text
I'm Nobody! Who are you?
Are you - Nobody - too?
Then there's a pair of us!
Don't tell! they'd advertise - you know!
```

### Читаем

Используем `std::fs`.

```rust
use std::env;
use std::fs;

fn main() {
    // ... чтение аргументов ...
    let args: Vec<String> = env::args().collect();
    let query = &args[1];
    let file_path = &args[2];

    println!("In file {}", file_path);

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    println!("With text:\n{contents}");
}
```

`fs::read_to_string` открывает файл, читает его целиком в `String` и возвращает `Result`.
Всё просто, как 5 копеек. Но `main` уже становится жирноват. Пора рефакторить!

---

**JavaScript Analogy:**

> `fs::read_to_string(path)` — это полный аналог `fs.readFileSync(path, 'utf8')` в Node.js.
> Читает весь файл синхронно и возвращает строку.





---

**English Joke:**

> How many programmers does it take to change a light bulb?
> None, that's a hardware problem.
