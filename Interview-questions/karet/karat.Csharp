// Question :: find if exactly one pair and 0 or more triplets

class CS148876 {
    public static bool IsCompleteHand(String tiles) {
        var counter = new int[10];
        foreach(char c in tiles) {
            counter[c - '0'] += 1;
        }

        var hasOnePair = false;
        foreach(var c in counter) {
            if (c % 3 == 1) return false;
            if (c % 3 == 2) {
                if (hasOnePair) {
                    return false;
                } else {
                    hasOnePair = true;
                }
            }
        }
        return hasOnePair;
    }

    public static void Test(String tiles) {
        Console.WriteLine(tiles + ": " + (IsCompleteHand(tiles) ? "COMPLETE" : "NOT COMPLETE"));
    }