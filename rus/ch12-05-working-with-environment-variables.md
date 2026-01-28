# Работа с переменными окружения

Мы хотим добавить фичу: поиск без учета регистра.
Но мы не хотим передавать лишний аргумент каждый раз. Давайте используем переменную окружения!

### TDD: Тест для регистронезависимого поиска

В `src/lib.rs` добавляем новый тест `case_insensitive`:

```rust
#[test]
fn case_insensitive() {
    let query = "rUsT";
    let contents = "\
Rust:
safe, fast, productive.
Pick three.
Trust me.";

    assert_eq!(
        vec!["Rust:", "Trust me."],
        search_case_insensitive(query, contents)
    );
}
```

### Реализация

```rust
pub fn search_case_insensitive<'a>(
    query: &str,
    contents: &'a str,
) -> Vec<&'a str> {
    let query = query.to_lowercase();
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            results.push(line);
        }
    }

    results
}
```

Заметьте: `to_lowercase` создает новую `String`, поэтому `query` теперь владеет данными.

### Чтение переменной окружения

В `src/main.rs`:

```rust
use std::env;

impl Config {
    pub fn build(args: &[String]) -> Result<Config, &'static str> {
        // ...
        let ignore_case = env::var("IGNORE_CASE").is_ok();

        Ok(Config {
            query,
            file_path,
            ignore_case,
        })
    }
}
```

`env::var` возвращает `Result`. Если переменная есть — `Ok`.

Запуск:
```bash
IGNORE_CASE=1 cargo run -- to poem.txt
```

---

**JavaScript Analogy:**

> `env::var("KEY")` — это как `process.env.KEY` в Node.js.
> Только в Rust мы получаем `Result`, потому что переменной может не быть, или она может содержать невалидный Unicode (в Windows такое бывает, но `env::var` паникует на невалидном Unicode, используйте `var_os` для безопасности).





---

**English Joke:**

> Why do programmers prefer dark mode?
> Because light attracts bugs.
