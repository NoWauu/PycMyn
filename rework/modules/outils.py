"""module outils"""
from typing import List


def dichotomie(liste: List[float], valeur: float) -> int:
    """
    renvoie l'index d'une liste
    avec une recherche dichotomique
    >>> dichotomie([1, 2, 3], 2.5)
    2
    """
    if len(liste) == 0:
        # cas d'une liste vide
        return 0

    if len(liste) == 1:
        # les listes commencent à zéros
        return valeur >= liste[0]

    mid_index: int = len(liste)//2
    mid: float = liste[mid_index]

    if mid <= valeur:
        return mid_index + dichotomie(liste[mid_index:], valeur)
    else:
        return dichotomie(liste[:mid_index], valeur)
