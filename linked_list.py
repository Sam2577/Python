
import unittest

class linked_list(object):

    class node(object):

        def __init__(self, value, next=None):
            self.value = value
            self.next = next

    def __init__(self):  # initialize class variables
        self.front = None
        self.rear = None
        self.num_items = 0

    def __str__(self):
        current = self.front
        if current:
            printed_list = "["
            while current.next:
                printed_list += str(current.value) + ", "
                current = current.next
            printed_list += str(current.value) + "]"
        else:
            printed_list = "[]"
            
        return printed_list

    def __iter__(self):
        curr = self.front
        while curr:
            yield curr.value
            curr = curr.next

    def push_front(self, value):
        new_front = linked_list.node(value, self.front)  # instantiate node with value and next

        self.front = new_front

        if not self.rear:  # if rear is set to None, set it to new_front (in case this is the first node added)
            self.rear = new_front

        self.num_items += 1

    def push_back(self, value):
        new_back = linked_list.node(value, None)
        if self.rear:
            self.rear.next = new_back

        self.rear = new_back

        if not self.front:
            self.front = new_back

        self.num_items += 1

    def empty(self):
        if self.num_items < 1:
            return True
        return False

    def pop_front(self):
        if self.empty():
            raise RuntimeError("Cannot pop from empty list")
        else:
            front_value = self.front.value

            if self.front.next:
                self.front = self.front.next  # "deletes" first item because self.front no longer points to it.
            else:
                self.rear = None
                
            self.num_items -= 1
            
            return front_value

    def pop_back(self):
        if self.empty():
            raise RuntimeError("Cannot pop from empty list")
        else:
            back_value = self.rear.value

            if self.rear == self.front:  # if there is only one item in the list
                self.rear = self.front = None
            else:
                current = self.front  
                while current.next:                   # iterate through the list until 'next' refers to same object as self.rear
                    if current.next == self.rear:     # this is the next-to-last item, so it will be the new rear item
                        current.next = None
                        self.rear = current
                    else:
                        current = current.next 
        
            self.num_items -= 1
            
            return back_value


class test_linked_list (unittest.TestCase):
    def test_none(self):
        self.assertTrue(linked_list().empty())
    def test_pop_front_empty(self):
        self.assertRaises(RuntimeError, lambda: linked_list().pop_front())
    def test_pop_back_empty(self):
        self.assertRaises(RuntimeError, lambda: linked_list().pop_back())
    def test_push_back_pop_front(self):
        ll = linked_list()
        ll.push_back(1)
        ll.push_back(2)
        ll.push_back(3)
        self.assertFalse(ll.empty())
        self.assertEquals(ll.pop_front(), 1)
        self.assertEquals(ll.pop_front(), 2)
        self.assertEquals(ll.pop_front(), 3)
        self.assertTrue(ll.empty())
    def test_push_front_pop_front(self):
        ll = linked_list()
        ll.push_front(1)
        ll.push_front(2)
        ll.push_front(3)
        self.assertEquals(ll.pop_front(), 3)
        self.assertEquals(ll.pop_front(), 2)
        self.assertEquals(ll.pop_front(), 1)
        self.assertTrue(ll.empty())
    def test_push_front_pop_back(self):
        ll = linked_list()
        ll.push_front(1)
        ll.push_front(2)
        ll.push_front(3)
        self.assertFalse(ll.empty())
        self.assertEquals(ll.pop_back(), 1)
        self.assertEquals(ll.pop_back(), 2)
        self.assertEquals(ll.pop_back(), 3)
        self.assertTrue(ll.empty())
    def test_push_back_pop_back(self):
        ll = linked_list()
        ll.push_back(1)
        ll.push_back("foo")
        ll.push_back([3,2,1])
        self.assertFalse(ll.empty())
        self.assertEquals(ll.pop_back(),[3,2,1])
        self.assertEquals(ll.pop_back(), "foo")
        self.assertEquals(ll.pop_back(), 1)
        self.assertTrue(ll.empty())


class factorial:
    def fact(self, a):
        if a < 0: raise ValueError("Less than zero")
        if a == 0 or a == 1: return 1

        stack = linked_list()
        while a > 1:
            stack.push_front(a)
            a -= 1

        result = 1
        while not stack.empty():
            result *= stack.pop_front()

        return result

class test_factorial (unittest.TestCase):
    def test_less_than_zero(self):
        self.assertRaises(ValueError, lambda: factorial().fact(-1))
    def test_zero(self):
        self.assertEquals(factorial().fact(0), 1)
    def test_one(self):
        self.assertEquals(factorial().fact(1), 1)
    def test_two(self):
        self.assertEquals(factorial().fact(2), 2)
    def test_10(self):
        self.assertEquals(factorial().fact(10), 10*9*8*7*6*5*4*3*2*1)

if __name__ ==  "__main__":
        print (factorial().fact(1))
        print (factorial().fact(2))
        print (factorial().fact(100))
