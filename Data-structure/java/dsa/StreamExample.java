package org.group_id_amit.dsa;

import java.util.*;
import java.util.stream.Collectors;

public class StreamExample {
    public static void main(String[] args){
        int[] numbers = {4,3,2,1,-1,-6,10};
        String[] strings = {"s1", "s2", "sssss3334"};
        List<int[]> numberList = Arrays.asList(numbers);
        List<int[]> list =  new ArrayList<>(Arrays.asList(numbers)); // new is used because without new modification is restricted.

        List<String> words = Arrays.asList("hello", "world");
        List<Integer> lengths = words.stream()
                .map(String::length)
                .collect(Collectors.toList()); // [5, 5]
        System.out.println("lengths = " + lengths);

        List<List<String>> list_of_list = Arrays.asList(Arrays.asList("a", "b"), Arrays.asList("c", "d"));
        List<String> flatList = list_of_list.stream()
                .flatMap(Collection::stream)
                .collect(Collectors.toList()); // [a, b, c, d]
        System.out.println("flatList = " + flatList);

        List<String> fruits = Arrays.asList("apple", "banana", "cherry");
        List<String> filteredFruits = fruits.stream()
//                .filter(word -> word.startsWith("a"))
                .filter(word -> word.contains("rr"))
                .collect(Collectors.toList()); // [apple]
        System.out.println("filteredFruits = " + filteredFruits);

//        A terminal operation triggers the processing of the stream and produces a result or a side-effect.
//        Some common terminal operations are: forEach, collect, reduce
        List<String> charList = Arrays.asList("a", "b", "c");
        charList.stream().forEach(System.out::println); // a b c

        int sum = Arrays.asList(1, 2, 3, 4).stream().reduce(0, Integer::sum); // 10
        System.out.println("sum via reduce = " + sum);
        List<Integer> inputNumbers = Arrays.asList(4,-1,5);
        Integer secondLargest = inputNumbers.stream()
//                .sorted(Comparator.reverseOrder())
                .sorted()
                .skip(1)  // Skip the first (largest) element
                .findFirst()
                .orElse(null);  // Safely return null if the second element doesn't exist
        System.out.println("second largest number = " + secondLargest);

        List<Integer> squareNumbers = Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> evenSquares = squareNumbers.stream()
                .filter(n -> n % 2 == 0) // Intermediate: filter
                .map(n -> n * n)         // Intermediate: map
                .collect(Collectors.toList()); // Terminal: collect
        System.out.println("evenSquares = " + evenSquares);

        Map<String, Integer> unsortedMap = new HashMap<>();
        unsortedMap.put("b", 2);
        unsortedMap.put("a", 1);
        unsortedMap.put("c", 3);

        Map<String, Integer> sortedMap = unsortedMap.entrySet()
                .stream()
                .sorted(Map.Entry.comparingByKey())
                .collect(Collectors.toMap(
                        Map.Entry::getKey,
                        Map.Entry::getValue,
                        (oldValue, newValue) -> oldValue, LinkedHashMap::new
                ));

        System.out.println("sortedMap" + sortedMap); // Output: {a=1, b=2, c=3}


    }
}
