package org.group_id_amit.dsa;

import java.util.Objects;

class Person{
    String name;
    Integer age;

    Person(String name, Integer age){
        this.name = name;
        this.age = age;
    }

    // Override equals method
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person person = (Person) obj;
        return Objects.equals(name, person.name) && Objects.equals(age, person.age);
    }

    // Override hashCode method
//    @Override
//    public int hashCode() {
//        return Objects.hash(name, age);
//    }
}


public class EqualsTest {
    public static void main(String[] args){
        Person p1 = new Person("name1", 20);
        Person p2 = new Person("name1", 20);
        System.out.println("Hash code of p1: " + p1.hashCode());
        System.out.println("Hash code of p2: " + p2.hashCode());
        System.out.println(String.valueOf(p1==p2) + " equals " + p1.equals(p2) );
        System.out.println(p1 == p2); // false, p1 and p2 refer to different memory locations
        System.out.println(p1.equals(p2)); // true, p1 and p2 are considered equal based on their content
    }
}
