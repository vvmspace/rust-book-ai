# Cargo Workspaces (Рабочие пространства)

Когда проект растет, его хочется разбить на несколько библиотек.
Cargo Workspace позволяет управлять несколькими пакетами (крейтами), которые делят один `Cargo.lock` и одну директорию `target`.

### Создание
`Cargo.toml` в корне:

```toml
[workspace]
members = [
    "adder",
    "add_one",
]
```

Это гарантирует, что все крейты в воркспейсе используют совместимые версии зависимостей.

### Тестирование
```bash
cargo test
```
Запустит тесты для всех крейтов в воркспейсе.

---

**JavaScript Analogy:**

> Это как Monorepo в мире JS (Lerna, Nx, Turborepo, Yarn Workspaces).
> У вас куча пакетов в одной репе, и они "дружат" друг с другом, используя общие зависимости.





---

**English Joke:**

> One does not simply merge a monorepo.
