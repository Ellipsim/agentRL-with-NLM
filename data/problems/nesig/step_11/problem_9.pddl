(define (problem problem_9)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 - block
)

(:init
	(clear obj1)
	(clear obj2)
	(clear obj3)
	(handempty)
	(on obj1 obj0)
	(ontable obj0)
	(ontable obj2)
	(ontable obj3)
)

(:goal (and
	(on obj2 obj3)
))
)