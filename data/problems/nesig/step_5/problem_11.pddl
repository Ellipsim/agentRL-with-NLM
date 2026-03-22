(define (problem problem_11)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 - block
)

(:init
	(clear obj2)
	(clear obj3)
	(handempty)
	(on obj2 obj0)
	(on obj3 obj1)
	(ontable obj0)
	(ontable obj1)
)

(:goal (and
	(on obj2 obj0)
	(on obj3 obj1)
))
)