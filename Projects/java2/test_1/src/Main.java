import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello world!");
        String s = "abcdab";
        Map<Character, Long> result = s.chars().mapToObj(c->(char)c).collect(Collectors.groupingBy(c->c,Collectors.counting()));
        for(Character c: result.keySet()){
            System.out.println(c +" "+ result.get(c));
        }
//        String s = null;
        Optional<String> optionalS = Optional.ofNullable(s);
        if(optionalS.isPresent()){
//            it's not null
        }
        else {
            // it's null
        }

    }
}