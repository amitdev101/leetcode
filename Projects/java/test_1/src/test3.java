import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;

public class test3 {
    // arr = [1,2,3,4,5,6,7]
//    split(3)
//    ans = [3,2,1,6,5,4,7]
    // [0,k-1] [1,2,3]
    // reverse this subarray
//    swap(newstart+i,newstart+k-i)
    public static  void main(String[] args){
        Integer[] myarr = {1,2,3,4,5,6,7};
        Integer split = 3;
        Integer newstart = 0;
        while(newstart+split<= myarr.length){
//            Integer mid = (newstart+split)/2;
            Integer mid = split/2;
            for(Integer i=0; i<mid; i++){
                // here swapping
                Integer x,y;
                x = myarr[newstart+ i];
                y = myarr[newstart+split-1-i];
                myarr[newstart+i] = y;
                myarr[newstart+split-1-i] = x;
                // array swapped
            }
            newstart+=split;
        }

        System.out.println(Arrays.toString(myarr));

    }


}
