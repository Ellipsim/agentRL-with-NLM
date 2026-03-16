(define (problem problem_17)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 - block
)

(:init
	(clear obj3)
	(clear obj4)
	(handempty)
	(on obj2 obj0)
	(on obj3 obj2)
	(on obj4 obj1)
	(ontable obj0)
	(ontable obj1)
)

(:goal (and
	(on obj2 obj0)
))
)