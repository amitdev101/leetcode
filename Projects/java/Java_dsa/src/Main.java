import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
//        System.out.println("Hello 1234world!");
//        int n = 10;
//        long ans = fibonacci(n);
//        System.out.printf("ans %d ", ans);
//        Stri
        System.out.println(first_non_repeating_char("abcdabcdfeg"));
    }

    private static long fibonacci(int n) {
        if (n<=1){
            return n;
        }
        return fibonacci(n-1) + fibonacci(n-2);
    }

    private static int max_difference(int[] arr){
        int ans = 0;
        int min=arr[0], max=arr[0];
        for(int i=0; i<arr.length; i++){
            if(arr[i]<min){
                min = arr[i];
            }
            if(arr[i]>max){
                max = arr[i];
            }
        }
        return max-min;
    }

    private static Character first_non_repeating_char(String s){
        Map<Character, Integer> frequencyMap = new LinkedHashMap<>();
        for(int i=0; i<s.length(); i++){
            char c = s.charAt(i);
            if(frequencyMap.containsKey(c)){
                frequencyMap.put(c,frequencyMap.get(c)+1);
            }
            else{
                frequencyMap.put(c,1);
            }
        }
        for (Map.Entry<Character,Integer> entry: frequencyMap.entrySet()){
            if(entry.getValue()==1){
                return entry.getKey();
            }
        }

        return null;
    }
    

}