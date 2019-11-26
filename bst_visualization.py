"""
Created on Sat Nov  9 13:53:08 2019

@author: danielb
"""

import logging
from tkinter import Tk, Toplevel, Frame, Label, Button, Entry
from helper_dictionaries import depth_colors, depth_size, depth_x_diff, depth_y_position

class Node():
    """Class that represents a node in the BST"""
    def __init__(self, passed_value):
        """Initialize the node"""
        self.data = passed_value
        self.parent = None
        self.right = None
        self.x_pos = None
        self.depth = None
        self.left = None


class BinarySearchTree():
    """Class that represents the binary search tree"""
    def __init__(self):
        """Initialize the tree"""
        self.root = None
        self.node_count = None

    def insert_node(self, value):
        """Insert a node into the BST"""
        # Make sure the node doesn't already exist in the tree
        if self.search_for_node(value) is not None:
            logging.warning("Node %i already exists in the BST", value)
            return

        # Create a new node
        new_node = Node(value)

        # Check if the tree is empty and, if so, create the root node
        if self.root is None:
            new_node.x_pos = 420
            new_node.depth = 0
            self.root = new_node
            return

        # Traverse the tree and find where the new node should be added
        temp = self.root
        while temp:
            if value < temp.data:
                if temp.left is None:
                    new_node.parent = temp
                    temp.left = new_node
                    return
                else:
                    temp = temp.left
            elif value > temp.data:
                if temp.right is None:
                    new_node.parent = temp
                    temp.right = new_node
                    return
                else:
                    temp = temp.right

    def delete_node(self, value):
        """Delete a node from the BST"""
        to_delete = self.search_for_node(value)
        if to_delete is None:
            logging.warning("Node %i not found", value)
            return

        # If node is a leaf node
        if to_delete.left is None and to_delete.right is None:
            if to_delete == self.root:
                del to_delete
                self.root = None
            else:
                if to_delete.parent.left == to_delete:
                    to_delete.parent.left = None
                elif to_delete.parent.right == to_delete:
                    to_delete.parent.right = None
                del to_delete

        # If node has two child nodes
        elif to_delete.left is not None and to_delete.right is not None:
            # Find in-order successor
            successor = self.min_value(to_delete.right)

            # Copy the successor's value and delete the node
            successor_data = successor.data
            self.delete_node(successor.data)

            # Copy the successor's data into the original to_delete node
            to_delete.data = successor_data

        # if node has one child node
        else:
            child = to_delete.left if to_delete.left is not None else to_delete.right
            if to_delete == self.root:
                child.x_pos = 380
                child.depth = 0
                self.root = child

            else:
                if to_delete.parent.left == to_delete:
                    to_delete.parent.left = child
                elif to_delete.parent.right == to_delete:
                    to_delete.parent.right = child
                child.parent = to_delete.parent
            del to_delete

    def search_for_node(self, value):
        """Searches for a node in the BST"""
        temp = self.root
        while temp:
            if temp.data == value:
                return temp
            elif value < temp.data:
                temp = temp.left
            elif value > temp.data:
                temp = temp.right
        return None

    def print_inorder(self, node):
        """In-order print of the BST"""
        if node.left is not None:
            self.print_inorder(node.left)
        print(node.data)
        if node.right is not None:
            self.print_inorder(node.right)

    def print_preorder(self, node):
        """Pre-order print of the BST"""
        print(node.data)
        if node.left is not None:
            self.print_inorder(node.left)
        if node.right is not None:
            self.print_inorder(node.right)

    def print_postorder(self, node):
        """Post-order print of the BST"""
        if node.left is not None:
            self.print_inorder(node.left)
        if node.right is not None:
            self.print_inorder(node.right)
        print(node.data)

    def min_value(self, node):
        """Finds and prints the miniumum value in the tree"""
        while node.left is not None:
            node = node.left
        return node

    def max_value(self, node):
        """Finds and prints the maximum value in the tree"""
        while node.right is not None:
            node = node.right
        return node

    def count_nodes(self, node):
        """Counts the nodes in the tree"""
        if node.left is not None:
            self.count_nodes(node.left)
        self.node_count += 1
        if node.right is not None:
            self.count_nodes(node.right)

    def print_helper(self, print_type):
        """Calls the appropriate print function"""
        if self.root is None:
            return

        if print_type == "inorder":
            self.print_inorder(self.root)
        elif print_type == "preorder":
            self.print_preorder(self.root)
        elif print_type == "postorder":
            self.print_postorder(self.root)
        elif print_type == "min":
            print(self.min_value(self.root).data)
        elif print_type == "max":
            print(self.max_value(self.root).data)
        elif print_type == "count":
            self.node_count = 0
            self.count_nodes(self.root)
            print("The number of nodes is:", self.node_count)
        print()

