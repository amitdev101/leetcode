// Algorithm to find all the prime factors of a number

vector<long long int> prime_factor(long long int num){
    vector<long long int> factors;
    if(num%2==0){
        while(num%2==0){
            num/=2;
        }
        factors.push_back(2);
    }
    long long int i=3;

    for(i=3;i<=sqrt(num);i+=2){
        if(num%i==0){
            while(num%i==0)
                num/=i;
            factors.push_back(i);
        }
    }
    if(num>2)
        factors.push_back(num);
    return factors; // factors is a vector of long long int  
}
