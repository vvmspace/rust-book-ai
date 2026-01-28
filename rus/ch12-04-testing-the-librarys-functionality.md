# TDD: Разработка через тестирование

Теперь, когда у нас есть `lib.rs`, мы можем писать тесты!
Мы будем использовать **TDD** (Test-Driven Development):

1.  Пишем тест, который падает.
2.  Пишем код, чтобы тест прошел.
3.  Рефакторим.
4.  Повторяем.

### Пишем тест

В `src/lib.rs`:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_result() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }
}
```

### Реализуем search

```rust
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.contains(query) {
            results.push(line);
        }
    }

    results
}
```

Заметьте лайфтайм `'a`. Мы говорим: "Результаты будут жить столько же, сколько исходный текст `contents`". Это логично, ведь мы возвращаем ссылки на строки из `contents`.

---

**JavaScript Analogy:**

> Это классический цикл Red-Green-Refactor, как в Jest или Mocha.
> Мы пишем `test('should find matching lines', ...)` перед тем, как реализовать функцию `search`.





---

**English Joke:**

> Test-driven development is like double-entry bookkeeping.
> You do everything twice to make sure you didn't screw up.
