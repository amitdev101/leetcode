import java.util.HashMap;
import java.util.Map;

public class Test2 {
    public static void main(String[] args) {
        // finite length string
        // s = "This is mumbai";
        String input = "This is mumbai";
        Map<Character, Integer> charCountMap = new HashMap<>();
        input.chars().mapToObj(c->(char) c).forEach(c-> charCountMap.put(c, charCountMap.getOrDefault(c,0) + 1));

        Map.Entry<Character,Integer> mostRepeatedEntry = charCountMap.entrySet().stream().max(Map.Entry.comparingByValue()).orElseThrow(()-> new IllegalStateException("Empty string given")) ;
        System.out.println("Most repeated char : " + mostRepeatedEntry.getKey() + " count: "+ mostRepeatedEntry.getValue());
    }

}
