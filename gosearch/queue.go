package main

/* TODO: Make this not a linked list */

type Queue struct {
	head *QueueNode
	tail *QueueNode
	size int
}

type QueueNode struct {
	url   string
	depth int
	next  *QueueNode
}

func NewQueue() *Queue {
	return &Queue{nil, nil, 0}
}

func (q *Queue) Enqueue(url string, depth int) {
	node := &QueueNode{url, depth, nil}
	prev := q.tail
	q.tail = node
	if prev == nil {
		q.head = node
	} else {
		prev.next = node
	}

	q.size++
}

func (q *Queue) Dequeue() (string, int) {
	url := q.head.url
	depth := q.head.depth
	q.head = q.head.next
	if q.head == nil {
		q.tail = nil
	}

	q.size--
	return url, depth
}

func (q *Queue) Size() int {
	return q.size
}
