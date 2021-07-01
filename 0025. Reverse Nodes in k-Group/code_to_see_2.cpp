// https://leetcode.com/problems/reverse-nodes-in-k-group/discuss/1300996/C%2B%2B%3A-super-easy-to-understand

ListNode* reverseKGroup(ListNode* head, int k)
{
	ListNode dummy;
	dummy.next = head;

	int count = 0;
	ListNode* pre = &dummy;
	ListNode* begin = head;
	ListNode* end = begin;

	while (end && count < k)
	{
		++count;
		if (count == k)
		{
			reverseList(&begin, &end);
			pre->next = begin;
			pre = end;
			begin = pre->next;
			end = begin;
			count = 0;
			continue;
		}
		end = end->next;
	}
	return dummy.next;
}

// Reverse a list, giving the first and last node of the range to reverse

void reverseList(ListNode** head, ListNode** tail)
{
	if (!(*head) || *head == *tail)
	{
		return;
	}

	ListNode dummy;
	dummy.next = *head;

	ListNode* node = (*head)->next;
	// Note: the is just part of a large list, can't set 
	// new tail next to null.
	ListNode* new_tail = *head;

	while (node != *tail)
	{
		ListNode* temp = node->next;
		node->next = dummy.next;
		dummy.next = node;
		node = temp;
	}

	// Still need to reverse last node, and remember to link new_tail
	// next to its proper next.
	new_tail->next = node->next;
	node->next = dummy.next;
	dummy.next = node;

	*head = dummy.next;
	*tail = new_tail;
}