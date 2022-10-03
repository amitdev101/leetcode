public int maxLengthValidSubArray(int[] processingPower, int[] bootingPower, long maxPower){
        if(processingPower == null || bootingPower == null
                || processingPower.length == 0 || processingPower.length != bootingPower.length){
            return 0;
        }

        PriorityQueue<Integer> maxBootingPower = new PriorityQueue<>((a, b) -> Integer.compare(b, a));
        int maxLength = 0;
        int currentLength = 1;

        int start = 0;
        int end = 0;

        long currentSumProcessingPower = processingPower[0];
        maxBootingPower.add(bootingPower[0]);
        while(end < processingPower.length){
            int currentBootingPower = maxBootingPower.peek();
            long currentPower = currentBootingPower + currentSumProcessingPower * currentLength;

            if(currentPower <= maxPower){
                maxLength = currentLength;
                end++;
                currentLength++;
            }
            else{
                currentSumProcessingPower -= processingPower[start];
                maxBootingPower.remove(bootingPower[start]);
                start++;
                end++;
            }



            if(end < processingPower.length){
                maxBootingPower.add(bootingPower[end]);
                currentSumProcessingPower += processingPower[end];
            }
        }

        return maxLength;
    }

}
