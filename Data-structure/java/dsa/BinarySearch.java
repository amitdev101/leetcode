package org.group_id_amit.dsa;

public class BinarySearch {
    public static int binarySearch(int[] array, int target){
        int left = 0;
        int right = array.length - 1;
        while (left<=right){
            int mid = left + (right-left)/2; // Prevents overflow
            if(array[mid]==target){
                return mid;
            }
            if(array[mid]<target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }

    public static void main(String[] args){
        int[] array = {2,3,4,10,40};
        int target = 40;
        int result = binarySearch(array, target);
        System.out.printf("result =  %d", result);
    }
}


