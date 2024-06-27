package org.group_id_amit.dsa;

class Parent {
    private void display() {
        System.out.println("Parent display");
    }
}

class Child extends Parent {
    public void display() {
        System.out.println("Child display");
    }
}

public class ParentChildTest {
        public static void main(String[] args) {
            Parent obj = new Child();
            Child childObj = new Child();
            childObj.display();
//            obj.display();  // Compilation error
    }
}
