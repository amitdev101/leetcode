package org.group_id_amit.dsa;
/*
Understanding Strings in Java

    Immutability:
        Strings in Java are immutable, meaning that once a String object is created, its value cannot be changed.
        Any operation that seems to modify a String actually creates a new String object.

    String Pool:
        Java optimizes the storage of strings using a concept known as the String Pool.
        When a string is created, Java checks the pool to see if an identical string already exists.
        If it does, Java reuses the existing string instead of creating a new one. This helps in saving memory.

    Creation of Strings:
        Literal: String str1 = "Hello";
        Using new keyword: String str2 = new String("Hello");
        The new keyword always creates a new string object, bypassing the string pool.
 */

public class StringMethodsExample {
    public static void main(String[] args) {
        String str = "Hello, World!";

        // Length of the string
        System.out.println("Length: " + str.length());

        // Character at a specific index
        System.out.println("Character at index 1: " + str.charAt(1));

        // Substring
        System.out.println("Substring from index 7: " + str.substring(7));
        System.out.println("Substring from index 7 to 12: " + str.substring(7, 12));

        // Index of a character or substring
        System.out.println("Index of 'o': " + str.indexOf('o'));
        System.out.println("Last index of 'o': " + str.lastIndexOf('o'));

        // Equals and equalsIgnoreCase
        System.out.println("Equals 'Hello, World!': " + str.equals("Hello, World!"));
        System.out.println("Equals 'hello, world!' (ignore case): " + str.equalsIgnoreCase("hello, world!"));

        // CompareTo
        System.out.println("Compare to 'Hello': " + str.compareTo("Hello"));

        // StartsWith and EndsWith
        System.out.println("Starts with 'Hello': " + str.startsWith("Hello"));
        System.out.println("Ends with 'World!': " + str.endsWith("World!"));

        // Replace
        System.out.println("Replace 'o' with 'a': " + str.replace('o', 'a'));

        // Split
        String[] parts = str.split(", ");
        System.out.println("Split by ', ': " + String.join(" | ", parts));

        // Trim
        String strWithSpaces = "   Hello, World!   ";
        System.out.println("Trimmed string: '" + strWithSpaces.trim() + "'");

        // Case conversion
        System.out.println("To lower case: " + str.toLowerCase());
        System.out.println("To upper case: " + str.toUpperCase());

        // Value of different types
        int num = 100;
        System.out.println("Value of int 100: " + String.valueOf(num));

        // IsEmpty and IsBlank
        String emptyStr = "";
        String blankStr = "   ";
        System.out.println("Is empty: " + emptyStr.isEmpty());
    }
}


