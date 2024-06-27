package org.group_id_amit.dsa;

class Node{
    int val;
    Node prev;
    Node next;
    Node(int val, Node prev, Node next){
        this.val = val;
        this.prev = prev;
        this.next = next;
    }

    Node(int val){
        this(val, null, null);
    }
}

class CustomLinkedList{
    private Node dummyHead;
    private Node dummyTail;
    private int size; // Number of elements in the list

    // constructor
    public CustomLinkedList(){
        dummyHead = new Node(-1);
        dummyTail = new Node(-1);
        dummyHead.next = dummyTail;
        dummyTail.prev = dummyHead;
        size = 0;
    }

    // Add a node to the end of the list
    public void add(int data){
        Node node = new Node(data);
        Node tail = dummyTail.prev;
        tail.next = node;
        node.prev = tail;
        node.next = dummyTail;
        dummyTail.prev = node;
        size++;
    }

    // remove the first occurrence of a node with the given data
    public boolean remove(int data) {
        Node current = dummyHead.next;
        while(current!=null){
            if(current.val == data){
                Node prev = current.prev;
                Node next = current.next;
                prev.next = next;
                next.prev = prev;
                size--;
                return true;
            }
            current = current.next;
        }
        return false;
    }

    public void displayForward(){
        Node current = dummyHead.next;
        while(current != dummyTail){
            System.out.print(current.val + " -> ");
            current = current.next;
        }
        System.out.println("null");
    }




}

public class LinkedListExample {
    public static void main(String[] args){
    CustomLinkedList customLinkedList = new CustomLinkedList();
    customLinkedList.add(10);
    customLinkedList.add(20);
    customLinkedList.add(40);
    customLinkedList.add(60);
    customLinkedList.add(70);

    customLinkedList.displayForward();

    }

}
