# Улучшаем I/O проект

Теперь мы можем сделать наш `minigrep` красивее.

### Убираем clone

В `Config::build` мы делали клонирование строк, потому что у нас был слайс.
Теперь мы можем принять сам итератор `env::args()`!

```rust
impl Config {
    pub fn build(
        mut args: impl Iterator<Item = String>,
    ) -> Result<Config, &'static str> {
        args.next(); // Пропускаем имя программы

        let query = match args.next() {
            Some(arg) => arg,
            None => return Err("Didn't get a query string"),
        };
        // ...
    }
}
```

### Функциональный стиль в search

Было:
```rust
let mut results = Vec::new();
for line in contents.lines() {
    if line.contains(query) {
        results.push(line);
    }
}
results
```

Стало (красиво):
```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    contents
        .lines()
        .filter(|line| line.contains(query))
        .collect()
}
```

---

**JavaScript Analogy:**

> В JS/TS мы постоянно заменяем циклы `for` на `.filter(...).map(...)`.
> Здесь то же самое. Код становится декларативным: мы говорим *что* мы хотим получить, а не *как* это делать шаг за шагом.





---

**English Joke:**

> Why do programmers always mix up Halloween and Christmas?
> Because Oct 31 == Dec 25.
