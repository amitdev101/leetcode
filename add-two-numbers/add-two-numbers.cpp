/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        // using carry method
        ListNode* head = nullptr;
        ListNode* tail = nullptr;
        ListNode* tempnode;
        int carry=0, r=0;
        int num1,num2;
        while(carry || l1 || l2){
            num1 = num2 = 0;
            if(l1){
                num1 = l1->val;
                l1 = l1->next;
            }
            if (l2){
                num2 = l2->val;
                l2 = l2->next;
            }
            
            int num = num1 + num2 + carry;
            carry = num/10;
            r = num%10;
            tempnode = new ListNode(r);
            if(!head){
                head = tail = tempnode;
            }
            else {
                tail->next = tempnode;
                tail = tempnode;
            }
            
        }
        return head;
    }
};