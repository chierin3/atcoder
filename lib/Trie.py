# トライ木の実装
# 文字列sの接頭辞を管理する
# 問題によって、Nodeのexecメソッドを変更する必要がある
class Trie:
    class Node:
        def __init__(self, root):
            self.root = root
            self.child = dict()
        # 以下は問題によって変更する必要がある
            self.f = False
            self.Z = set()

        def exec(self, id, flag):
            if flag:
                self.Z.add(id)
                if self.f:
                    self.root.Z.add(id)
            else:
                self.f = True
                self.root.Z |= self.Z
                self.Z.clear() 

    def __init__(self):
        self.root = self.Node(None)

    def add(self, s, id, flag):
        node = self.root
        for c in s:
            if c not in node.child:
                node.child[c] = self.Node(self.root)
            node = node.child[c]
            if flag:
                node.exec(id, flag)
        node.exec(id, flag)

Q = int(input())
trie = Trie()
Y = 0
for i in range(Q):
    T, S = input().rstrip().split()
    trie.add(S, i, T == "2")
    if T == "2":
        Y += 1
    print(Y - len(trie.root.Z))