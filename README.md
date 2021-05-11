# Words Search Comparison

This program implements Binary Search Tree.

As there are many words, recursion does not work, that is why the required methods are written with iterations usage.

This program allows to compare the search of 10,000 random words in:
- a list;
- a binary tree, the elements of which were added sequently;
- a binary tree, the elements of which were added randomly;
- a balanced binary tree.

The result of the comparison on a file with 11k words gives the results:
> The slowest way is the search in an ordered binary tree.
> The search in a list is faster.
> The search in a disordered binary tree is much faster.
> The search in a balanced tree is the fastest.

The program shows the time tiken for each search method and the number of words (10,000)
to demonstrate that they appear in every case.