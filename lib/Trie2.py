# トライ木の実装
# 文字列sの接頭辞を管理する
class Trie:
    class Node:
        def __init__(self, root):
            self.root = root
            self.child = dict()
            self.count = 0

    def __init__(self):
        self.root = self.Node(None)

    def add(self, s):
        node = self.root
        for c in s:
            if c not in node.child:
                node.child[c] = self.Node(self.root)
            node = node.child[c]
            node.count += 1

    def remove(self, s):
        node = self.root
        for c in s:
            if node.child[c].count == 1:
                del node.child[c]
                return
            node = node.child[c]
            node.count -= 1

    def exec(self, s):
        ans = 0
        node = self.root
        for c in s:
            if node.child[c].count <= 1:
                break
            node = node.child[c]
            ans += 1
        return ans

N = int(input())
S = [input() for _ in range(N)]
TRIE = Trie()
for s in S:
    TRIE.add(s)
for s in S:
    print(TRIE.exec(s))
