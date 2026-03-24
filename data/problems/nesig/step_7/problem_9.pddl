(define (problem problem_9)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 - block
)

(:init
	(clear obj1)
	(clear obj2)
	(handempty)
	(on obj1 obj0)
	(ontable obj0)
	(ontable obj2)
)

(:goal (and
	(on obj0 obj1)
	(on obj2 obj0)
))
)