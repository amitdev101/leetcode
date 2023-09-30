public class parent_child_test {
    public static void main(String[] args) {
        Parent test = new Child();
        test.display1();
        test.display2();
        Child ctest = (Child) test;
        ctest.display1();
        ctest.display2();
        ctest.display3();
        ctest.display4();

        Parent ptest = new Parent();
        ptest.display1();
        ptest.display2();
        ctest = (Child) ptest;
        ctest.display4();
        ctest.display1();





//        test.display3();
    }
}


class Parent{
    public void display1(){
        System.out.println("Parent class display1 called");
    }
    public static void display2(){
        System.out.println("Parent Static display2 called");
    }

}

class Child extends Parent{
    public void display1(){
        System.out.println("Child class display1 called");
    }
    public static void display2(){
        System.out.println("Child Static display2 called");
    }

    public static void display3(){
        System.out.println("Child static display3 method called");
    }

    public  void display4(){
        System.out.println("Child display4 method called");
    }
}


