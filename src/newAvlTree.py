from typing import TypeVar, Generic, Optional, Generator

T = TypeVar('T')

# Generic tree node class 
class TreeNode(Generic[T]):
    val: T
    parent: 'TreeNode[T]'
    left: 'TreeNode[T]'
    right: 'TreeNode[T]'
    height: int 
    
    def __init__(self, val: T, parent: Optional[T]): 
        self.val = val 
        self.left = None
        self.right = None
        self.height = 1
        self.parent = parent
  
# AVL tree class which supports the  
# Insert operation 
class AVL_Tree(Generic[T]): 
  
    # Recursive function to insert key in  
    # subtree rooted with node and returns 
    # new root of subtree. 
    def insert(self, root: Optional[TreeNode[T]], key: TreeNode[T], parent: Optional[TreeNode[T]] = None): 
      
        # Step 1 - Perform normal BST 
        if root is None: 
            return TreeNode(key, parent=parent) 
        elif key < root.val: 
            root.left = self.insert(root.left, key, parent=root) 
        else: 
            root.right = self.insert(root.right, key, parent=root) 
  
        # Step 2 - Update the height of the  
        # ancestor node 
        root.height = 1 + max(self.getHeight(root.left), 
                           self.getHeight(root.right)) 
  
        # Step 3 - Get the balance factor 
        balance = self.getBalance(root) 
  
        # Step 4 - If the node is unbalanced,  
        # then try out the 4 cases 
        # Case 1 - Left Left 
        if balance > 1 and key < root.left.val: 
            return self.rightRotate(root) 
  
        # Case 2 - Right Right 
        if balance < -1 and key > root.right.val: 
            return self.leftRotate(root) 
  
        # Case 3 - Left Right 
        if balance > 1 and key > root.left.val: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
  
        # Case 4 - Right Left 
        if balance < -1 and key < root.right.val: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
  
        return root 
    
    # Recursive function to delete a node with
    # given key from subtree with given root.
    # It returns root of the modified subtree.
    def delete(self, root: TreeNode[T], key):
 
        # Step 1 - Perform standard BST delete
        if root is None:
            return root
        elif key == root.val:
            if root.left is None:
                temp = root.right
                root = None
                return temp
 
            elif root.right is None:
                temp = root.left
                root = None
                return temp
 
            temp = self.getMinValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right,
                                      temp.val)
        elif key < root.val:
            root.left = self.delete(root.left, key)
        else:
            root.right = self.delete(root.right, key)
            
 
        # If the tree has only one node,
        # simply return it
        if root is None:
            return root
 
        # Step 2 - Update the height of the 
        # ancestor node
        root.height = 1 + max(self.getHeight(root.left),
                            self.getHeight(root.right))
 
        # Step 3 - Get the balance factor
        balance = self.getBalance(root)
 
        # Step 4 - If the node is unbalanced, 
        # then try out the 4 cases
        # Case 1 - Left Left
        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
 
        # Case 2 - Right Right
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
 
        # Case 3 - Left Right
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
 
        # Case 4 - Right Left
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)
 
        return root
    
    def getMinValueNode(self, root: TreeNode[T]):
        if root is None or root.left is None:
            return root
 
        return self.getMinValueNode(root.left)
  
    def leftRotate(self, z: TreeNode[T]): 
  
        y = z.right 
        T2 = y.left 
  
        # Perform rotation 
        y.left = z 
        z.right = T2 
  
        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                         self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                         self.getHeight(y.right)) 
  
        # Return the new root 
        return y 
  
    def rightRotate(self, z: TreeNode[T]): 
  
        y = z.left 
        t = y.right 
  
        # Perform rotation 
        y.right = z 
        z.left = t

  
        # Update heights 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 
  
        # Return the new root 
        return y 
  
    def getHeight(self, root: TreeNode[T]): 
        if not root: 
            return 0
  
        return root.height 
  
    def getBalance(self, root: TreeNode[T]): 
        if not root: 
            return 0
  
        return self.getHeight(root.left) - self.getHeight(root.right) 
  
    def inOrder(self, root: TreeNode[T]) -> Generator[T, None, None]:         
        if root is not None:
            yield from self.inOrder(root.left)
            yield root.val
            yield from self.inOrder(root.right)

    # Given a non-empty binary search tree, return the 
    # minimum data value found in that tree. Note that the
    # entire tree doesn't need to be searched
    def minValue(self, node: TreeNode[T]):
        current: TreeNode[T] = node
    
        # loop down to find the leftmost leaf
        while(current is not None):
            if current.left is None:
                break
            current = current.left
    
        return current


    def inOrderSuccessor(self, n: TreeNode[T]):
     
        # Step 1 of the above algorithm
        if n.right is not None:
            return self.minValue(n.right)
    
        # Step 2 of the above algorithm
        p = n.parent
        while( p is not None):
            if n != p.right :
                break
            n = p 
            p = p.parent
        return p
 
# This function finds predecessor and successor of key in BST
# It sets pre and suc as predecessor and successor respectively
def findPreSuc(root, key: TreeNode[T]):
 
    # Base Case
    if root is None:
        return
 
    # If key is present at root
    if root.val == key:
 
        # the maximum value in left subtree is predecessor
        if root.left is not None:
            tmp = root.left 
            while(tmp.right):
                tmp = tmp.right 
            findPreSuc.pre = tmp
 
 
        # the minimum value in right subtree is successor
        if root.right is not None:
            tmp = root.right
            while(tmp.left):
                tmp = tmp.left 
            findPreSuc.suc = tmp 
 
        return
 
    # If key is smaller than root's key, go to left subtree
    if root.val > key :
        findPreSuc.suc = root 
        findPreSuc(root.left, key)
 
    else: # go to right subtree
        findPreSuc.pre = root
        findPreSuc(root.right, key)