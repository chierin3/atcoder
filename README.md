# AtCoder Python Libraries

AtCoderで使用する再利用可能なPythonライブラリを管理するリポジトリです。

## 構成

- `library/`: 提出コードにコピーして使えるライブラリ
- `tests/`: ライブラリの動作確認用テスト

## 使用例

```python
from library.union_find import UnionFind

uf = UnionFind(5)
uf.union(0, 1)
print(uf.same(0, 1))  # True
```

## テスト

```sh
python -m unittest discover -s tests
```
