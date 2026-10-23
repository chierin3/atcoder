def rolling_list_2D(lst:list[list], n:int) -> list[list]:
    """
    2次元リストをn回回転させる
    :param lst: 2次元リスト
    :param n: 回転数
    :return: 回転後の2次元リスト
    """

    n = n % 4  # 4回回すと元に戻るため、nを4で割った余りを使用

    for _ in range(n):
        lst = [list(row) for row in zip(*lst[::-1])]
    return lst

A = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
print(rolling_list_2D(A, 1))  # 90度回転