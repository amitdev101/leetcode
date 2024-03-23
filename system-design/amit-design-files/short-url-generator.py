


"Daily Active Users (DAU):

Given the dynamic nature of user behavior and market conditions, the DAU estimation might vary. However, here is a rough estimate:

1B (dau social media users)
* .01 (percent that post shortener links each day)
* .25 (our estimated market share)
= 2.5M DAU

Storage Requirements:

Let's consider the database system storage overhead and the possibility of users creating more than one short link per day. The revised calculation is as follows:

dbRow = 100b (original url) + 8b (short url) + 500b (metadata & analytics) = about 1KB

2.5M (dau)
* .01 (100:1 read to write ratio)
* 2 (average links shortened /day /user, considering users might create more than one link per day)
* 1 KB (dbRow)
* 2 (redundancy)
* 2 (backup)
* 2 (growth)
* 365 (days per year)
* 10 (store data 10 years)
= about 2TB

Additionally, let's add a 20% overhead for the database system itself, bringing the total to approximately 2.4TB."
=======================
Users (uid, phone, email, props, create time, update_time) -> 2100 Bytes per user
Urls (url_id, short_url, long_url, create_time, update_time, props (Json Field)) -> 16Bytes + how much for 1 char?


uid -> md5 hash (128 bit -> 16 Bytes) phone (3 country code + 10 for mobile number) + (email -> 60 Bytes) 
timestamp (8 Bytes) + props (Json field average (2000 Bytes)
16+3+10+60+8+2000 ~ 2100 Bytes per user




======================

"For current system i will focus on availability. eventual consistency will be fine for this. 
we don't need immediate consistency. to overcome for new url generated and accessed then we can store in our cache (redis). 
So according to CAP theorem it will be AP system where we sacrifice our consistency to make it highly available and partition tolerant.
As from user's perspective it will be okay if my short url is not present for a short period of time. 
But our services should be available all the time."