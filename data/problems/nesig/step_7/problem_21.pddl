(define (problem problem_21)

(:domain BLOCKS)

(:objects
	obj0 obj1 obj2 obj3 obj4 - block
)

(:init
	(clear obj0)
	(clear obj2)
	(clear obj4)
	(handempty)
	(on obj2 obj1)
	(on obj4 obj3)
	(ontable obj0)
	(ontable obj1)
	(ontable obj3)
)

(:goal (and
	(on obj2 obj1)
	(on obj4 obj3)
))
)