package main

import "testing"

func TestQueue(t *testing.T) {
	data := []string{"a", "b", "c", "d"}

	queue := NewQueue()
	for _, k := range data {
		queue.Enqueue(k)
	}

	sz := queue.Size()
	if sz != len(data) {
		t.Errorf("Got wrong size: %v", sz)
	}

	for _, k := range data {
		s, err := queue.Dequeue()
		if err != nil {
			t.Fatalf("Failed to dequeue: %v", err)
		}

		if s != k {
			t.Errorf("Didn't get expected result from queue. Wanted: %v. Got: %v.", k, s)
		}
	}

	sz = queue.Size()
	if sz != 0 {
		t.Errorf("Queue not empty after all elements were dequeued.")
	}
}