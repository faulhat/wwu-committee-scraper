package main

import "testing"

func TestQueue(t *testing.T) {
	names := []string{"a", "b", "c", "d"}
	nums := []int{1, 5, 3, 4}

	queue := NewQueue()
	for i, k := range names {
		queue.Enqueue(k, nums[i])
	}

	sz := queue.Size()
	if sz != len(names) {
		t.Errorf("Got wrong size: %v", sz)
	}

	for i, k := range names {
		s, n := queue.Dequeue()

		if s != k {
			t.Errorf("Didn't get expected result from queue at pos %v. Wanted: %v. Got: %v.", i, k, s)
		}

		if n != nums[i] {
			t.Errorf("Didn't get expected result from queue at pos %v. Wanted: %v. Got: %v.", i, nums[i], n)
		}
	}

	sz = queue.Size()
	if sz != 0 {
		t.Errorf("Queue not empty after all elements were dequeued.")
	}
}