class TreeDisplay():
    """Class that implements the Tkinter display"""
    def __init__(self):
        self.display_window = None
        self.input_window = None
        self.main_frame = None
        self.temp_frame = None
        self.input_frame = None
        self.display_height = 720
        self.display_width = 920
        self.screen_width = None
        self.screen_height = None
        self.entry_var = None
        self.bst = BinarySearchTree()
        self.create_tree_display()
        self.create_input_display()
        self.add_widgets()

    def create_tree_display(self):
        """Creates the display for the tree visualization"""
        self.display_window = Tk()
        self.display_window.protocol("WM_DELETE_WINDOW", self.close_windows)
        self.screen_width = self.display_window.winfo_screenwidth()
        self.screen_height = self.display_window.winfo_screenheight()
        display_x_pos = self.screen_width/2 - self.display_width/2
        display_y_pos = self.screen_height*0.45 - self.display_height/2
        self.display_window.geometry('%dx%d+%d+%d' % (self.display_width,
                                                      self.display_height,
                                                      display_x_pos,
                                                      display_y_pos))
        self.display_window.title("Binary Search Tree")
        self.main_frame = Frame(self.display_window,
                                width=self.display_width,
                                height=self.display_height)
        self.main_frame.pack()
        self.temp_frame = Frame(self.main_frame,
                                width=self.display_width,
                                height=self.display_height)
        self.temp_frame.pack()

    def create_input_display(self):
        """Creates the display for entering values"""
        self.input_window = Toplevel()
        self.input_window.protocol("WM_DELETE_WINDOW", self.close_windows)
        text_window_width = 260
        text_window_height = 160
        text_window_x_pos = self.screen_width*0.82 - text_window_width/2
        text_window_y_pos = self.screen_height*0.45 - text_window_height/2
        self.input_window.title('Input')
        self.input_window.geometry('%dx%d+%d+%d' % (text_window_width,
                                                    text_window_height,
                                                    text_window_x_pos,
                                                    text_window_y_pos))
        self.input_frame = Frame(self.input_window,
                                 width=text_window_width,
                                 height=text_window_height)
        self.input_frame.pack()

    def add_widgets(self):
        """Adds widgets to the input display window"""
        add_button = Button(self.input_frame,
                            text='Add Node',
                            bg="blue",
                            fg="white",
                            font="Helvetica 10",
                            cursor="hand2",
                            command=self.add_node)
        add_button.place(x=20, y=90, width=100, height=50)
        delete_button = Button(self.input_frame,
                               text='Delete Node',
                               bg="red",
                               activebackground="red",
                               fg="white",
                               activeforeground="white",
                               font="Helvetica 10",
                               cursor="hand2",
                               command=self.delete_node)
        delete_button.place(x=140, y=90, width=100, height=50)
        self.user_entry = Entry(self.input_frame,
                                font="Helvetica 11",
                                justify="center")
        self.user_entry.place(x=80, y=20, width=100, height=50)
        self.user_entry.focus()

    def close_windows(self):
        """Deletes both windows"""
        self.display_window.destroy()

    def reset_display(self):
        """Resets the temp frame"""
        self.temp_frame.destroy()
        self.temp_frame = Frame(self.main_frame,
                                width=self.display_width,
                                height=self.display_height)
        self.temp_frame.pack()

    def add_node(self):
        """Adds a node to the tree"""
        new_value = self.user_entry.get()
        if new_value.isnumeric():
            new_value = int(new_value)
        else:
            self.user_entry.delete(0, 'end')
            return
        self.user_entry.delete(0, 'end')
        self.bst.insert_node(new_value)
        #self.bst.print_helper("inorder")
        self.reset_display()
        self.update_display(self.bst.root)

    def delete_node(self):
        """Deletes a node from the tree"""
        delete_value = self.user_entry.get()
        if delete_value.isnumeric():
            delete_value = int(delete_value)
        else:
            self.user_entry.delete(0, 'end')
            return
        self.user_entry.delete(0, 'end')
        self.bst.delete_node(delete_value)
        #self.bst.print_helper("inorder")
        self.reset_display()
        self.update_display(self.bst.root)

    def update_display(self, node):
        """Pre-order traversal that updates the display"""
        if node is None:
            return

        node_size = 50 * depth_size[node.depth]
        node_label = Label(self.temp_frame,
                           text=node.data,
                           bg=depth_colors[node.depth],
                           fg="white")
        node_label.place(x=node.x_pos,
                         y=depth_y_position[node.depth],
                         width=node_size,
                         height=node_size)

        if node.left is not None:
            node.left.depth = node.depth + 1
            # TODO: Check if node depth exceeds maximum
            node.left.x_pos = node.x_pos - depth_x_diff[node.left.depth] - node_size
            self.update_display(node.left)

        if node.right is not None:
            node.right.depth = node.depth + 1
            # TODO: Check if node depth exceeds maximum
            node.right.x_pos = node.x_pos + depth_x_diff[node.right.depth] + 50 * depth_size[node.depth]
            self.update_display(node.right)


def main():
    """Main function"""
    # Start up logging
    logging.basicConfig(format='[%(asctime)s] %(levelname)s : %(message)s',
                        level=logging.INFO)

    disp = TreeDisplay()
    disp.display_window.mainloop()

if __name__ == '__main__':
    main()
