(define (problem problem_22)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 - block
)

(:init
	(clear obj0)
	(clear obj3)
	(clear obj4)
	(handempty)
	(on obj3 obj2)
	(on obj4 obj1)
	(ontable obj0)
	(ontable obj1)
	(ontable obj2)
)

(:goal (and
	(on obj3 obj2)
))
)