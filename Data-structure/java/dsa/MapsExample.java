package org.group_id_amit.dsa;

import java.util.*;

public class MapsExample {
    public static void main(String[] args) {
        List<String> words = Arrays.asList("apple", "banana", "apple", "orange", "banana", "apple");
        Map<String, Integer> map = new HashMap<>();
        for (String word : words) {
            word = word.toLowerCase();
            map.put(word, map.getOrDefault(word, 0) + 1);
        }
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.println(entry.getKey() + " = " + entry.getValue());
        }
        int size = map.size(); // Returns the number of key-value pairs
        System.out.println("size = " + size);
        boolean isEmpty = map.isEmpty(); // Returns false if the map has elements
        System.out.println("isEmpty = " + isEmpty);

        Set<String> keys = map.keySet();
        System.out.println("keys = " + keys);
        Collection<Integer> values = map.values();
        System.out.println("values = " + values);
        boolean hasKey = map.containsKey("banana"); // Returns true
        System.out.println("hasKey = " + hasKey);
        boolean hasValue = map.containsValue(1); // Returns true
        System.out.println("hasValue = " + hasValue);
        map.remove("banana"); // Removes the key-value pair for key "banana"
        System.out.println("map = " + map);



    }
}
