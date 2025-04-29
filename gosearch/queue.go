package main

import "errors"

/* TODO: Make this not a linked list */

type Queue struct {
	head *QueueNode
	tail *QueueNode
	size int
}

type QueueNode struct {
	data string
	next *QueueNode
}

func NewQueue() *Queue {
	return &Queue{nil, nil, 0}
}

func (q *Queue) Enqueue(s string) {
	node := &QueueNode{s, nil}
	prev := q.tail
	q.tail = node
	if prev == nil {
		q.head = node
	} else {
		prev.next = node
	}

	q.size++
}

func (q *Queue) Dequeue() (string, error) {
	if q.head == nil {
		return "", errors.New("Queue empty!")
	} else {
		s := q.head.data
		q.head = q.head.next
		if q.head == nil {
			q.tail = nil
		}

		q.size--
		return s, nil
	}
}

func (q *Queue) Size() int {
	return q.size
} 
