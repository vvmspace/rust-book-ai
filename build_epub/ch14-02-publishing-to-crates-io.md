# Публикация крейта на Crates.io

Вы можете делиться своим кодом со всем миром через [crates.io](https://crates.io).

### Документация

Хороший тон — писать документацию.
Используйте `///` (три слеша) для doc-комментариев.
Они поддерживают Markdown.

```rust
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

Команда `cargo doc --open` сгенерирует красивый HTML и откроет его в браузере.
Крутая фишка: примеры кода в документации автоматически тестируются при запуске `cargo test`!

### Публикация

1.  Создайте аккаунт на crates.io (через GitHub).
2.  Залогиньтесь локально: `cargo login <token>`.
3.  Добавьте метаданные в `Cargo.toml` (`license`, `description`).
4.  `cargo publish`.

**Важно:** Опубликованный код удалить нельзя (можно только "yank" - пометить версию как устаревшую, чтобы новые проекты ее не подтягивали, но старые продолжали работать).

---

**JavaScript Analogy:**

> Crates.io — это NPM для Rust.
> `cargo publish` — это полный аналог `npm publish`.
> А `cargo login` похож на `npm login`.





---

**English Joke:**

> I don't always test my code, but when I do, I do it in production.
