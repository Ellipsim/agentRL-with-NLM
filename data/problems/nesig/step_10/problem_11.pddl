(define (problem problem_11)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 - block
)

(:init
	(clear obj1)
	(clear obj3)
	(clear obj4)
	(handempty)
	(on obj1 obj0)
	(on obj3 obj2)
	(ontable obj0)
	(ontable obj2)
	(ontable obj4)
)

(:goal (and
	(on obj3 obj2)
))
)