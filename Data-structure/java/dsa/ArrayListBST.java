package org.group_id_amit.dsa;

import java.util.ArrayList;
import java.util.Arrays;

public class ArrayListBST {
    public static int binarySearch(ArrayList<Integer> list, int target){
        int left = 0;
        int right = list.size() - 1;
        while(left <= right){
            int mid = (left+right)/2;
            if(list.get(mid)==target){
                return mid;
            }
            if(list.get(mid) < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args){
        ArrayList<Integer> list = new ArrayList<>(Arrays.asList(2,3,4,5,10,40));
        int result = binarySearch(list, 6);
        System.out.printf("result = %d", result);
    }
}
